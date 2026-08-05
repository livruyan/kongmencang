"""
Phase 9 · Capstone：端到端多 Agent 研究系统（整合全部知识点）
====================================================================
这是整个课程的「毕业设计」——把前面所有概念收进一张 LangGraph 图里：

  - Phase 4 工具：research 节点调用一个检索工具（这里用 mock 检索）
  - Phase 5 路由：coordinator 按问题类型分流到不同专家
  - Phase 6 图：StateGraph 显式建模所有节点/边/条件边
  - Phase 7 HITL：在发布前用 interrupt 暂停，等人类审批
  - Phase 3 循环：各节点内部本质都是「思考→行动」的微观循环

图结构：
  START -> coordinator
  coordinator --(route)--> research / math
  research -> writer -> reviewer -> approval
  approval --(yes)--> publish
  approval --(no)--> revise -> reviewer (回环)
  publish/revise -> END

运行（需配置 .env 的 LLM provider）：
  python -m examples.p9.capstone
"""

from typing import TypedDict

from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt

from examples.common.llm import get_chat_model


# ---------------------------------------------------------------------------
# 状态
# ---------------------------------------------------------------------------
class CapstoneState(TypedDict):
    question: str
    route: str          # coordinator 决策：research / math
    research: str
    draft: str
    review: str
    approved: bool
    final: str


# ---------------------------------------------------------------------------
# 工具（Phase 4 知识）
# ---------------------------------------------------------------------------
@tool
def search(query: str) -> str:
    """检索知识库。当用户需要事实性资料时使用。"""
    kb = {
        "langgraph": "LangGraph 用状态图建模 Agent 工作流。",
        "agent": "Agent 是能自主决策并调用工具的智能体。",
    }
    return kb.get(query.lower(), f"未找到关于「{query}」的资料（演示数据）。")


# ---------------------------------------------------------------------------
# 节点
# ---------------------------------------------------------------------------
def coordinator(state: CapstoneState) -> dict:
    model = get_chat_model()
    choice = model.invoke([
        SystemMessage(content="你是协调者。若问题需要查证资料回复 research，若需要计算回复 math。只回一个词。"),
        HumanMessage(content=state["question"]),
    ]).content.strip().lower()
    return {"route": choice if choice in ("research", "math") else "research"}


def research_node(state: CapstoneState) -> dict:
    # 演示工具调用：把模型和检索工具绑定，执行后回填
    model = get_chat_model()
    model_with_tools = model.bind_tools([search])
    msg = model_with_tools.invoke([
        SystemMessage(content="你是研究员，必要时调用 search 工具，最后给出 2 条要点，每行一条。"),
        HumanMessage(content=f"问题：{state['question']}"),
    ])
    content = msg.content or ""
    for call in getattr(msg, "tool_calls", []) or []:
        out = search.invoke(call["args"])
        msg = model_with_tools.invoke([
            msg,
            ToolMessage(content=str(out), tool_call_id=call["id"]),
        ])
        content = msg.content
    return {"research": content.strip()}


def math_node(state: CapstoneState) -> dict:
    model = get_chat_model()
    out = model.invoke([
        SystemMessage(content="你是数学专家，只给出计算答案。"),
        HumanMessage(content=state["question"]),
    ]).content.strip()
    return {"research": out}


def writer_node(state: CapstoneState) -> dict:
    model = get_chat_model()
    out = model.invoke([
        SystemMessage(content="基于资料写一段通顺的中文介绍（不超过 100 字）。"),
        HumanMessage(content=f"资料：\n{state['research']}"),
    ]).content.strip()
    return {"draft": out}


def reviewer_node(state: CapstoneState) -> dict:
    model = get_chat_model()
    out = model.invoke([
        SystemMessage(content="审校草稿，给出 1 条改进建议（一句话）。"),
        HumanMessage(content=f"草稿：\n{state['draft']}"),
    ]).content.strip()
    return {"review": out}


def approval_node(state: CapstoneState) -> dict:
    # Phase 7 HITL：暂停，等人类审批
    decision = interrupt({"draft": state["draft"], "prompt": "批准发布？(yes/no)"})
    return {"approved": str(decision).strip().lower() in ("yes", "y", "true", "是")}


def publish_node(state: CapstoneState) -> dict:
    return {"final": "✅ 已发布：" + state["draft"]}


def revise_node(state: CapstoneState) -> dict:
    return {"final": "🔁 已打回，请基于审校意见修改：" + state["review"]}


def route_from_coordinator(state: CapstoneState) -> str:
    return state["route"]


def route_from_approval(state: CapstoneState) -> str:
    return "publish" if state["approved"] else "revise"


# ---------------------------------------------------------------------------
# 组装图
# ---------------------------------------------------------------------------
def build_capstone_graph():
    builder = StateGraph(CapstoneState)
    builder.add_node("coordinator", coordinator)
    builder.add_node("research", research_node)
    builder.add_node("math", math_node)
    builder.add_node("writer", writer_node)
    builder.add_node("reviewer", reviewer_node)
    builder.add_node("approval", approval_node)
    builder.add_node("publish", publish_node)
    builder.add_node("revise", revise_node)

    builder.add_edge(START, "coordinator")
    builder.add_conditional_edges(
        "coordinator", route_from_coordinator, {"research": "research", "math": "math"}
    )
    builder.add_edge("research", "writer")
    builder.add_edge("math", "writer")
    builder.add_edge("writer", "reviewer")
    builder.add_edge("reviewer", "approval")
    builder.add_conditional_edges(
        "approval", route_from_approval, {"publish": "publish", "revise": "revise"}
    )
    builder.add_edge("revise", "reviewer")   # 打回后回到审校，形成闭环
    builder.add_edge("publish", END)
    return builder.compile(checkpointer=MemorySaver())


def run_capstone(question: str, human_says: str = "yes"):
    graph = build_capstone_graph()
    config = {"configurable": {"thread_id": "capstone-1"}}
    graph.invoke({"question": question}, config)
    result = graph.invoke(Command(resume=human_says), config)
    print("最终结果：", result["final"])
    return result


if __name__ == "__main__":
    run_capstone("请查证并介绍 LangGraph 是什么。", human_says="yes")
