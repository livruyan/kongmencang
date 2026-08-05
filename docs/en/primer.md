# Phase 1 · Python / Environment Primer (Skippable)

> If you already know Python and the basics of LLM APIs, you can skip this chapter and return when needed.

## 1. Python Crash Course / Python 速补

### Variables & functions
```python
name = "LangGraph"
count = 3
items = [1, 2, 3]

def greet(concept: str) -> str:
    return f"Hello, {concept}!"

print(greet("StateGraph"))
```

### Classes & imports
```python
from dataclasses import dataclass

@dataclass
class Node:
    name: str
    next: str | None = None
```

### Packages & modules
- A directory with `__init__.py` is a **package** and can be imported.
- All examples live under the `examples/` package and import the model via `examples.common.llm`.

## 2. Environment Setup / 环境搭建

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then edit .env to choose LLM_PROVIDER
```

## 3. LLM API Primer / LLM API 速览

- **Token**: the smallest unit a model processes (roughly a piece of a word). Usage is billed per token.
- **Chat Completion**: send the model a set of messages (`system` sets the role, `user` is input); it returns a reply.
- **API key safety**: never hard-code keys or commit them to Git. Put them in `.env` (git-ignored) and read at runtime.

```python
chain = prompt | model           # the most common LangChain shape
result = chain.invoke({"concept": "StateGraph"})
```

Next: [Write your first Chain →](/en/p1-hello-chain)
