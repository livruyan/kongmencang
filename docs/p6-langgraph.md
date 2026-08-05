# Phase 6 · LangGraph 图编排：范式统一论的闭环

> 目标：用 LangGraph 把前几章的所有案例「归一」表达。当你看到 CrewAI 的 crew、AutoGen 的群聊、单 Agent 循环，都能用同一套「状态图 + 节点 + 条件边」写出来时，本项目的核心主张就完成了闭环。

## LangGraph 三个核心概念

1. **State（状态）**：一张在节点之间流动的「共享白板」。用 `TypedDict` 或 Pydantic 定义。每个节点读它、写它。
2. **Node（节点）**：一个普通函数 `(state) -> 部分状态更新`。它可以是一次 LLM 调用、一个工具、一段逻辑。
3. **Edge（边）**：节点之间的连接。
   - **普通边**：固定顺序，如 `A → B`。
   - **条件边** `add_conditional_edges`：由一个函数读取状态、决定下一条边走向哪里——这正是「智能路由」的来源。

还有两个保留端点：`START`（入口）、`END`（出口）。

## 示例 1：把 Phase 5 的 crew 写成图

文件：`examples/p6/crew_graph.py`

回顾 Phase 5 我们手写的「研究员 → 写手 → 审校」流水线。用 LangGraph 重写后：

```python
builder = StateGraph(CrewState)
builder.add_node("researcher", researcher)
builder.add_node("writer", writer)
builder.add_node("reviewer", reviewer)
builder.add_edge(START, "researcher")
builder.add_edge("researcher", "writer")
builder.add_edge("writer", "reviewer")
builder.add_edge("reviewer", END)
graph = builder.compile()
```

看，CrewAI 的 crew = 一张**线性图**。框架不同，但「节点 + 边」的结构一模一样。

```bash
python -m examples.p6.crew_graph
```

## 示例 2：把「协调者路由」写成条件边

文件：`examples/p6/router_graph.py`

Phase 5 里「协调者决定下一个专家」的逻辑，用 `add_conditional_edges` 显式表达：

```python
builder.add_conditional_edges(
    "coordinator",
    route_by_state,                    # 读 state["route"] 决定走向
    {"math": "math", "language": "language", "code": "code"},
)
```

这正是 AutoGen「协调者决定谁发言」在 LangGraph 里的标准形式——一个**条件边**。

```bash
python -m examples.p6.router_graph
```

## 闭环：一张统一心智模型

把整个项目串起来：

| 你前面见过的东西 | 它的图的真身 |
|------------------|--------------|
| 单 Agent 循环（Phase 3） | 思考节点 + 工具节点 + 条件边（到 END） |
| 带工具 Agent（Phase 4） | 思考节点 + 工具节点 + 条件边 |
| CrewAI crew（Phase 5） | 线性图：role 节点 + 顺序边 |
| AutoGen 群聊（Phase 5） | 角色节点 + 协调者条件边 |
| 本 Phase 的 LangGraph | 上面每一个的**标准写法** |

> **范式统一论闭环**：CrewAI / AutoGen / 手写循环，本质都是「状态 + 节点 + 条件边」。LangGraph 把这个共性抽象成一门通用语言。掌握它，你就不用再为每个框架单独学一套编排 API——它们的底层，你都已经懂了。

## 为什么用图而不是直接写 for 循环

- **可观测**：图结构可被可视化、被追踪（配合 LangSmith / Langfuse）。
- **可控**：循环次数、状态更新、分支逻辑都在图里显式声明，不再藏在一堆 `if/for` 里。
- **可组合**：子图可以作为节点嵌入更大图，天然支持复杂多 Agent 系统。
- **可持久化**：状态可存数据库，支持中断恢复、人工介入（HITL，见后续 Phase）。

## 验收清单

- [ ] 能说出 State / Node / Edge / 条件边 各自是什么
- [ ] 能凭记忆用 StateGraph 写出「线性流水线」和「带条件边的路由」
- [ ] 跑通过示例 1 和示例 2
- [ ] 能向别人解释「为什么 CrewAI/AutoGen 都能用 LangGraph 表达」

## 下一步

Phase 7 起进入工程化与实战：把图用在生产级多 Agent 系统（Capstone）、加上**人工介入（HITL）**、**持久化与断点续跑**，最后是 **Phase 8–9 的生产部署实战**。你的「底层范式」地基已经打牢。

## 扩展示例 / Extra Example {#extra-p6}

### 条件分支图（examples/p6/branching.py）
用 `add_conditional_edges` 把请求路由到不同节点——这正是 AutoGen 协调者路由的「图」表达。

```bash
python -m examples.p6.branching
```

