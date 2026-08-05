"""Phase 2 · 带记忆的对话 / Conversational Memory.

演示如何用 RunnableWithMessageHistory 让模型「记住」上下文，
这是后续 Human-in-the-loop 与多轮 Agent 的基础。
Demonstrates memory via RunnableWithMessageHistory — the basis for
multi-turn Agents and human-in-the-loop later.

运行 / Run:
    python -m examples.p2.memory_chat
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory

from examples.common.llm import get_chat_model

# 简单的会话存储 / a trivial session store
store: dict = {}


def get_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


def main() -> None:
    model = get_chat_model()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个友好的助手。"),
            MessagesPlaceholder("history"),
            ("human", "{input}"),
        ]
    )
    chain = RunnableWithMessageHistory(
        prompt | model,
        get_history,
        input_messages_key="input",
        history_messages_key="history",
    )
    cfg = {"configurable": {"session_id": "user-1"}}

    r1 = chain.invoke({"input": "我叫小明，请记住我的名字。"}, cfg)
    print("模型:", r1.content)

    r2 = chain.invoke({"input": "我刚才说我的名字是什么？"}, cfg)
    print("模型:", r2.content)


if __name__ == "__main__":
    main()
