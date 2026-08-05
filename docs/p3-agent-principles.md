# Phase 3 · Agent 原理：从 ReAct 到自主循环

> 目标：搞懂「Agent 到底在干什么」。这一章不堆概念，而是把 Agent 的核心运行机制拆开给你看——你会发现它远没有听起来那么神秘。

## 一句话理解 Agent

**Agent = 一个会循环的程序**：它拿到一个问题，先「想」(Reasoning)，决定要不要「做」(Acting，比如调工具)，看到结果（Observation）后再想下一步，直到能给出答案。

它不是「更聪明的模型」，而是「让模型接上工具、并在一个循环里反复决策」的编排方式。

## 从 ReAct 说起

ReAct（**Re**asoning + **Act**ing）是 2022 年提出的一种范式，核心思想：让 LLM 把**思考过程**和**行动**交替输出，而不是一次性给答案。

一次典型的 ReAct 交互长这样：

```
Thought: 我需要先确认 langgraph 的拼写，才能数字母。
Action: search
Action Input: langgraph
Observation: LangGraph 是...用「状态 + 节点 + 条件边」描述工作流。
Thought: 拼写是 l-a-n-g-g-r-a-p-h，共 9 个字母。
Final Answer: 9
```

注意三点：
1. 模型并没有「真的」去搜索，是**我们**根据它的 `Action` 去调用工具，再把结果回填成 `Observation`。
2. 模型看到的上下文里包含了前面的 Thought / Observation，所以它能「基于证据」继续推理。
3. 循环在哪停？——模型输出 `Final Answer` 时停。

## 示例 1：手动实现 ReAct 循环

文件：`examples/p3/react_loop.py`

我们**不**用任何 Agent 框架，纯手写一个最小循环，把上面那套机制跑通：

- 一个特殊提示词，要求模型严格按 `Thought/Action/Action Input/Final Answer` 格式输出；
- `parse_action()` 解析模型输出；
- 当 `Action` 命中工具时，调用它并把 `Observation` 写回「草稿板」(scratchpad)；
- 循环直到出现 `Final Answer` 或达到最大步数。

运行：

```bash
cd langchain-langgraph-course
python -m examples.p3.react_loop
```

跑完你会直观看到：所谓「自主 Agent」，不过是一个 `for` 循环 + 几次字符串解析。

## 示例 2：用框架跑同样的活

文件：`examples/p3/builtin_agent.py`

理解了原理，再用 LangChain 1.x 原生的 `create_agent` 跑一遍同样的问题。框架替我们做了**提示词拼接、输出解析、循环控制、错误处理**——它会把每一步的内部轨迹打印出来，你可以对照示例 1 的手动版本来理解。

```bash
python -m examples.p3.builtin_agent
```

## 关键认知（为后续埋伏笔）

回看这个循环：每一步是一个「节点」，节点间的走向由模型输出（是否 `Final Answer`）决定——这不就是一个**带条件边的图**吗？

- 「思考节点」→（如果还要继续）「工具调用节点」→「观察节点」→ 回到「思考节点」
- 直到「思考节点」判定结束 → 走向「最终答案节点」

**这就是本项目最核心的论点雏形**：你已经亲手写出了一个最朴素的 Agent 图。Phase 5–6 我们会正式用 LangGraph 把这种「状态图 + 节点 + 条件边」显式建模出来，并说明 CrewAI / AutoGen 等框架的底层逻辑都可以映射到同一范式。

## 验收清单

- [ ] 能说清楚 ReAct 的 Thought / Action / Observation 分别是什么
- [ ] 能解释「为什么 Agent 需要循环」而不是一步到位
- [ ] 跑通过示例 1（手动循环）和示例 2（框架 Agent）
- [ ] 能用自己的话描述「Agent 循环如何用图来建模」

## 下一步

Phase 4 我们会深入 **Tools**：如何把任意函数/API 封装成 Agent 可用的工具，如何设计工具的描述、参数与错误处理——这是 Agent 能力的真正来源。

## 扩展示例 / Extra Example {#extra-p3}

### Plan-and-Execute（examples/p3/plan_execute.py）
先规划再执行：把大任务拆成有序步骤，再逐步交给模型完成——自主 Agent 的常见变体。

```bash
python -m examples.p3.plan_execute
```

