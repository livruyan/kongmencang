# Phase 7 · 人工介入与状态持久化：生产级多 Agent 的两块基石

> 目标：掌握让 Agent 从「玩具」走向「生产」的两个关键能力——**人工介入（HITL）** 与 **状态持久化**。这是 Phase 6 那张图真正能落地的保障。

## 为什么需要 HITL（Human-in-the-loop）

之前的图都是「全自动」的：模型一路跑到 END。但真实业务里，有些节点你**不敢**让它自动过：
- 给外界发邮件、扣款、删数据——错一次代价巨大；
- 法律/医疗/金融结论——必须有人兜底；
- 模型拿不准时——让人来定夺。

HITL 就是：在关键节点**暂停，把控制权交给人**，人确认后再继续。在图里，它本质上是一条「决策权在人类」的**条件边**。

## 用 interrupt 实现审批节点

```python
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

def approval_node(state):
    human_input = interrupt({"draft": state["draft"], "prompt": "是否批准？(yes/no)"})
    return {"approved": human_input.lower() == "yes"}

graph = builder.compile(checkpointer=MemorySaver())   # 必须带 checkpointer 才能中断
graph.invoke({"topic": "..."}, config)                 # 跑到 interrupt 暂停
graph.invoke(Command(resume="yes"), config)            # 人给完指令，从断点继续
```

示例文件：`examples/p7/hitl_approve.py` —— 起草 → **暂停等审批** →（yes）发布 /（no）打回修改。运行：

```bash
python -m examples.p7.hitl_approve
```

## 为什么需要持久化（checkpoint）

长任务（研究、生成、多步检索）动辄几十秒到几分钟。如果：
- 进程中途崩了 → 从头再来，浪费钱也浪费时间；
- 用户关掉页面 → 回来进度没了；
- 配合 HITL → 人离开几小时，回来还得接着审。

LangGraph 用 **checkpointer** 把图的执行状态自动存到外部（内存 / SQLite / Postgres）。`thread_id` 标识一条会话，同一个 `thread_id` 的调用共享同一份持久化状态。

## 用 MemorySaver 演示断点续跑

示例文件：`examples/p7/persistence.py`：

```python
graph = builder.compile(checkpointer=MemorySaver())
graph.invoke({"topic": "..."}, config)        # 跑到 gate 的 interrupt 暂停
saved = graph.get_state(config)               # 查看被持久化的状态
graph.invoke(Command(resume="yes"), config)   # 从检查点续跑
```

你会看到：暂停时 `research` 结果被原样保存，续跑时无需重算。换成 SqliteSaver/PostgresSaver 即可跨进程/跨机器持久化。

```bash
python -m examples.p7.persistence
```

## 这两者和「图」的关系

- HITL 的审批分支 = **条件边**，只是决策方从「模型」换成「人类」；
- 持久化 = 把 **State** 外置，让图可以「暂停—恢复」而状态不丢。

它们都证明了一件事：**用「状态图」建模，天然就比一堆 `for/if` 更适合生产**——因为状态、分支、暂停点都是一等公民。

## 验收清单

- [ ] 能说清 HITL 解决什么、哪些节点该加审批
- [ ] 能写出 interrupt + Command(resume) 的暂停/恢复骨架
- [ ] 能解释 checkpointer 与 thread_id 的作用
- [ ] 跑通过示例 1（审批）和示例 2（持久化续跑）

## 下一步

Phase 8–9：**生产部署实战**。把前面学的图、工具、HITL、持久化，封装成一个对外服务的系统——容器化、API 暴露、可观测（LangSmith/Langfuse）、以及与 CrewAI/AutoGen 方案的对照总结。

## 扩展示例 / Extra Example {#extra-p7}

### 时间旅行（examples/p7/time_travel.py）
利用 checkpoint 列出历史状态点、回放到任意状态并分叉——调试多步 Agent 的利器。

```bash
python -m examples.p7.time_travel
```

