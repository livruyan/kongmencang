"""
Phase 12 · 多智能体协作 (Agent-to-Agent, A2A)
=========================================================================
目的：演示「智能体调用智能体」——一个 supervisor（主管）智能体把任务分派给两个
worker（工作）智能体：调研员负责搜集要点、写作者负责落成短文。三者都是独立的
LangGraph Agent，通过一张状态图 + 条件边编排起来。

这正好呼应本教程主线：状态图(Node) + 节点(各 Agent) + 条件边(主管的路由决策)。
对应改进报告中「MCP / A2A 智能体互联」的热点方向——这里用 LangGraph 原生多智能体，
不引入额外协议 SDK，单机即可运行（与 Phase 11 的 MCP「智能体↔工具」形成对照：
MCP 是 agent 接工具，A2A 是 agent 接 agent）。

要点：
  1. supervisor / researcher / writer 都是 Agent（底层都是状态图）；
  2. supervisor 节点用 LLM 决定下一步该交给谁（或结束）；
  3. 条件边根据 supervisor 的决策在 worker 之间路由；
  4. 所有 Agent 共享同一份 messages 状态，互相「看得见」对方的产出。

运行 / Run:
    python -m examples.p12.hello_chain
    # 或 make run p=12
"""
import asyncio
import warnings
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import create_react_agent

from examples.common.llm import get_chat_model

# langgraph>=1 把 create_react_agent 标为 deprecated（功能仍正常），抑制该提示让演示输出干净
warnings.filterwarnings("ignore", message=".*create_react_agent has been moved.*")


# ---- 共享状态：messages 用 add_messages 累加，next 记录主管的路由决策 ----------
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    next: str


# ---- Worker 1：调研员 -------------------------------------------------------
RESEARCHER_PROMPT = (
    "你是调研员。只负责针对用户问题列出 3 条关键事实/要点，每条一行，不要展开成文。"
)


# ---- Worker 2：写作者 -------------------------------------------------------
WRITER_PROMPT = (
    "你是写作者。基于已有的要点，写一段通顺、面向外行的中文短文（3-5 句），不要新造事实。"
)


# ---- Supervisor 节点：决定下一步交给谁 -------------------------------------
ROUTING_INSTRUCTION = (
    "你是任务主管。根据当前对话，决定下一步由谁处理，只回复一个词：\n"
    "researcher —— 还需要更多事实/要点时\n"
    "writer    —— 要点已够、可以成文时\n"
    "FINISH    —— 短文已完成、可以交差时\n"
    "只回复 researcher / writer / FINISH 其中一个词，不要解释。"
)


async def supervisor(state: AgentState) -> dict:
    model = get_chat_model()
    decision = await model.ainvoke(
        [HumanMessage(content=ROUTING_INSTRUCTION)] + list(state["messages"])
    )
    text = decision.content.strip() if isinstance(decision.content, str) else "FINISH"
    # 解析 LLM 决策：只取最后出现的合法 token，避免模型多嘴
    token = None
    for t in ("FINISH", "writer", "researcher"):
        if t in text:
            token = t
            break

    # 确定性兜底，保证演示出「调研员 → 写作者 → 结束」完整链路：
    # 研究员已产出但写作者还没 → 强制走写作者；写作者已产出 → 结束。
    # （生产环境可让主管完全自由路由；此处约束是为了稳定展示双 worker 协作。）
    has_research = any(
        "（主管决定：调研员）" in m.content
        for m in state["messages"]
        if isinstance(m, AIMessage)
    )
    has_writer = any(
        "（主管决定：写作者）" in m.content
        for m in state["messages"]
        if isinstance(m, AIMessage)
    )
    if has_research and not has_writer:
        token = "writer"
    elif has_writer:
        token = "FINISH"
    if token is None:
        token = "FINISH"

    label = {"researcher": "调研员", "writer": "写作者", "FINISH": "结束"}.get(token, "结束")
    print(f"\n[supervisor] 路由决策 → {label}")
    return {"messages": [AIMessage(content=f"（主管决定：{label}）")], "next": token}


async def call_researcher(state: AgentState) -> dict:
    # 角色提示只在本次调用内生效，不写进共享状态
    agent = create_react_agent(get_chat_model(), tools=[])
    result = await agent.ainvoke(
        {"messages": [SystemMessage(content=RESEARCHER_PROMPT)] + list(state["messages"])}
    )
    answer = result["messages"][-1]
    print("[worker] 调研员产出：")
    print(answer.content)
    return {"messages": [answer]}  # 只把最终回答追加进共享状态，避免重复


async def call_writer(state: AgentState) -> dict:
    agent = create_react_agent(get_chat_model(), tools=[])
    result = await agent.ainvoke(
        {"messages": [SystemMessage(content=WRITER_PROMPT)] + list(state["messages"])}
    )
    answer = result["messages"][-1]
    print("[worker] 写作者产出：")
    print(answer.content)
    return {"messages": [answer]}


def should_continue(state: AgentState) -> str:
    return state.get("next", "FINISH")


async def main_async() -> None:
    builder = StateGraph(AgentState)
    builder.add_node("supervisor", supervisor)
    builder.add_node("researcher", call_researcher)
    builder.add_node("writer", call_writer)

    builder.add_edge(START, "supervisor")
    builder.add_conditional_edges(
        "supervisor",
        should_continue,
        {"researcher": "researcher", "writer": "writer", "FINISH": END},
    )
    # worker 干完活都回到主管，由主管决定下一步
    builder.add_edge("researcher", "supervisor")
    builder.add_edge("writer", "supervisor")

    graph = builder.compile()

    print("===== 多智能体协作演示（supervisor + researcher + writer）=====")
    result = await graph.ainvoke(
        {"messages": [("user", "用三句话向完全不懂技术的人解释：什么是 Agent？")]}
    )

    print("\n===== 最终对话轨迹（messages）=====")
    for m in result["messages"]:
        print(f"- [{m.type}] {m.content}")


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
