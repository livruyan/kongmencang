"""Phase 7 · 时间旅行 / Time travel.

利用 checkpoint，可以列出历史状态点、回放到其中任意一个并从此分叉。这是调试
多步 Agent 的利器——不必每次都从头重跑。
With checkpoints you can list past states, replay any of them and fork from
there. A debugging superpower for multi-step Agents — no need to re-run from
scratch every time.
"""
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from examples.common.llm import get_chat_model


class State(TypedDict):
    messages: Annotated[list, add_messages]


def bot(state: State):
    return {"messages": [get_chat_model().invoke(state["messages"])]}


def build():
    g = StateGraph(State)
    g.add_node("bot", bot)
    g.add_edge(START, "bot")
    g.add_edge("bot", END)
    return g.compile(checkpointer=MemorySaver())


def main():
    app = build()
    cfg = {"configurable": {"thread_id": "t1"}}
    app.invoke({"messages": [("user", "你好")]}, cfg)

    states = list(app.get_state_history(cfg))
    print(f"共 {len(states)} 个历史状态点")
    target = states[-1].config
    out = app.invoke({"messages": [("user", "换个说法再问一遍")]}, target)
    print(out["messages"][-1].content)


if __name__ == "__main__":
    main()
