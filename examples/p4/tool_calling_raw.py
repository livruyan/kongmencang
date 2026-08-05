"""
Phase 4 · 示例 2：揭开 tool-calling 的底层机制（model.bind_tools + 解析 tool_calls）
====================================================================================
目的：示例 1 用框架把「工具调用」封装好了，但你看不到内部。这里直接演示
「模型如何返回结构化的工具调用意图」，以及「我们如何据此真正去执行工具」。

这正是 Phase 3 那个手动 ReAct 循环的「现代版」——只不过这次模型原生支持
输出结构化的 tool_calls，省掉了手写的字符串解析。

铺垫：把「模型选出要调用的工具」视为一个**节点**，把「执行工具」视为下一个**节点**，
二者之间的跳转由 model 的 tool_calls 决定——这又是一个「条件边 + 节点」的图结构。

注：DeepSeek 对并行 tool_calls 的校验较严格，这里用 parallel_tool_calls=False
让模型一次只选一个工具，循环处理，既规避 400 报错，教学上也更清晰。
"""

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from pydantic import BaseModel, Field

from examples.common.llm import get_chat_model


# 用 Pydantic 声明工具，bind_tools 会据此生成给模型的工具描述
class AddInput(BaseModel):
    a: int = Field(description="第一个整数")
    b: int = Field(description="第二个整数")


class WeatherInput(BaseModel):
    city: str = Field(description="城市名称")


def add(a: int, b: int) -> int:
    return a + b


def fake_weather(city: str) -> str:
    return f"{city} 晴朗，演示数据。"


# 把「函数实现」和 schema 对应起来，方便按名字分发执行
TOOL_IMPL = {
    "add": lambda a, b: add(a, b),
    "get_weather": lambda city: fake_weather(city),
}


def run_raw_tool_calling(question: str):
    model = get_chat_model()

    # 把工具「绑定」到模型上；parallel_tool_calls=False 让模型一次只选一个工具，
    # 避免 DeepSeek 在并行 tool_calls 下的 400 校验问题（教学上也更清晰）。
    model_with_tools = model.bind_tools(
        [
            {"name": "add", "description": "两个整数相加", "args_schema": AddInput},
            {"name": "get_weather", "description": "查询城市天气", "args_schema": WeatherInput},
        ],
        parallel_tool_calls=False,
    )

    messages = [HumanMessage(content=question)]

    # 底层「思考 → 行动 → 观察」循环：只要模型还想调用工具就继续
    max_iter = 3
    for _ in range(max_iter):
        ai_msg: AIMessage = model_with_tools.invoke(messages)
        # 把模型这条「带 tool_calls 的回复」也塞回历史，作为后续上下文
        messages.append(ai_msg)
        print("模型返回的 tool_calls：", ai_msg.tool_calls)

        if not ai_msg.tool_calls:
            # 模型不再要求调用工具 → 综合给出最终答案
            final = ai_msg
            break

        # 逐个执行模型「想调用」的工具，并把结果以 ToolMessage 回填
        for call in ai_msg.tool_calls:
            name = call["name"]
            args = call["args"]
            if name in TOOL_IMPL:
                output = TOOL_IMPL[name](**args)
                messages.append(
                    ToolMessage(content=str(output), tool_call_id=call["id"])
                )
                print(f"执行工具 {name}({args}) -> {output}")
    else:
        # 达到最大轮数仍未收敛：取最后一条消息兜底
        final = messages[-1]

    print("\n===== 最终答案 =====")
    print(final.content)
    return final.content


if __name__ == "__main__":
    run_raw_tool_calling("帮我算一下 15 加 27，再告诉我上海的天气。")
