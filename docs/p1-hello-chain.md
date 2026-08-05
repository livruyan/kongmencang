# Phase 1 · 第一个 Chain

本章用最小代码跑通一个 LangChain 应用，建立 **Model I/O 三件套**的心智模型。

## Model I/O 三件套 / The Model I/O Triad

```
PromptTemplate  ──▶  ChatModel  ──▶  Output
   (输入模板)          (大模型)        (模型回复)
```

- **PromptTemplate**：把变量填进固定的提示词模板，生成发给模型的消息。
- **ChatModel**：真正调用大模型（通过 `examples/common/llm.py` 抽象，可切换 OpenAI / DeepSeek / Ollama）。
- **Output**：模型返回的内容（`response.content`）。

## 代码走读 / Code Walkthrough

`examples/p1/hello_chain.py`：

```python
from langchain_core.prompts import ChatPromptTemplate
from examples.common.llm import get_chat_model

def main() -> None:
    model = get_chat_model()                       # 取模型（按 .env 切换）
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个乐于助人的助手，用一句话回答。"),
        ("user", "用一句话解释什么是 {concept}。"),
    ])
    chain = prompt | model                         # 用管道符组合
    response = chain.invoke({"concept": "状态图（StateGraph）"})
    print(response.content)
```

关键点：
- `prompt | model` 是 LangChain 的 **LCEL 管道语法**，把两步串成一个可执行单元。
- `{concept}` 是模板变量，由 `invoke({"concept": ...})` 注入。

## 运行 / Run

```bash
# 确保已激活虚拟环境并装好依赖、配置 .env
python -m examples.p1.hello_chain
```

预期输出（示例）：
```
状态图（StateGraph）是 LangGraph 中用节点和边描述 Agent 执行流程的一种结构。
```

## 小结 / Takeaway

你已经跑通了第一个 Chain。记住这条主线：**提示词模板 → 模型 → 输出**，后面所有可能的复杂 Agent，都是在这条主线上不断加「节点」和「边」。

下一章（Phase 2）我们将学习如何把多个 Chain 组合、加入记忆与检索。

## 扩展示例 / Extra Example {#extra-p1}

### 流式输出（examples/p1/streaming.py）
演示非流式与流式两种调用方式，让你直观看到「模型是一点一点吐字」的底层行为。

```bash
python -m examples.p1.streaming
```

