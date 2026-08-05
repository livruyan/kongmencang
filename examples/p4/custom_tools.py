"""
Phase 4 · 示例 1：把任意函数封装成 Agent 可用的工具（现代 tool-calling）
=========================================================================
目的：理解「工具」到底是什么——它就是一个带**清晰描述**和**明确参数结构**的函数。
Agent 的能力上限，几乎完全取决于你给了它哪些好用的工具。

要点：
  1. 用 @tool 装饰器把普通函数变成 Tool；
  2. 用 Pydantic 的 args_schema 声明参数类型，模型才能正确地「填表」；
  3. 工具描述（docstring）极其重要——模型靠它决定「该不该用、怎么用」这个工具；
  4. 用 LangGraph 原生 create_react_agent 跑一个会自己挑工具的 Agent。
"""

from langchain_core.tools import tool
from langchain.agents import create_agent
from pydantic import BaseModel, Field

from examples.common.llm import get_chat_model


# ---------------------------------------------------------------------------
# 1) 定义工具（带参数 schema + 清晰描述）
# ---------------------------------------------------------------------------
class WeatherInput(BaseModel):
    city: str = Field(description="城市名称，例如 '北京' 或 'Shanghai'")
    unit: str = Field(default="celsius", description="温度单位：celsius 或 fahrenheit")


@tool(args_schema=WeatherInput)
def get_weather(city: str, unit: str = "celsius") -> str:
    """查询指定城市的当前天气。当用户问天气时一定要用这个工具。"""
    # 这里用假数据演示；真实场景替换为天气 API 调用
    mock = {"北京": 22, "shanghai": 26, "上海": 26}
    temp = mock.get(city.lower(), 20)
    if unit == "fahrenheit":
        temp = round(temp * 9 / 5 + 32)
    return f"{city} 当前温度约 {temp}°{'F' if unit == 'fahrenheit' else 'C'}（演示数据）。"


@tool
def multiply(a: int, b: int) -> str:
    """计算两个整数的乘积。当用户需要乘法运算时使用。"""
    return str(a * b)


@tool
def reverse_text(text: str) -> str:
    """把给定文本反转。当用户要求反转、倒序字符串时使用。"""
    return text[::-1]


# ---------------------------------------------------------------------------
# 2) 组装 tool-calling Agent（LangGraph 原生）
# ---------------------------------------------------------------------------
def run_agent(question: str):
    llm = get_chat_model()
    tools = [get_weather, multiply, reverse_text]

    # LangGraph 原生 Agent：内置提示词 + 自动工具选择循环
    agent = create_agent(llm, tools)
    result = agent.invoke({"messages": [("user", question)]})

    # 打印框架内部轨迹，看清工具是如何被挑中并执行的
    print("===== 框架内部的「思考 → 行动 → 观察」轨迹 =====")
    for i, msg in enumerate(result["messages"], 1):
        extra = ""
        if getattr(msg, "tool_calls", None):
            extra = f"  tool_calls={msg.tool_calls}"
        print(f"[{i}] {getattr(msg, 'type', '?')}: {getattr(msg, 'content', '')}{extra}")

    answer = result["messages"][-1].content
    print("\n===== 最终答案 =====")
    print(answer)
    return answer


if __name__ == "__main__":
    run_agent("北京现在多少度？另外把 'langgraph' 倒过来写，并算一下 7 乘以 8。")
