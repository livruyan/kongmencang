# Phase 1 · The First Chain

In this chapter we run the smallest possible LangChain app and build the mental model of the **Model I/O triad**.

## The Model I/O Triad / Model I/O 三件套

```
PromptTemplate  ──▶  ChatModel  ──▶  Output
   (input tmpl)        (LLM)          (reply)
```

- **PromptTemplate**: fills variables into a fixed prompt template to produce messages.
- **ChatModel**: actually calls the LLM (via `examples/common/llm.py`, switchable between OpenAI / DeepSeek / Ollama).
- **Output**: the model's reply (`response.content`).

## Code Walkthrough / 代码走读

`examples/p1/hello_chain.py`:

```python
from langchain_core.prompts import ChatPromptTemplate
from examples.common.llm import get_chat_model

def main() -> None:
    model = get_chat_model()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Answer in one sentence."),
        ("user", "Explain what {concept} is in one sentence."),
    ])
    chain = prompt | model
    response = chain.invoke({"concept": "StateGraph"})
    print(response.content)
```

Key points:
- `prompt | model` is LangChain's **LCEL pipe syntax**, composing two steps into one runnable unit.
- `{concept}` is a template variable injected by `invoke({"concept": ...})`.

## Run / 运行

```bash
python -m examples.p1.hello_chain
```

Expected output (example):
```
A StateGraph is a LangGraph structure that describes an Agent's execution flow using nodes and edges.
```

## Takeaway / 小结

You have run your first Chain. Remember the main line: **prompt template → model → output**. Every complex Agent later is just more "nodes" and "edges" built on top of it.

Next (Phase 2): combine multiple chains and add memory & retrieval.

## Extra Example {#extra-p1}

### Streaming (examples/p1/streaming.py)
Shows both one-shot and streaming calls so you can see the model emit tokens token-by-token.

```bash
python -m examples.p1.streaming
```

