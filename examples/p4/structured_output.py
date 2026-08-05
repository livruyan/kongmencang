"""Phase 4 · 结构化输出 / Structured output.

模型不只是吐文本——它可以按 schema 返回结构化数据。底层本质是一次「强制工具调用」。
Models can return data conforming to a schema; under the hood it's a forced
tool-call. Useful for piping Agent output into downstream code.

注意：DeepSeek 的 deepseek-chat 不支持 JSON-schema 形式的 response_format，
直接 `with_structured_output(Person)` 会返回 400。
因此这里显式指定 method="function_calling"，走 function-calling 路径
（DeepSeek 支持），既能拿到结构化对象，又避免报错。
"""
from typing import Optional

from pydantic import BaseModel, Field

from examples.common.llm import get_chat_model


class Person(BaseModel):
    name: str = Field(description="姓名")
    age: Optional[int] = Field(default=None, description="年龄")
    skills: list[str] = Field(description="技能列表")


def main():
    llm = get_chat_model()
    # 用 function_calling 方式拿到结构化输出，兼容 DeepSeek
    structured = llm.with_structured_output(Person, method="function_calling")
    result = structured.invoke(
        "介绍一位叫小明、会 Python 和写作的 25 岁工程师。"
    )
    print(result)


if __name__ == "__main__":
    main()
