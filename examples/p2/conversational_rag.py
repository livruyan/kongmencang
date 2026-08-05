"""Phase 2 · 带记忆的 RAG / Conversational RAG.

把检索（RAG）与多轮记忆（Memory）组合：用户第二问能基于第一问的上下文继续。
Combines retrieval (RAG) with multi-turn memory (Memory): the 2nd question
keeps context from the 1st.
"""
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from examples.common.llm import get_chat_model, get_embeddings

store: dict[str, BaseChatMessageHistory] = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    return store.setdefault(session_id, ChatMessageHistory())


def build_chain():
    texts = [
        "LangChain 是一个用于构建 LLM 应用的框架。",
        "RAG 通过检索外部知识来增强生成，减少幻觉。",
    ]
    vectordb = FAISS.from_texts(texts, get_embeddings())
    retriever = vectordb.as_retriever()
    llm = get_chat_model()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "根据上下文回答用户问题。\n上下文：\n{context}"),
        ("human", "{question}"),
    ])

    def format_docs(docs):
        return "\n".join(d.page_content for d in docs)

    rag = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
    )
    return RunnableWithMessageHistory(
        rag, get_session_history, input_messages_key="question"
    )


def main():
    chain = build_chain()
    cfg = {"configurable": {"session_id": "demo"}}
    print(chain.invoke({"question": "LangChain 是什么？"}, config=cfg).content)
    print(chain.invoke({"question": "那 RAG 呢？"}, config=cfg).content)


if __name__ == "__main__":
    main()
