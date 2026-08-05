# Phase 2 · 组合链、记忆与 RAG

上一章你跑通了单个 Chain。本章把它「拼起来」：用 LCEL 组合多个步骤、让模型拥有记忆、并用检索增强（RAG）引入外部知识。

## 1. 组合链 / Composing Chains

LCEL 用管道符 `|` 串接可运行单元（Runnable）。两种最常见模式：

- **顺序（Sequential）**：`A | B`，A 的输出成为 B 的输入。
- **并行（Parallel）**：`RunnableParallel({...})`，同一输入同时送进多个分支。

见 `examples/p2/compose_chain.py`：

```python
gen_chain = gen_prompt | model | StrOutputParser()      # 生成中文
trans_chain = trans_prompt | model | StrOutputParser()   # 翻译
sequential = gen_chain | trans_chain                     # 顺序
parallel = RunnableParallel(zh=zh_chain, en=en_chain)    # 并行
```

> 路由（Routing）是第三种：根据输入/状态把请求导向不同链，这正是 Phase 6 LangGraph「条件边」的雏形。

## 2. 记忆 / Memory

多轮对话需要「记住」历史。现代做法是用 `RunnableWithMessageHistory`：

```python
chain = RunnableWithMessageHistory(
    prompt | model,
    get_history,                      # 按 session_id 取历史
    input_messages_key="input",
    history_messages_key="history",
)
chain.invoke({"input": "我叫小明。"}, {"configurable": {"session_id": "u1"}})
```

见 `examples/p2/memory_chat.py`。记忆是后续多轮 Agent 与 Human-in-the-loop 的基础。

## 3. RAG 基础 / Retrieval-Augmented Generation

RAG 让模型回答「它没背过」的知识：先把文档切块嵌入成向量，运行时按问题检索最相关片段，再交给模型生成答案。

最小闭环（`examples/p2/simple_rag.py`）：

```python
vectorstore = FAISS.from_texts(knowledge, get_embeddings())
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
rag = (
    {"context": retriever | _format_docs, "question": RunnablePassthrough()}
    | prompt | model | StrOutputParser()
)
```

> 嵌入模型也走统一抽象层 `get_embeddings()`：OpenAI / DeepSeek 用其 embedding 接口，Ollama 用 `nomic-embed-text`（需 `ollama pull nomic-embed-text`）。

## 运行 / Run

```bash
python -m examples.p2.compose_chain
python -m examples.p2.memory_chat
python -m examples.p2.simple_rag
```

## 小结 / Takeaway

- **组合**让你把小单元拼成复杂流程；
- **记忆**让流程跨越多次调用保持上下文；
- **RAG** 让模型接入外部知识。

这三者仍是「节点 + 边」：每个链/检索都是节点，数据流动就是边。下一章（Phase 3）我们让模型**自己决定**下一步走哪条边——这就是 Agent。

→ 回到 [项目简介](/) · → 上一章 [第一个 Chain](/p1-hello-chain)

## 扩展示例 / Extra Example {#extra-p2}

### 带记忆的 RAG（examples/p2/conversational_rag.py）
把检索（RAG）与多轮记忆（Memory）组合：第二问能基于第一问的上下文继续追问。

```bash
python -m examples.p2.conversational_rag
```

