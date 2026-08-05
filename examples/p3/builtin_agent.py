"""
Phase 3 · 示例 2：用 LangGraph 原生 Agent 跑一个带工具的 Agent
=============================================================
目的：在理解了「手动 ReAct 循环」之后，直接用 LangGraph 封装好的原生 Agent
（create_react_agent）跑同样的活，体会「轮子」带来的便利，也看清框架替我们
做了哪些事（提示词、解析、循环）。

`create_react_agent` 是 1.x 时代官方推荐的原生 Agent 实现，
替代了已从 `langchain.agents` 移除的 `AgentExecutor`。
"""

from langchain_core.tools import tool
from langchain.agents import create_agent

from examples.common.llm import get_chat_model


@tool
def word_length(word: str) -> str:
    """返回单词的字母长度。输入一个单词，返回它的字母个数。"""
    return str(len(word.strip()))


@tool
def calculator(expression: str) -> str:
    """计算四则运算表达式，例如 '11 * 3 + 2'。"""
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:  # noqa
        return f"计算出错：{e}"


def run_agent(question: str):
    llm = get_chat_model()
    tools = [word_length, calculator]

    # LangGraph 原生 ReAct Agent：内置提示词 + 自动循环，
    # 把「思考 → 调用工具 → 观察」封装成一张状态图。
    agent = create_agent(llm, tools)
    result = agent.invoke({"messages": [("user", question)]})

    # 打印框架内部轨迹，看清它替我们做了什么
    print("===== 框架内部的「思考 → 行动 → 观察」轨迹 =====")
    for i, msg in enumerate(result["messages"], 1):
        print(f"[{i}] {getattr(msg, 'type', '?' )}: {getattr(msg, 'content', '')}")

    answer = result["messages"][-1].content
    print("\n===== 最终答案 =====")
    print(answer)
    return answer


if __name__ == "__main__":
    run_agent("请先计算 langgraph 这个单词有几个字母，再乘以 3。")
