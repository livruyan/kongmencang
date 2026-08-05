# LangChain & LangGraph: A Systematic Course

> Understand Agent orchestration from first principles: **State Graph + Nodes + Conditional Edges**.

## What is this / 这个项目是什么

An open-source learning project for developers who can program but have not yet worked with LLMs / Agents. The goal is to help you **truly understand how Agents work**, so you can build complex applications on a solid foundation — not just copy templates.

## Core Thesis / 核心价值主张

We believe most mainstream Agent frameworks (CrewAI, AutoGen, etc.) can be mapped onto LangGraph's model of **StateGraph + Node + Conditional Edge**.

> Master LangChain and LangGraph, and you master the underlying paradigm of Agent orchestration.

That is also what sets this project apart from "yet another LangChain tutorial": instead of listing APIs, we help you build a **general mental model** so you can understand and design any Agent system.

## Learning Path (9 Phases) / 学习路线

| Phase | Topic | Key Output |
|-------|-------|------------|
| 1 | LangChain Core & Environment (skippable primer) | First Chain |
| 2 | Chains, Memory & RAG Basics | Multi-step chains |
| 3 | Agent Principles: ReAct to Loops | Agent loop |
| 4 | Tools & Function Calling | Tool use |
| 5 | Multi-Agent Patterns & Comparison | Framework → graph mapping |
| 6 | LangGraph Orchestration Core | StateGraph in practice |
| 7 | State, Memory & Human-in-the-loop | Interruptible workflows |
| 8 | Multi-Agent Workflow System (Capstone) | End-to-end system |
| 9 | Production Deployment | Serving + observability |

> **Progressive design**: early chapters build intuition with concrete frameworks; Phase 5–6 converge on the "everything is a graph" paradigm.

## Getting Started / 如何开始

1. Set up Python & dependencies (see [Phase 1 · Python/Env Primer](/en/primer)).
2. Configure `.env` to choose a model (OpenAI / DeepSeek / local Ollama).
3. Run your [first Chain](/en/p1-hello-chain).

## Bilingual / 双语

This docs site is available in **Simplified Chinese (default)** and **English** (you are here). Switch via the language toggle at the top.
