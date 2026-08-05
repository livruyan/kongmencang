# Phase 3 · Agent Principles: From ReAct to the Autonomous Loop

> Goal: understand what an Agent actually *does*. This chapter doesn't pile on jargon — it takes the core mechanism apart so you can see it's far less mysterious than it sounds.

## The one-sentence version of an Agent

**An Agent = a program that loops.** It takes a question, *thinks* (Reasoning), decides whether to *act* (Acting — e.g. call a tool), sees the result (Observation), then thinks again — repeating until it can answer.

It is not "a smarter model". It is an orchestration that *connects a model to tools and lets it make decisions repeatedly inside a loop*.

## Starting with ReAct

ReAct (**Re**asoning + **Act**ing) is a paradigm from 2022 whose core idea is: let the LLM emit its *reasoning* and its *actions* **interleaved**, rather than answering in one shot.

A typical ReAct turn looks like:

```
Thought: I should confirm the spelling of "langgraph" before counting letters.
Action: search
Action Input: langgraph
Observation: LangGraph is ... a framework using "state + nodes + conditional edges".
Thought: The spelling is l-a-n-g-g-r-a-p-h, that's 9 letters.
Final Answer: 9
```

Three things to notice:
1. The model doesn't *really* search — **we** call the tool based on its `Action`, then feed the result back as `Observation`.
2. The model's context includes the preceding Thought / Observation, so it can reason *on evidence*.
3. Where does the loop stop? — when the model emits `Final Answer`.

## Example 1: hand-rolling the ReAct loop

File: `examples/p3/react_loop.py`

We build a minimal loop **without** any Agent framework, to run the mechanism above:

- A special prompt forces the model to output strictly in `Thought/Action/Action Input/Final Answer` format;
- `parse_action()` parses the model output;
- When `Action` hits a tool, we call it and write the `Observation` back to the *scratchpad*;
- The loop continues until `Final Answer` appears or the step budget is exhausted.

Run it:

```bash
cd langchain-langgraph-course
python -m examples.p3.react_loop
```

After running it, you'll see concretely: an "autonomous Agent" is just a `for` loop plus a bit of string parsing.

## Example 2: the same job with a framework

File: `examples/p3/builtin_agent.py`

Now that you understand the principle, run the same question with LangChain 1.x's native `create_agent`. The framework does the **prompt stitching, output parsing, loop control, and error handling** for you — it prints the internal trace of every step so you can map it back to the hand-rolled version.

```bash
python -m examples.p3.builtin_agent
```

## Key insight (a setup for later)

Look again at the loop: each step is a *node*, and where the flow goes is decided by the model's output (whether it's `Final Answer`) — isn't that a **graph with conditional edges**?

- "think node" → (if not done) "tool node" → "observe node" → back to "think node"
- until the "think node" decides to stop → "final answer node"

**This is the seed of this project's central thesis:** you just hand-wrote the most naive Agent graph. In Phase 5–6 we'll formally model this "state + nodes + conditional edges" with LangGraph, and show how the underlying logic of frameworks like CrewAI / AutoGen maps onto the same paradigm.

## Acceptance checklist

- [ ] Can explain what Thought / Action / Observation mean in ReAct
- [ ] Can explain *why* an Agent needs a loop instead of answering in one step
- [ ] Have run Example 1 (manual loop) and Example 2 (framework Agent)
- [ ] Can describe in your own words "how the Agent loop is modeled as a graph"

## Next

Phase 4 goes deep on **Tools**: how to wrap any function / API into a tool an Agent can use, and how to design a tool's description, arguments, and error handling — the real source of an Agent's capability.

## Extra Example {#extra-p3}

### Plan-and-Execute (examples/p3/plan_execute.py)
Plan a task into ordered steps, then execute them one by one — a common Agent variant.

```bash
python -m examples.p3.plan_execute
```

