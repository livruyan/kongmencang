"""Phase 1 · 第一个 Chain / The first Chain.

演示 LangChain 的 Model I/O 三件套：PromptTemplate -> ChatModel -> 输出。
Demonstrates the Model I/O triad: PromptTemplate -> ChatModel -> output.

运行 / Run:
    python -m examples.p1.hello_chain
"""
import os
import sys
from pathlib import Path

# 让示例在任意工作目录都能 import examples 包
# Make `examples` importable regardless of current working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langchain_core.prompts import ChatPromptTemplate

from examples.common.llm import get_chat_model


def main() -> None:
    model = get_chat_model()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个乐于助人的助手，用一句话回答。"),
            ("user", "用一句话解释什么是 {concept}。"),
        ]
    )
    chain = prompt | model
    response = chain.invoke({"concept": "状态图（StateGraph）"})
    print(response.content)


if __name__ == "__main__":
    main()
