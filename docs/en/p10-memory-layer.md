# Phase 10 · Independent Memory Layer: episodic + semantic + traceability

> Maps to report P0 "memory independent layer". Source: `examples/common/memory.py`, `examples/p10/hello_chain.py`.

## Why this layer

Earlier "memory" was only a checkpoint state snapshot (`MemorySaver`) — a task-level snapshot, not
real, durable / traceable knowledge. A production Agent needs:

- **Episodic (short-term)**: what happened in a session, replayable;
- **Semantic (long-term)**: facts distilled from dialogue, reusable across sessions;
- **Traceability**: every semantic memory carries a source; answers must cite it — the anti-hallucination switch.

## Three layers

```python
from examples.common.memory import MemoryStore
ms = MemoryStore()                        # :memory: demo; pass a file path for persistence
eid = ms.add_episode("s1", "user", "We chose LangGraph.")
ms.add_semantic("Orchestration framework = LangGraph", f"episode:{eid}", "s1")
```

Retrieve with citations:

```python
ctx = ms.build_citation_context("orchestration")   # returns facts with [source]
# empty when no source -> caller must NOT let the model assert; refuse instead
```

## Anti-hallucination

`build_citation_context` returns "" when nothing matches. Inject it into the prompt:
non-empty → model may only answer from memory and cite; empty → model says "no memory found", no fabrication.

## Run

```bash
make run p=10
```

## Summary

- Memory ≠ checkpoint snapshot: checkpoint is task-level state; the memory layer is durable, traceable knowledge.
- The three layers (episodic / semantic / traceability) let the Agent cite sources — the hard switch for anti-hallucination.
- With memory as an independent layer, RAG handles retrieval and memory handles "known facts" — cleaner separation of concerns.
