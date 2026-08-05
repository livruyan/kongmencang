# Phase 5 · 多 Agent 工作流对比：它们为什么是「同一张图」

> 目标：正面比较 CrewAI / AutoGen 等主流框架，并指出它们与 LangGraph 在「图」这一层其实是**同构**的。这是本项目核心主张的**第一次正式亮相**。

## 先看两个框架怎么设计

### CrewAI：角色 + 流水线（crew）
- 你定义若干 **Agent（角色）**，每个角色有 `role / goal / backstory`；
- 用 **Task** 把角色串成一条顺序/并行的流水线（crew）；
- 前一个 Agent 的输出自动成为下一个的输入。

它的心智模型是：**几个专职角色排成一条流水线**。

### AutoGen：对话 + 协调者
- 你定义若干 **ConversableAgent（可对话角色）**；
- 一个 **GroupChat / 协调者** 决定「下一句话该谁说」；
- 角色之间互相发消息，直到某角色说「任务完成」。

它的心智模型是：**一群角色在群里聊天，由协调者控场**。

## 把它们「翻译」回图

现在用我们前几章的视角重看：

| 框架概念 | 图里的对应物 |
|----------|--------------|
| Agent / 角色 | **节点（node）** |
| Task 串联 / 消息传递 | **边（edge）** |
| CrewAI 的顺序执行 | **固定顺序的边** |
| AutoGen 协调者「下一个谁说」 | **条件边（conditional edge）** |
| 共享的状态 / 对话历史 | **图的状态（state）** |

**结论**：CrewAI 的顺序 crew ≈ 一张「线性图」；AutoGen 的群聊 ≈ 一张「带条件边的图」。两者底层都是「状态 + 节点 + 边」，只是 API 长得不一样。

> 这就是本项目的核心主张：**主流 Agent 框架的底层逻辑，都能映射到 LangGraph 的「状态图 + 节点 + 条件边」模型。** 掌握 LangGraph，你就掌握了它们的通用语言。

## 示例 1：手写一个 crew（模拟 CrewAI）

文件：`examples/p5/mini_crew.py`

不装 CrewAI，用三个 prompt 模板把「研究员 → 写手 → 审校」串成流水线。你会看到它和 CrewAI 的 crew 是**同一个结构**——只是 CrewAI 帮你把「把上一步输出喂给下一步」这件事自动化了。

```bash
python -m examples.p5.mini_crew
```

## 示例 2：协调者路由（模拟 AutoGen 的条件边）

文件：`examples/p5/agent_router.py`

一个协调者读取用户请求，输出「该派给 math / language / code 哪个专家」，然后执行对应节点。这个「派给谁」的瞬间，就是 AutoGen group-chat 里协调者决定「下一个谁发言」的**条件边**。

```bash
python -m examples.p5.agent_router
```

## 关键认知

到这里，范式统一论已经呼之欲出：
- Phase 3：单 Agent 循环 = 图（思考/工具/观察节点 + 条件边）
- Phase 4：带工具 Agent = 图（思考节点 + 工具节点 + 条件边）
- Phase 5：多 Agent 框架 = 图（角色节点 + 顺序/条件边 + 共享状态）

**既然它们本质都是图，为什么不直接用一个专门描述「图」的框架来统一表达？** 这正是 Phase 6 要回答的问题——LangGraph 登场。

## 验收清单

- [ ] 能说出 CrewAI（角色+流水线）与 AutoGen（对话+协调者）的设计差异
- [ ] 能把「角色 / 消息 / 协调者决策」分别映射到「节点 / 边 / 条件边」
- [ ] 跑通过示例 1（手写 crew）和示例 2（协调者路由）
- [ ] 能复述本项目核心主张：「主流 Agent 框架底层皆图」

## 下一步

Phase 6：**LangGraph 图编排**——正式用状态图、节点、条件边把前面所有案例「归一」表达，并对比「用框架图 vs 前面手写的图」代码量差异。范式统一论在此完成闭环。

## 扩展示例 / Extra Example {#extra-p5}

### 双 Agent 辩论（examples/p5/debate.py）
模拟 AutoGen group-chat 的一种形态：两个角色交替发言、互相挑战，由简单轮次循环驱动。

```bash
python -m examples.p5.debate
```

