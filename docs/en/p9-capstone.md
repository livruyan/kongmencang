# Phase 9 · Capstone Multi-Agent System & 9-Phase Retrospective

> Goal: tie everything together with one **end-to-end runnable** multi-Agent system, then do a single retrospective of the whole course and point to next steps.

## Capstone: an end-to-end research system

Example `examples/p9/capstone.py` folds every concept into **one LangGraph graph**:

```
START -> coordinator
coordinator --(route)--> research / math
research -> writer -> reviewer -> approval
approval --(yes)--> publish
approval --(no)--> revise -> reviewer  (loop)
publish/revise -> END
```

It uses, all at once:
- **Phase 4 Tools**: research node calls a `search` tool;
- **Phase 5 Routing**: coordinator branches by question type;
- **Phase 6 Graph**: StateGraph explicitly models nodes/edges/conditional edges;
- **Phase 7 HITL**: approval node uses `interrupt` to pause for human sign-off;
- **Phase 3 Loop**: each node internally is a "think → act" micro-loop.

```bash
python -m examples.p9.capstone
```

This is the ultimate proof of the unification thesis: **a production-grade multi-Agent system is, at heart, a graph with tools, conditional edges, and the ability to pause.**

## 9-Phase retrospective

| Phase | Core takeaway | Corresponding "graph" concept |
|-------|---------------|------------------------------|
| 1 | LangChain core, first Chain | Chain = node chain |
| 2 | Composition, memory, RAG | node chain + state (memory/retrieval) |
| 3 | Agent principles (ReAct loop) | think/tool/observe nodes + conditional edge |
| 4 | Tools | tool = node; call = conditional edge |
| 5 | Multi-Agent compared | CrewAI = linear graph, AutoGen = conditional-edge graph |
| 6 | LangGraph orchestration | universal "state + nodes + edges" language |
| 7 | HITL + persistence | human-decision edge + externalized State |
| 8 | Production deployment | graph → service → container → observability |
| 9 | Capstone + retrospective | everything integrated into one graph |

**One-line thread**: you started from "calling one model" and gradually realized "all Agent orchestration can ultimately be expressed as a state graph". That is this project's central claim.

## Where to go next

1. **Subgraphs & modularity**: split each Capstone role into a subgraph, compose into larger systems (LangGraph subgraphs).
2. **Real persistence**: swap MemorySaver for PostgresSaver / Redis to support real multi-user.
3. **Deep observability**: wire Langfuse for cost/latency/quality dashboards.
4. **Evaluation**: use LangSmith datasets for regression eval — quantify "change one prompt, how much does overall quality move".
5. **Hands-on comparison**: re-implement the Capstone in CrewAI / AutoGen to feel the control benefits of the graph paradigm.

## Acceptance checklist (graduation standard)

- [ ] Can build a LangGraph multi-Agent system from scratch (tools, routing, HITL)
- [ ] Can "translate" any Agent framework's orchestration into a graph
- [ ] Can state the course's central claim and prove it with examples
- [ ] Has run the Capstone example

---

🎓 **Congratulations on finishing all 9 Phases.** You now understand Agent orchestration from the underlying paradigm — enough to build complex, controllable, deployable Agent applications.

## Extra Example {#extra-p9}

### Minimal eval (examples/p9/eval_pipeline.py)
A safety net before shipping: check whether outputs contain required keywords across a set of assertion cases, then compute a pass rate.

```bash
python -m examples.p9.eval_pipeline
```

