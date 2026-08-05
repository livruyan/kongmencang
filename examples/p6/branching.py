"""Phase 6 · 条件分支图 / Conditional branching graph.

用 add_conditional_edges 根据内容把请求路由到不同节点——这正是 AutoGen 协调者
路由的「图」表达。对比 p5/agent_router.py，这里把它显式画成图。
Route a request to different nodes via add_conditional_edges — the graph form of
AutoGen's coordinator routing. Compared with p5/agent_router.py, here it's an
explicit graph.
"""
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from examples.common.llm import get_chat_model


class State(TypedDict):
    messages: Annotated[list, add_messages]
    kind: str


def classify(state: State):
    llm = get_chat_model()
    r = llm.invoke(f"只回答 'code' 或 'chat'：{state['messages'][-1].content}")
    return {"kind": r.content.strip().lower()}


def code_node(state: State):
    return {"messages": [("ai", "进入代码处理分支。")]}


def chat_node(state: State):
    return {"messages": [("ai", "进入闲聊分支。")]}


def route(state: State):
    return "code" if "code" in state["kind"] else "chat"


def build():
    g = StateGraph(State)
    g.add_node("classify", classify)
    g.add_node("code", code_node)
    g.add_node("chat", chat_node)
    g.set_entry_point("classify")
    g.add_conditional_edges("classify", route, {"code": "code", "chat": "chat"})
    g.add_edge("code", END)
    g.add_edge("chat", END)
    return g.compile()


def main():
    app = build()
    result = app.invoke({"messages": [("user", "帮我写个排序函数")], "kind": ""})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
