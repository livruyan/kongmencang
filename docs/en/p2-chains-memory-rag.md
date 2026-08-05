# Phase 2 · Composition, Memory & RAG

Last chapter you ran a single Chain. Here we **compose** them: combine steps with LCEL, give the model memory, and augment it with retrieval (RAG).

## 1. Composing Chains / 组合链

LCEL connects runnables with the pipe `|`. Two common patterns:

- **Sequential**: `A | B` — the output of A becomes the input of B.
- **Parallel**: `RunnableParallel({...})` — the same input fans out to multiple branches.

See `examples/p2/compose_chain.py`:

```python
gen_chain = gen_prompt | model | StrOutputParser()      # generate (zh)
trans_chain = trans_prompt | model | StrOutputParser()   # translate
sequential = gen_chain | trans_chain                     # sequential
parallel = RunnableParallel(zh=zh_chain, en=en_chain)    # parallel
```

> **Routing** is the third pattern: direct the request to different chains based on input/state. This is the seed of LangGraph's "conditional edge" in Phase 6.

## 2. Memory / 记忆

Multi-turn chat needs to "remember" history. The modern approach is `RunnableWithMessageHistory`:

```python
chain = RunnableWithMessageHistory(
    prompt | model,
    get_history,                      # fetch history by session_id
    input_messages_key="input",
    history_messages_key="history",
)
chain.invoke({"input": "My name is Xiao Ming."}, {"configurable": {"session_id": "u1"}})
```

See `examples/p2/memory_chat.py`. Memory is the foundation for multi-turn Agents and human-in-the-loop later.

## 3. RAG Basics / RAG 基础

RAG lets the model answer questions about knowledge it was not trained on: embed documents into vectors, retrieve the most relevant chunks at query time, and feed them to the model.

Minimal loop (`examples/p2/simple_rag.py`):

```python
vectorstore = FAISS.from_texts(knowledge, get_embeddings())
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
rag = (
    {"context": retriever | _format_docs, "question": RunnablePassthrough()}
    | prompt | model | StrOutputParser()
)
```

> Embeddings also go through the unified `get_embeddings()` abstraction: OpenAI/DeepSeek use their embedding API, Ollama uses `nomic-embed-text` (run `ollama pull nomic-embed-text`).

## Run / 运行

```bash
python -m examples.p2.compose_chain
python -m examples.p2.memory_chat
python -m examples.p2.simple_rag
```

## Takeaway / 小结

- **Composition** lets you build complex flows from small units.
- **Memory** keeps context across calls.
- **RAG** connects the model to external knowledge.

All three are still "nodes + edges": each chain/retriever is a node, and data flow is the edge. Next chapter (Phase 3) we let the model **decide** which edge to take next — that is an Agent.

→ Back to [Introduction](/) · → Previous [The First Chain](/en/p1-hello-chain)

## Extra Example {#extra-p2}

### Conversational RAG (examples/p2/conversational_rag.py)
Combines retrieval (RAG) with multi-turn memory: the 2nd question keeps context from the 1st.

```bash
python -m examples.p2.conversational_rag
```

