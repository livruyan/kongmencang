# LangGraph 状态机 + checkpoint 白板稿

> 面试素材 / 白板准备。对应改进报告「准备 LangGraph 状态机 + checkpoint 白板稿」。
> 白板时按本稿顺序画即可。

## 1. 最小状态图（边画边讲）

```
   START
     │
     ▼
 [research]  ──节点：调用 LLM 产出要点──► 写入 state["research"]
     │
     ▼
  [gate]     ──节点：interrupt 暂停，等人工 approve──►
     │                                                          │
     ▼ (resume="yes")                                          │
 [summarize]  ──节点：基于要点写总结──► 写入 state["summary"]    │
     │                                                          │
     ▼                                                          │
    END ───────────────────────────────────────────────────────┘
```

- **StateGraph**：用 TypedDict 定义全局状态（本例 `topic / research / summary`）。
- **节点（Node）**：一个纯函数 `(state) -> 部分更新`，框架负责把返回值 merge 回状态。
- **条件边（Conditional Edge）**：用函数根据状态决定走哪条边（本例 `gate` 之后可加
  `router`：`if approved -> summarize else -> END`），这是「同一张图」能表达
  ReAct / Plan-Execute / 辩论 的根本原因。

## 2. checkpoint 怎么持久化、怎么恢复（必问）

- **checkpointer** 在 `compile(checkpointer=MemorySaver())` 时注入。
- 每次 `invoke` 都带 `config={"configurable": {"thread_id": "x"}}`，
  **thread_id 就是状态的坐标**。
- 框架把每一步后的完整状态写入后端（内存 / SQLite / Postgres）。
- **恢复**：`graph.get_state(config)` 读回最新状态；
  `graph.invoke(Command(resume=...), config)` 从最近检查点续跑——
  进程重启、用户离开再回来都不丢进度。

## 3. HITL 怎么实现（必问）

- `from langgraph.types import interrupt`
- 在 `gate` 节点里 `interrupt({"research": ..., "prompt": "继续？"})`：
  执行到此**暂停并把控制权交回调用方**，状态已被持久化。
- 调用方拿到结果后，用 `Command(resume="yes"/"no")` 把决定送回，图从断点继续。
- 落点：人工审批、敏感操作确认、外部系统回执，都在 interrupt 处。

## 4. Memory vs RAG（必问）

- **Memory** = 对话 / 任务状态的**快照或可溯源记忆**（本项目用独立记忆层 + checkpoint）。
- **RAG** = 从外部知识库**检索**喂给模型，解决「不知道」的问题。
- 区别：Memory 是「我记得刚才发生了什么」，RAG 是「我去查一下资料」。
- 本项目的防幻觉设计：semantic 记忆每条带 `source_ref`，无来源则不允许模型断言。

## 5. 与自研内核（灵犀）的区别（必问）

- LangGraph = 用框架：状态图、调度、持久化开箱即用，快速落地。
- 灵犀 = 自研内核：双脑协同 + 反思循环 + 权重演化，自己实现运行时。
- 一句话：框架让你交付快，自研让你懂底层；两者互补。
