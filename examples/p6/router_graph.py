"""
Phase 6 · 示例 2：用条件边实现协调者路由（对应 AutoGen 的 group-chat）
=========================================================================
目的：把 Phase 5 里「协调者决定下一个专家」的逻辑，用 LangGraph 的
add_conditional_edges 显式表达。

- 一个 coordinator 节点负责「判断该派给谁」；
- add_conditional_edges 根据 coordinator 写入 State 的 route 字段，
  把控制流导向 math / language / code 节点之一。

这就是 AutoGen「协调者决定谁发言」在 LangGraph 里的标准形式：
一个 **条件边（conditional edge）**。
"""

from typing import TypedDict

from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END

from examples.common.llm import get_chat_model

EXPERT_SYS = {
    "math": "你是数学专家，只回答数学计算/推理，简洁给出答案。",
    "language": "你是语言专家，只回答翻译/语法/用词，简洁给出答案。",
    "code": "你是编程专家，只回答代码相关，给出简明解释。",
}


class RouterState(TypedDict):
    question: str
    route: str      # coordinator 写入：math / language / code
    answer: str     # 被选中的专家写入


def coordinator(state: RouterState) -> dict:
    model = get_chat_model()
    choice = model.invoke([
        SystemMessage(content="你是协调者。给定请求，只回复一个词：math / language / code。"),
        HumanMessage(content=state["question"]),
    ]).content.strip().lower()
    return {"route": choice if choice in EXPERT_SYS else "code"}


def make_expert_node(key: str):
    def node(state: RouterState) -> dict:
        model = get_chat_model()
        out = model.invoke([
            SystemMessage(content=EXPERT_SYS[key]),
            HumanMessage(content=state["question"]),
        ]).content.strip()
        return {"answer": out}
    return node


def route_by_state(state: RouterState) -> str:
    return state["route"]


def build_graph():
    builder = StateGraph(RouterState)
    builder.add_node("coordinator", coordinator)
    builder.add_node("math", make_expert_node("math"))
    builder.add_node("language", make_expert_node("language"))
    builder.add_node("code", make_expert_node("code"))

    builder.add_edge(START, "coordinator")
    # 条件边：根据 state["route"] 分流到不同专家节点
    builder.add_conditional_edges(
        "coordinator",
        route_by_state,
        {"math": "math", "language": "language", "code": "code"},
    )
    # 所有专家节点结束后都连到 END
    builder.add_edge("math", END)
    builder.add_edge("language", END)
    builder.add_edge("code", END)
    return builder.compile()


def run_router(question: str):
    graph = build_graph()
    result = graph.invoke({"question": question})
    print(f"# 请求：{question}")
    print(f"# 路由：{result['route']}")
    print(f"# 回答：{result['answer']}\n")
    return result


if __name__ == "__main__":
    run_router("请把 'state graph' 翻译成中文。")
    run_router("求 1 到 100 的和。")
