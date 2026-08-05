"""
Phase 7 · 示例 1：人工介入（Human-in-the-loop）——审批节点
================================================================
目的：演示生产级 Agent 必备的能力——在关键决策点「暂停，等人类拍板」。
LangGraph 用 interrupt() 让图在执行中停下来，把控制权交还给人，
人给完指令后，用 Command(resume=...) 让图从断点继续。

场景：Agent 先起草，然后**暂停等人类审批**；人类说 yes 才「发布」，
说 no 则「打回修改」。审批这个分支，就是一条**条件边**，只不过
它的「决策权」在人类手里。

要点：
  - compile(checkpointer=MemorySaver())：必须有 checkpointer 才能中断/恢复
  - interrupt(payload)：在节点内暂停，把 payload 交给外部
  - graph.invoke(Command(resume=value), config)：从断点恢复
"""

from typing import TypedDict

from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt

from examples.common.llm import get_chat_model


class ApprovalState(TypedDict):
    topic: str
    draft: str
    approved: bool
    final: str


def draft_node(state: ApprovalState) -> dict:
    model = get_chat_model()
    out = model.invoke([
        SystemMessage(content="你是写手，就给定主题写一句简短说明（不超过 40 字）。"),
        HumanMessage(content=f"主题：{state['topic']}"),
    ]).content.strip()
    return {"draft": out}


def approval_node(state: ApprovalState) -> dict:
    # 暂停，把草稿交给人类，等人类回复 yes/no
    human_input = interrupt({"draft": state["draft"], "prompt": "是否批准发布？(yes/no)"})
    decision = str(human_input).strip().lower()
    return {"approved": decision in ("yes", "y", "true", "是")}


def publish_node(state: ApprovalState) -> dict:
    return {"final": "✅ 已发布：" + state["draft"]}


def revise_node(state: ApprovalState) -> dict:
    return {"final": "🔁 已打回修改（草稿：" + state["draft"] + "）"}


def route_after_approval(state: ApprovalState) -> str:
    return "publish" if state["approved"] else "revise"


def build_graph():
    builder = StateGraph(ApprovalState)
    builder.add_node("draft", draft_node)
    builder.add_node("approval", approval_node)
    builder.add_node("publish", publish_node)
    builder.add_node("revise", revise_node)
    builder.add_edge(START, "draft")
    builder.add_edge("draft", "approval")
    builder.add_conditional_edges(
        "approval", route_after_approval, {"publish": "publish", "revise": "revise"}
    )
    builder.add_edge("publish", END)
    builder.add_edge("revise", END)
    return builder.compile(checkpointer=MemorySaver())


def run_with_human(topic: str, human_says: str):
    graph = build_graph()
    config = {"configurable": {"thread_id": "demo-1"}}

    # 第一次调用：跑到 approval 节点的 interrupt 处暂停
    graph.invoke({"topic": topic}, config)
    print("（图已暂停，等待人类审批）")

    # 人类给出决定，从断点恢复
    result = graph.invoke(Command(resume=human_says), config)
    print("最终结果：", result["final"])
    return result


if __name__ == "__main__":
    run_with_human("用一句话介绍 LangGraph", "yes")
