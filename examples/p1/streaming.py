"""Phase 1 · 流式输出 / Streaming output.

演示如何以流式方式逐 token 接收模型返回，以及它和一次性返回的关系。
Demonstrates receiving model output token-by-token, and how it relates to a
single-shot response.
"""
from examples.common.llm import get_chat_model


def main():
    llm = get_chat_model(temperature=0.7)
    prompt = "用三句话介绍什么是大语言模型。"

    print("=== 非流式 / Non-streaming ===")
    print(llm.invoke(prompt).content)

    print("\n=== 流式 / Streaming ===")
    for chunk in llm.stream(prompt):
        if chunk.content:
            print(chunk.content, end="", flush=True)
    print()


if __name__ == "__main__":
    main()
