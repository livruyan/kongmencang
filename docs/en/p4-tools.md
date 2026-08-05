# Phase 4 · Tools: The Real Source of an Agent's Power

> Goal: understand how tools are actually built, and why good descriptions make or break an Agent's "intelligence". This chapter is the "capability depot" for the Phase 3 Agent.

## What is a tool

In one sentence: **a tool is just a function with a clear description and well-defined arguments.** An Agent can't check the weather or query a database by itself — it's a dispatcher that *decides when to call which tool and how to fill its arguments*. Therefore:

> **An Agent's capability ceiling ≈ the quality of the tools you give it.**

## Building a tool (modern style)

```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    city: str = Field(description="City name, e.g. 'Beijing'")
    unit: str = Field(default="celsius", description="celsius or fahrenheit")

@tool(args_schema=WeatherInput)
def get_weather(city: str, unit: str = "celsius") -> str:
    """Look up the current weather for a city. Use this whenever the user asks about weather."""
    # In production, replace with a real weather API
    return f"{city} is around 22°C (demo data)."
```

Three things to always get right:

1. **The docstring is the "user manual"** — the model uses it to decide *whether and how* to use the tool. Vague docs lead to misuse.
2. **`args_schema` makes argument-filling reliable** — declaring types/descriptions with Pydantic lets the model "fill the form" instead of guessing strings.
3. **Return readable text** — the model reasons on the tool's output, so clearer returns help.

## Example 1: multiple tools + a tool-calling Agent

File: `examples/p4/custom_tools.py`

We build three tools (weather / multiply / reverse text) and run a tool-calling Agent that **picks tools on its own**. Notice how it chains several tools for one question: check weather, reverse text, then multiply.

```bash
python -m examples.p4.custom_tools
```

## Example 2: peeling back the tool-calling mechanism

File: `examples/p4/tool_calling_raw.py`

Example 1 hid the internals behind the framework. This one shows them directly:

1. `model.bind_tools([...])` — attaches tools to the model so it knows what's available and their shapes;
2. The model returns structured `tool_calls` (not plain text);
3. We **execute** those calls one by one and feed results back with `ToolMessage`;
4. We hand the results back to the model to synthesize a final answer.

This is the "modern version" of the Phase 3 hand-rolled ReAct loop — except the model natively supports structured calls, dropping the hand-written string parsing.

```bash
python -m examples.p4.tool_calling_raw
```

## Key insight (keep planting the seed)

Connect this chapter to the last:

- "the model selects which tool to call" → a **node**
- "execute the tool and get the result" → the next **node**
- the transition is decided by the model's `tool_calls` → a **conditional edge**

So a "tool-using Agent" = think node → (branch by model decision) → different tool nodes → aggregate node. Another graph. **You're getting closer to the thesis that "every Agent is a graph".**

## Common pitfalls

- **Vague tool description** → model picks the wrong tool or fills args wrongly. Write descriptions as if for a novice.
- **No argument schema** → model improvises and sends wrong types. Always use `args_schema`.
- **Unhandled tool errors** → one exception can crash the whole Agent. In production, wrap tools in try/except and return friendly errors.

## Acceptance checklist

- [ ] Can build a parameterized tool using `@tool` + `args_schema`
- [ ] Can explain *why* the docstring matters so much
- [ ] Have run Example 1 (multi-tool Agent) and Example 2 (raw tool_calling)
- [ ] Can sketch the graph behind a tool-using Agent (nodes + conditional edges)

## Next

Phase 5 is the first strike of the value spine: **comparing multi-Agent workflows** — a head-on comparison of CrewAI / AutoGen designs, and showing they are isomorphic to LangGraph at the level of "graphs". This is the first official appearance of the project's central claim.

## Extra Example {#extra-p4}

### Structured output (examples/p4/structured_output.py)
Use `with_structured_output` to make the model return data conforming to a Pydantic schema — under the hood a forced tool-call.

```bash
python -m examples.p4.structured_output
```

