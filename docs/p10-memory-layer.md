# Phase 10 · 记忆独立层：episodic + semantic + 溯源（防幻觉）

> 对应改进报告 P0「记忆独立层」。源码：`examples/common/memory.py`、`examples/p10/hello_chain.py`。

## 为什么要做这一层

之前的「记忆」只是 checkpoint 的状态快照（`MemorySaver`），它是**任务级快照**，不是真正可沉淀、
可溯源的「知识」。生产级 Agent 需要：

- **短期情节记忆（episodic）**：一次会话里发生了什么，可回放；
- **长期语义记忆（semantic）**：从对话中提炼的「事实」，跨会话复用；
- **溯源（traceability）**：每条语义记忆都带来源，回答必须引用 —— 这是防幻觉的开关。

## 三层结构

```python
from examples.common.memory import MemoryStore

ms = MemoryStore()                       # :memory: 演示；生产传文件路径做持久化
eid = ms.add_episode("s1", "user", "我们决定用 LangGraph。")   # episodic
ms.add_semantic("编排框架选型为 LangGraph", f"episode:{eid}", "s1")  # semantic + 溯源
```

检索时带上引用：

```python
ctx = ms.build_citation_context("编排框架")   # 返回带 [来源] 的事实
# 若无来源，ctx == "" —— 调用方不应让模型断言，而应拒答
```

## 防幻觉机制

`build_citation_context` 检索不到来源时返回空串。把该串注入 prompt：
- 非空 → 模型**只能依据记忆回答并标注引用**；
- 空 → 模型**明确说「记忆中没有」**，不编造。

这就是把「记忆」从 RAG 附庸里解放出来、做成独立可溯源层的核心价值。

## 运行

```bash
make run p=10
# 或 python -m examples.p10.hello_chain
```

会演示：有来源的问题带引用回答、无来源的问题被护栏拦下、以及溯源明细。

## 小结

- 记忆 ≠ checkpoint 快照：checkpoint 是任务级状态，记忆独立层是**可沉淀、可溯源的知识**。
- 三层（episodic / semantic / traceability）让 Agent 能「引用来源」，这是防幻觉的硬开关。
- 把记忆做成独立层后，RAG 只负责检索，记忆负责「已知事实」，职责边界更清晰。
