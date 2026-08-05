"""Phase 2 · 简单 RAG / A Minimal RAG Pipeline.

演示检索增强生成的最小闭环：把知识写入向量库 -> 按问题检索 -> 喂给模型回答。
Demonstrates the minimal RAG loop: embed knowledge -> retrieve by question -> answer.

运行 / Run:
    python -m examples.p2.simple_rag
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from examples.common.llm import get_chat_model, get_embeddings


def _format_docs(docs) -> str:
    return "\n".join(d.page_content for d in docs)


def main() -> None:
    embeddings = get_embeddings()
    knowledge = [
        "LangGraph 用 StateGraph 描述 Agent 的执行流程。",
        "节点（Node）是图中的一个计算步骤，例如调用一次模型。",
        "条件边（Conditional Edge）根据当前状态决定下一步走向哪个节点。",
    ]
    vectorstore = FAISS.from_texts(knowledge, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    model = get_chat_model()
    prompt = ChatPromptTemplate.from_template(
        "根据上下文回答问题。\n上下文：\n{context}\n问题：{question}"
    )

    rag = (
        {"context": retriever | _format_docs, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    print(rag.invoke("什么是条件边？"))


if __name__ == "__main__":
    main()
