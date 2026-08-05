# Phase 5 · Multi-Agent Workflows Compared: Why They're "The Same Graph"

> Goal: a head-on comparison of mainstream frameworks like CrewAI / AutoGen, and showing they are **isomorphic** to LangGraph at the level of "graphs". This is the **first official appearance** of this project's central claim.

## Two framework designs, up close

### CrewAI: roles + pipeline (crew)
- You define several **Agents (roles)**, each with `role / goal / backstory`;
- You chain them into a sequential/parallel pipeline (crew) using **Tasks**;
- The output of one Agent automatically becomes the input of the next.

Its mental model: **a few specialists lined up in a pipeline**.

### AutoGen: conversation + coordinator
- You define several **ConversableAgents**;
- A **GroupChat / coordinator** decides "who speaks next";
- Roles message each other until someone says "task done".

Its mental model: **a group chat moderated by a coordinator**.

## Translating them back into graphs

Now re-read them through the lens of previous chapters:

| Framework concept | Graph equivalent |
|-------------------|------------------|
| Agent / role | **node** |
| Task chaining / messaging | **edge** |
| CrewAI sequential execution | **fixed sequential edge** |
| AutoGen coordinator "who speaks next" | **conditional edge** |
| shared state / chat history | **graph state** |

**Conclusion**: CrewAI's sequential crew ≈ a "linear graph"; AutoGen's group chat ≈ a "graph with conditional edges". Both are fundamentally "state + nodes + edges", just with different APIs.

> This is the project's central claim: **the underlying logic of mainstream Agent frameworks maps onto LangGraph's "state graph + nodes + conditional edges" model.** Master LangGraph, and you master their common language.

## Example 1: hand-rolled crew (CrewAI analog)

File: `examples/p5/mini_crew.py`

Without installing CrewAI, we chain "Researcher → Writer → Reviewer" with three prompt templates. You'll see it's the **same structure** as a CrewAI crew — CrewAI just automates "feed the previous output to the next step".

```bash
python -m examples.p5.mini_crew
```

## Example 2: coordinator routing (AutoGen conditional-edge analog)

File: `examples/p5/agent_router.py`

A coordinator reads the user request, outputs "route to math / language / code", then executes the chosen node. That routing moment is the **conditional edge** of AutoGen's coordinator deciding "who speaks next".

```bash
python -m examples.p5.agent_router
```

## Key insight

The unification thesis is now almost self-evident:
- Phase 3: single-Agent loop = graph (think/tool/observe nodes + conditional edge)
- Phase 4: tool-using Agent = graph (think node + tool nodes + conditional edge)
- Phase 5: multi-Agent frameworks = graph (role nodes + sequential/conditional edges + shared state)

**Since they're all graphs at heart, why not express them uniformly with a framework built for graphs?** That's exactly what Phase 6 answers — LangGraph takes the stage.

## Acceptance checklist

- [ ] Can describe the design difference between CrewAI (roles + pipeline) and AutoGen (chat + coordinator)
- [ ] Can map "role / message / coordinator decision" to "node / edge / conditional edge"
- [ ] Have run Example 1 (hand-rolled crew) and Example 2 (coordinator routing)
- [ ] Can restate the central claim: "mainstream Agent frameworks are graphs underneath"

## Next

Phase 6: **LangGraph graph orchestration** — using state graphs, nodes, and conditional edges to express everything from earlier chapters in one unified way, and comparing the code-size difference between "framework graph" vs "hand-rolled graph". The unification thesis closes its loop here.

## Extra Example {#extra-p5}

### Two-agent debate (examples/p5/debate.py)
One shape of an AutoGen group-chat: two roles take turns challenging each other, driven by a simple turn loop.

```bash
python -m examples.p5.debate
```

