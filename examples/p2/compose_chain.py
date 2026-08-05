"""Phase 2 · 组合链：顺序与并行 / Composition: Sequential & Parallel.

演示 LCEL 的两种基础组合方式：
  - 顺序（sequential）：一个链的输出作为下一个链的输入
  - 并行（parallel）：同一输入同时送入多个链
Demonstrates two basic LCEL compositions: sequential and parallel.

运行 / Run:
    python -m examples.p2.compose_chain
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel

from examples.common.llm import get_chat_model


def main() -> None:
    model = get_chat_model()

    # 顺序链：生成中文介绍 -> 翻译成英文
    gen_prompt = ChatPromptTemplate.from_template("用一句话介绍 {topic}（中文）。")
    trans_prompt = ChatPromptTemplate.from_template("把下面内容翻译成英文：\n{text}")
    gen_chain = gen_prompt | model | StrOutputParser()
    trans_chain = trans_prompt | model | StrOutputParser()

    sequential = gen_chain | trans_chain
    print("顺序链 / sequential:")
    print(" ", sequential.invoke({"topic": "状态图 StateGraph"}))

    # 并行链：同一输入同时产出中英文
    zh_chain = ChatPromptTemplate.from_template(
        "用一句话介绍 {topic}（中文）。"
    ) | model | StrOutputParser()
    en_chain = ChatPromptTemplate.from_template(
        "Explain {topic} in one sentence (English)."
    ) | model | StrOutputParser()

    parallel = RunnableParallel(zh=zh_chain, en=en_chain)
    print("并行链 / parallel:")
    print(" ", parallel.invoke({"topic": "LangGraph"}))


if __name__ == "__main__":
    main()
