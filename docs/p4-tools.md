# Phase 4 · Tools：Agent 能力的真正来源

> 目标：搞懂「工具」是怎么造出来的、为什么描述写得好坏直接决定 Agent 智商。这一章是 Phase 3 Agent 的「能力补给站」。

## 工具是什么

一句话：**工具就是一个「带清晰说明 + 明确参数」的函数**。Agent 本身不会算天气、不会查数据库，它只是「决定何时调用哪个工具、怎么填参数」的调度员。所以——

> **Agent 的能力上限 ≈ 你给它的工具质量。**

## 造一个工具（现代写法）

```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    city: str = Field(description="城市名称，例如 '北京'")
    unit: str = Field(default="celsius", description="celsius 或 fahrenheit")

@tool(args_schema=WeatherInput)
def get_weather(city: str, unit: str = "celsius") -> str:
    """查询指定城市的当前天气。当用户问天气时一定要用这个工具。"""
    # 真实场景这里换成天气 API
    return f"{city} 当前约 22°C（演示数据）。"
```

三个必须注意的点：

1. **docstring 就是「使用说明书」**：模型靠它判断「该不该用、怎么用」这个工具。写得含糊，模型就会乱用。
2. **args_schema 决定参数能否被正确填充**：用 Pydantic 声明类型与描述后，模型才能稳定地「填表」，而不是瞎编字符串。
3. **返回值要可读**：模型会基于工具返回的文本继续推理，返回结构越清晰越好。

## 示例 1：多工具 + tool-calling Agent

文件：`examples/p4/custom_tools.py`

我们造了三个工具（天气 / 乘法 / 字符串反转），用 1.x 原生的 `create_agent` 跑一个会**自己挑工具**的 Agent。注意同一个问题里它如何先后调用多个工具：先查天气、再反转文本、再乘法。

```bash
python -m examples.p4.custom_tools
```

## 示例 2：揭开 tool-calling 的底层

文件：`examples/p4/tool_calling_raw.py`

示例 1 用框架把「工具调用」封装了，你看不到内部。这个示例直接演示：

1. `model.bind_tools([...])` —— 把工具「挂」到模型上，模型就知道有哪些工具、参数长什么样；
2. 模型返回结构化的 `tool_calls`（而不是纯文本）；
3. 我们**逐个执行**这些调用，把结果用 `ToolMessage` 回填；
4. 再把结果交回模型，让它综合出最终答案。

这正是 Phase 3 手动 ReAct 循环的「现代版」——只不过模型原生支持结构化调用，省掉了手写字符串解析。

```bash
python -m examples.p4.tool_calling_raw
```

## 关键认知（继续埋伏笔）

把这一章和上一章连起来看：

- 「模型选出要调用的工具」→ 一个**节点**
- 「执行工具、拿到结果」→ 下一个**节点**
- 二者之间的跳转，由模型的 `tool_calls` 决定 → **条件边**

所以「带工具的 Agent」= 思考节点 →（按模型决策分流）→ 不同工具节点 → 汇总节点。又是一张图。**你已经离「一切 Agent 皆图」的范式统一论越来越近了。**

## 常见坑

- **工具描述含糊** → 模型选错工具或参数填错。写 description 时想象「一个新手看了能不能用对」。
- **参数无 schema** → 模型自由发挥，容易传错类型。务必用 `args_schema`。
- **工具报错没兜住** → 一次异常可能让整个 Agent 崩。生产环境应在工具内 try/except 并返回友好错误信息。

## 验收清单

- [ ] 能独立用 `@tool` + `args_schema` 造一个带参数的工具
- [ ] 能解释「为什么 docstring 如此重要」
- [ ] 跑通过示例 1（多工具 Agent）和示例 2（底层 tool_calling）
- [ ] 能画出「带工具 Agent」对应的图（节点 + 条件边）

## 下一步

Phase 5 是价值主轴的第一击：**多 Agent 工作流对比**——正面比较 CrewAI / AutoGen 的设计，并指出它们和 LangGraph 在「图」这一层其实是同构的。这正是本项目核心主张的第一次正式亮相。

## 扩展示例 / Extra Example {#extra-p4}

### 结构化输出（examples/p4/structured_output.py）
用 `with_structured_output` 让模型按 Pydantic schema 返回结构化数据，底层是一次强制工具调用。

```bash
python -m examples.p4.structured_output
```

