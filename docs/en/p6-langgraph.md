# Phase 6 · LangGraph Orchestration: Closing the Unification Loop

> Goal: express everything from earlier chapters in one unified way with LangGraph. When you see CrewAI crews, AutoGen chats, and single-Agent loops all writable as "state graph + nodes + conditional edges", the project's central claim closes its loop.

## Three core LangGraph concepts

1. **State**: a "shared whiteboard" flowing between nodes, defined with `TypedDict` or Pydantic. Each node reads and writes it.
2. **Node**: an ordinary function `(state) -> partial state update`. It can be an LLM call, a tool, or any logic.
3. **Edge**: connections between nodes.
   - **Normal edge**: fixed order, e.g. `A → B`.
   - **Conditional edge** `add_conditional_edges`: a function reads the state and decides where to go next — this is the source of "intelligent routing".

Two reserved endpoints: `START` (entry) and `END` (exit).

## Example 1: the Phase 5 crew as a graph

File: `examples/p6/crew_graph.py`

Recall the "Researcher → Writer → Reviewer" pipeline we hand-rolled in Phase 5. In LangGraph:

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

See — a CrewAI crew = a **linear graph**. Different framework, identical "nodes + edges" structure.

```bash
python -m examples.p6.crew_graph
```

## Example 2: coordinator routing as a conditional edge

File: `examples/p6/router_graph.py`

The Phase 5 "coordinator picks the next expert" logic, expressed with `add_conditional_edges`:

```python
builder.add_conditional_edges(
    "coordinator",
    route_by_state,                    # reads state["route"] to decide
    {"math": "math", "language": "language", "code": "code"},
)
```

This is exactly AutoGen's "coordinator decides who speaks" in LangGraph's standard form — a **conditional edge**.

```bash
python -m examples.p6.router_graph
```

## The loop closes: one unified mental model

Tying the whole project together:

| What you've seen | Its true graph form |
|------------------|---------------------|
| Single-Agent loop (Phase 3) | think node + tool node + conditional edge (to END) |
| Tool-using Agent (Phase 4) | think node + tool nodes + conditional edge |
| CrewAI crew (Phase 5) | linear graph: role nodes + sequential edges |
| AutoGen chat (Phase 5) | role nodes + coordinator conditional edge |
| This Phase's LangGraph | the **standard notation** for all of the above |

> **Unification thesis, closed**: CrewAI / AutoGen / hand-rolled loops are all fundamentally "state + nodes + conditional edges". LangGraph abstracts that commonality into a general language. Master it and you no longer learn a separate orchestration API per framework — you already understand their underpinnings.

## Why a graph instead of a for-loop

- **Observable**: graph structure can be visualized and traced (with LangSmith / Langfuse).
- **Controllable**: loop counts, state updates, branching are all explicitly declared, not buried in `if/for`.
- **Composable**: subgraphs embed as nodes in larger graphs — natural fit for complex multi-Agent systems.
- **Persistable**: state can be stored, enabling interruption/resume and human-in-the-loop (later phases).

## Acceptance checklist

- [ ] Can state what State / Node / Edge / conditional edge each are
- [ ] Can write a "linear pipeline" and a "conditional-edge router" from memory using StateGraph
- [ ] Have run Example 1 and Example 2
- [ ] Can explain to someone "why CrewAI/AutoGen can both be expressed in LangGraph"

## Next

Phase 7 onward moves into engineering and practice: a production-grade multi-Agent system (Capstone), **human-in-the-loop (HITL)**, **persistence and resume**, and finally **Phase 8–9 production deployment**. Your "underlying paradigm" foundation is now solid.

## Extra Example {#extra-p6}

### Conditional branching graph (examples/p6/branching.py)
Use `add_conditional_edges` to route a request to different nodes — the graph form of AutoGen's coordinator routing.

```bash
python -m examples.p6.branching
```

