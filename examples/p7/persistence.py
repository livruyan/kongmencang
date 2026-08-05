"""
Phase 7 · 示例 2：状态持久化与断点续跑（checkpoint）
================================================================
目的：演示 LangGraph 的「记忆」能力——图的执行状态会被 checkpointer
自动保存到外部存储（这里是内存 MemorySaver，生产可用 Sqlite/Postgres）。
即使进程重启、或中途暂停，也能从最近的检查点恢复，而不用从头跑。

这对生产级多 Agent 系统至关重要：
  - 长任务可分段执行、超时可续跑；
  - 用户关掉页面再回来，对话/进度还在；
  - 配合 HITL，人类离开后回来仍能接着审批。

本例：research 节点跑完后 interrupt 暂停 -> 我们用 get_state 查看
被持久化的状态 -> 再用 Command(resume) 续跑 summarize 节点，
证明状态确实被保存、未被丢弃。
"""

from typing import TypedDict

from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt

from examples.common.llm import get_chat_model


class PersistState(TypedDict):
    topic: str
    research: str
    summary: str


def research_node(state: PersistState) -> dict:
    model = get_chat_model()
    out = model.invoke([
        SystemMessage(content="你是研究员，给定主题输出 2 条要点，每条一行。"),
        HumanMessage(content=f"主题：{state['topic']}"),
    ]).content.strip()
    return {"research": out}


def gate_node(state: PersistState) -> dict:
    # 模拟「人工确认是否继续生成摘要」的暂停点
    _ = interrupt({"research": state["research"], "prompt": "继续生成摘要吗？(yes/no)"})
    return {}


def summarize_node(state: PersistState) -> dict:
    model = get_chat_model()
    out = model.invoke([
        SystemMessage(content="基于要点写一句总结。"),
        HumanMessage(content=f"要点：\n{state['research']}"),
    ]).content.strip()
    return {"summary": out}


def build_graph():
    builder = StateGraph(PersistState)
    builder.add_node("research", research_node)
    builder.add_node("gate", gate_node)
    builder.add_node("summarize", summarize_node)
    builder.add_edge(START, "research")
    builder.add_edge("research", "gate")
    builder.add_edge("gate", "summarize")
    builder.add_edge("summarize", END)
    return builder.compile(checkpointer=MemorySaver())


def run_persisted(topic: str):
    graph = build_graph()
    config = {"configurable": {"thread_id": "persist-demo"}}

    # 第一步：跑到 gate 的 interrupt 暂停
    graph.invoke({"topic": topic}, config)
    saved = graph.get_state(config)        # 查看被持久化的状态
    print("【暂停时持久化的 research 状态】\n" + saved.values["research"])

    # 第二步：从检查点恢复，续跑 summarize
    graph.invoke(Command(resume="yes"), config)
    final = graph.get_state(config)
    print("\n【续跑后最终状态】\n" + final.values["summary"])
    return final.values


if __name__ == "__main__":
    run_persisted("状态图相比普通循环有什么优势？")
