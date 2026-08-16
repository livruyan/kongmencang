# Frameworks vs Self-built Kernels for Agents: My Dual-Track Practice

> A technical write-up to build a personal brand. Maps to report P2 "blog comparing with Lingxi".
> Companion whiteboard draft: [LangGraph state machine + checkpoint](./whiteboard-langgraph).

## One-line conclusion

**Frameworks let you ship fast; self-built kernels let you understand the internals.** They are not
either/or — they are the two pillars of Agent competency. With LangGraph I can deliver a persistent,
human-in-the-loop multi-agent service within a week; with the self-built kernel "Lingxi" I can explain
every detail of dual-brain collaboration, reflection loops, and weight evolution.

## Positioning of the two projects

| Dimension | LangGraph project (this repo) | Lingxi (self-built kernel) |
|-----------|-------------------------------|----------------------------|
| Nature | Framework practice: engineering wrapping + extension of official LangChain tutorials | Self-built kernel: implement the Agent runtime from scratch |
| Proves | "Keeps up with the mainstream stack", "can ship frameworks in production" | "Understands Agent internals", "can build the wheels" |
| Core | StateGraph + Node + Conditional Edge + checkpoint + HITL | Dual-brain + reflection loop + weight evolution |
| Memory | Independent layer: episodic + semantic + traceability (anti-hallucination) | Self-built memory / evolution module |
| Tools | MCP standard-protocol interface | Self-built tool registry & dispatch |
| Tell it to | "Do you know mainstream frameworks?" | "Do you understand the internals / can you build?" |

## Why dual-track

- **Complete resume narrative**: tutorial alone looks like "followed along"; self-built alone looks like
  "never touched industrial practice". Together: "ships fast with frameworks AND builds the internals".
- **Interview complement**: "How does a state machine work?" → explain via LangGraph's state graph;
  "How would you build it without a framework?" → explain via Lingxi.
- **Risk hedge**: frameworks iterate fast and break APIs; a self-built kernel is your own hard knowledge.

## Honest disclaimer (important)

The LangGraph project is a **learning/tutorial project**, not a from-scratch system. If asked in an
interview whether it was independently designed, say honestly: "engineering wrapping + deployment
extension of the official tutorials", and pivot to the internals you truly mastered — state machine,
checkpoint persistence, HITL, independent memory layer, MCP substrate.

## The unified four-project story

- **LangGraph (framework) + Lingxi (kernel) = Agent double insurance**
- **Aesthetic system (AI + creative product) + RealEstateAI (full-stack ML) = application & engineering breadth**

One sentence: can model, can build Agents, can ship product-grade applications.
