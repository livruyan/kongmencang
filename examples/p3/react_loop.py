"""
Phase 3 · 示例 1：用 LangGraph 原生 Agent 重做「思考 → 行动 → 观察」循环
==========================================================================
目的：在 Phase 1 我们手写过一个最小 ReAct 循环，看清 Agent 的底层机理。
那时要自己写提示词、自己解析模型输出、自己管理 scratchpad，非常脆弱
（模型格式稍有不同就解析失败）。

这里用 LangGraph 官方推荐的**原生 Agent** `create_react_agent` 重做同一件事：
  - 框架替我们管理「思考 → 调用工具 → 观察」的循环；
  - 它底层仍是一张「状态 + 节点 + 条件边」的图（正是本课程的核心理念）；
  - 我们通过打印中间消息，看清框架在每一步替我们做了什么。

对比手写版本，你会直观感受到「轮子」的价值，也印证了课程主张：
主流 Agent 框架的底层，都是状态图 + 节点 + 条件边。
"""

from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langchain.agents import create_agent

from examples.common.llm import get_chat_model


@tool
def search(query: str) -> str:
    """根据关键词查询资料。输入一个关键词，返回对应的知识条目。"""
    knowledge = {
        "langgraph": "LangGraph 是 LangChain 团队推出的图编排框架，用「状态 + 节点 + 条件边」描述工作流。",
        "react": "ReAct = Reasoning + Acting，是一种让 LLM 交替进行推理与工具调用的范式。",
        "agent": "Agent 是能感知环境、自主决策并调用工具来完成目标的系统。",
    }
    return knowledge.get(query.strip().lower(), f"未找到关于「{query}」的资料。")


@tool
def calculator(expression: str) -> str:
    """一个安全的四则运算计算器，输入如 '3 + 5 * 2'。"""
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        return "表达式包含非法字符。"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:  # noqa
        return f"计算出错：{e}"


def _print_trace(messages):
    """把框架内部的「思考 → 行动 → 观察」轨迹打印出来，看清每一步。"""
    print("===== 框架内部的「思考 → 行动 → 观察」轨迹 =====")
    for i, msg in enumerate(messages, 1):
        if not isinstance(msg, BaseMessage):
            continue
        who = getattr(msg, "type", type(msg).__name__)
        content = getattr(msg, "content", "")
        extra = ""
        tool_calls = getattr(msg, "tool_calls", None)
        if tool_calls:
            extra = f"  tool_calls={tool_calls}"
        print(f"[{i}] {who}: {content}{extra}")


def run_react(question: str):
    llm = get_chat_model()
    tools = [search, calculator]

    # LangGraph 原生 ReAct Agent：内置提示词 + 自动循环
    agent = create_agent(llm, tools)
    result = agent.invoke({"messages": [("user", question)]})

    # 打印中间消息，看清框架替我们做了哪些事
    _print_trace(result["messages"])

    answer = result["messages"][-1].content
    print("\n===== 最终答案 =====")
    print(answer)
    return answer


if __name__ == "__main__":
    run_react("langgraph 这个词一共有几个字母？请先查资料确认拼写，再计算长度。")
