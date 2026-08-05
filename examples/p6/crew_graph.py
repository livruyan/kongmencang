"""
Phase 6 · 示例 1：用 LangGraph 把「研究员 → 写手 → 审校」表达为一张显式图
====================================================================================
目的：把 Phase 5 里手写的 crew 流水线，用 LangGraph 的 StateGraph 重新表达。
你会发现——
  - 每个角色是一个 **节点（node）**
  - 角色之间的串联是 **边（edge）**
  - 在节点之间流动的数据，是图的 **状态（State）**

这就是「范式统一论」的闭环：CrewAI 的 crew，用 LangGraph 不过是一张线性图。
"""

from typing import TypedDict

from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END

from examples.common.llm import get_chat_model


# ---------------------------------------------------------------------------
# 1) 定义「共享状态」：所有节点读写同一份 State
# ---------------------------------------------------------------------------
class CrewState(TypedDict):
    topic: str
    research: str
    draft: str
    review: str


# ---------------------------------------------------------------------------
# 2) 定义节点：每个节点是一个函数，入参是 State，返回要「写入」State 的字段
# ---------------------------------------------------------------------------
def researcher(state: CrewState) -> dict:
    model = get_chat_model()
    out = model.invoke([
        SystemMessage(content="你是严谨的研究员，给定主题只输出 3 条关键要点，每条一行。"),
        HumanMessage(content=f"主题：{state['topic']}"),
    ]).content.strip()
    return {"research": out}


def writer(state: CrewState) -> dict:
    model = get_chat_model()
    out = model.invoke([
        SystemMessage(content="你是技术写手，基于要点写一段通俗中文介绍（不超过 120 字）。"),
        HumanMessage(content=f"要点：\n{state['research']}"),
    ]).content.strip()
    return {"draft": out}


def reviewer(state: CrewState) -> dict:
    model = get_chat_model()
    out = model.invoke([
        SystemMessage(content="你是审校，基于草稿给出 2 条可执行改进建议，每条一行。"),
        HumanMessage(content=f"草稿：\n{state['draft']}"),
    ]).content.strip()
    return {"review": out}


# ---------------------------------------------------------------------------
# 3) 组装图：加节点、加边（START -> researcher -> writer -> reviewer -> END）
# ---------------------------------------------------------------------------
def build_graph():
    builder = StateGraph(CrewState)
    builder.add_node("researcher", researcher)
    builder.add_node("writer", writer)
    builder.add_node("reviewer", reviewer)

    builder.add_edge(START, "researcher")
    builder.add_edge("researcher", "writer")
    builder.add_edge("writer", "reviewer")
    builder.add_edge("reviewer", END)
    return builder.compile()


def run_graph(topic: str):
    graph = build_graph()
    result = graph.invoke({"topic": topic})
    print("# 主题：", topic)
    print("\n【research】\n" + result["research"])
    print("\n【draft】\n" + result["draft"])
    print("\n【review】\n" + result["review"])
    return result


if __name__ == "__main__":
    run_graph("为什么大多数 Agent 框架都能映射到状态图？")
