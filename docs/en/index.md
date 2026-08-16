# LangChain & LangGraph: A Systematic Course

> Understand Agent orchestration from first principles: **State Graph + Nodes + Conditional Edges**.

## What is this / 这个项目是什么

An open-source learning project for developers who can program but have not yet worked with LLMs / Agents. The goal is to help you **truly understand how Agents work**, so you can build complex applications on a solid foundation — not just copy templates.

## Core Thesis / 核心价值主张

We believe most mainstream Agent frameworks (CrewAI, AutoGen, etc.) can be mapped onto LangGraph's model of **StateGraph + Node + Conditional Edge**.

> Master LangChain and LangGraph, and you master the underlying paradigm of Agent orchestration.

That is also what sets this project apart from "yet another LangChain tutorial": instead of listing APIs, we help you build a **general mental model** so you can understand and design any Agent system.

## Learning Path (13 Phases) / 学习路线

| Phase | Topic | Key Output |
|-------|-------|------------|
| 1 | LangChain Core & Environment (skippable primer) | First Chain |
| 2 | Chains, Memory & RAG Basics | Multi-step chains, RAG |
| 3 | Agent Principles: ReAct to Loops | Agent loop |
| 4 | Tools & Function Calling | Tool use |
| 5 | Multi-Agent Patterns & Comparison | Framework → graph mapping |
| 6 | LangGraph Orchestration Core | StateGraph in practice |
| 7 | State, Memory & Human-in-the-loop | Interruptible workflows |
| 8 | Production Deployment | Serving + observability |
| 9 | Capstone Project & Full Review | End-to-end system |
| 10 | Independent Memory Layer: episodic + semantic + traceability | Traceable memory |
| 11 | MCP Tool Interface: standard-protocol tools | agent ↔ tool |
| 12 | Multi-Agent Collaboration (A2A): supervisor + worker | agent ↔ agent (in-process) |
| 13 | A2A Standard Protocol: Agent Card + JSON-RPC | agent ↔ agent (cross-process) |

> **Progressive design**: P1–P9 build intuition with concrete frameworks and converge on the "everything is a graph" paradigm; P10–P13 are advanced hands-on chapters — memory layer → MCP → native multi-agent → A2A standard protocol — completing the agent-interconnection picture of a production multi-agent system.

## Getting Started / 如何开始

1. Set up Python & dependencies (see [Phase 1 · Python/Env Primer](/en/primer)).
2. Configure `.env` to choose a model (OpenAI / DeepSeek / Qwen / local Ollama).
3. Run your [first Chain](/en/p1-hello-chain).

## Bilingual / 双语

This docs site is available in **Simplified Chinese (default)** and **English** (you are here). Switch via the language toggle at the top.
