# Phase 7 · Human-in-the-Loop & Persistence: Two Pillars of Production Agents

> Goal: master the two capabilities that take an Agent from "toy" to "production" — **Human-in-the-loop (HITL)** and **state persistence**. They are what make the Phase 6 graph actually deployable.

## Why HITL (Human-in-the-loop)

Previous graphs were fully automatic — the model ran to END. But in real business, some nodes you **dare not** let run unsupervised:
- Sending emails, charging money, deleting data — one mistake is costly;
- Legal/medical/financial conclusions — a human must have the final say;
- When the model is unsure — let a person decide.

HITL means: at a critical node, **pause and hand control to a human**, then continue after their confirmation. In graph terms, it's a **conditional edge** whose "decision maker" is a human.

## Implementing an approval node with interrupt

```python
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

def approval_node(state):
    human_input = interrupt({"draft": state["draft"], "prompt": "Approve? (yes/no)"})
    return {"approved": human_input.lower() == "yes"}

graph = builder.compile(checkpointer=MemorySaver())   # needs checkpointer to interrupt
graph.invoke({"topic": "..."}, config)                 # pauses at interrupt
graph.invoke(Command(resume="yes"), config)            # resume from breakpoint
```

Example file: `examples/p7/hitl_approve.py` — draft → **pause for approval** → (yes) publish / (no) revise. Run:

```bash
python -m examples.p7.hitl_approve
```

## Why persistence (checkpoint)

Long tasks (research, generation, multi-step retrieval) take seconds to minutes. If:
- the process crashes mid-way → redo from scratch, wasting time and money;
- the user closes the page → progress is lost on return;
- combined with HITL → a person leaves for hours and must resume later.

LangGraph uses a **checkpointer** to auto-save graph execution state externally (memory / SQLite / Postgres). `thread_id` identifies a session; calls with the same `thread_id` share persisted state.

## Breakpoint resume with MemorySaver

Example file: `examples/p7/persistence.py`:

```python
graph = builder.compile(checkpointer=MemorySaver())
graph.invoke({"topic": "..."}, config)        # pauses at gate's interrupt
saved = graph.get_state(config)               # inspect persisted state
graph.invoke(Command(resume="yes"), config)   # resume from checkpoint
```

You'll see: the `research` result is saved as-is at pause, and resume needs no recomputation. Swap in SqliteSaver/PostgresSaver for cross-process/cross-machine persistence.

```bash
python -m examples.p7.persistence
```

## How these relate to "the graph"

- HITL's approval branch = a **conditional edge**, just with the decision maker switched from "model" to "human";
- Persistence = externalizing the **State** so the graph can "pause — resume" without losing it.

Both prove the point: **modeling with a state graph is inherently more production-fit than a pile of `for/if`** — because state, branching, and pause points are first-class citizens.

## Acceptance checklist

- [ ] Can explain what HITL solves and which nodes need approval
- [ ] Can write the interrupt + Command(resume) pause/resume skeleton
- [ ] Can explain checkpointer and thread_id
- [ ] Have run Example 1 (approval) and Example 2 (persistence resume)

## Next

Phase 8–9: **production deployment in practice**. Wrap the graphs, tools, HITL, and persistence into a served system — containerization, API exposure, observability (LangSmith/Langfuse), and a wrap-up comparing against CrewAI/AutoGen approaches.

## Extra Example {#extra-p7}

### Time travel (examples/p7/time_travel.py)
Use checkpoints to list past states, replay any of them and fork from there — a debugging superpower for multi-step Agents.

```bash
python -m examples.p7.time_travel
```

