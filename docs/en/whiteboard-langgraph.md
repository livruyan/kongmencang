# LangGraph State Machine + checkpoint Whiteboard Draft

> Interview material / whiteboard prep. Maps to report "prepare LangGraph state machine + checkpoint whiteboard draft".

## 1. Minimal state graph (draw while explaining)

```
   START
     │
     ▼
 [research]  ──node: call LLM for key points──►  write state["research"]
     │
     ▼
  [gate]     ──node: interrupt to wait for human approve──►
     │                                                          │
     ▼ (resume="yes")                                          │
 [summarize]  ──node: summarize from points──► write state["summary"]  │
     │                                                          │
     ▼                                                          │
    END ───────────────────────────────────────────────────────┘
```

- **StateGraph**: a TypedDict defines the global state (`topic / research / summary` here).
- **Node**: a pure function `(state) -> partial update`; the framework merges the return into state.
- **Conditional Edge**: a function picks the next edge from state. This is why "one graph" can express
  ReAct / Plan-Execute / debate — the routing logic is just edges.

## 2. How checkpoint persists & recovers (always asked)

- Inject `checkpointer` at `compile(checkpointer=MemorySaver())`.
- Every `invoke` carries `config={"configurable": {"thread_id": "x"}}` — **thread_id is the coordinate of state**.
- The framework writes the full state after each step to a backend (memory / SQLite / Postgres).
- **Recover**: `graph.get_state(config)` reads the latest state; `graph.invoke(Command(resume=...), config)`
  resumes from the last checkpoint — survives process restart and user leaving & returning.

## 3. How HITL works (always asked)

- `from langgraph.types import interrupt`
- In `gate` node: `interrupt({"research": ..., "prompt": "continue?"})` — pauses and returns control to caller;
  state is already persisted.
- Caller sends the decision back with `Command(resume="yes"/"no")`; graph continues from the breakpoint.
- Landing points: human approval, sensitive-op confirmation, external-system receipts — all at `interrupt`.

## 4. Memory vs RAG (always asked)

- **Memory** = snapshot or traceable memory of conversation / task state (independent layer + checkpoint here).
- **RAG** = retrieve from external knowledge base to feed the model; solves "don't know".
- Difference: Memory is "I remember what just happened"; RAG is "let me look it up".
- Anti-hallucination: each semantic memory carries `source_ref`; without a source the model must not assert.

## 5. Difference from self-built kernel (Lingxi) (always asked)

- LangGraph = use the framework: state graph, scheduling, persistence out of the box — ship fast.
- Lingxi = self-built kernel: dual-brain + reflection loop + weight evolution — implement the runtime yourself.
- One sentence: frameworks ship fast, self-build teaches internals; they complement each other.
