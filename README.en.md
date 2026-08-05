# LangChain & LangGraph: A Systematic Course

> Understand Agent orchestration from first principles: **State Graph + Nodes + Conditional Edges**.

This is an open-source learning project for developers who can program but have not yet worked with LLMs / Agents. The goal is to help you truly understand how Agents work, so you can build complex applications on a solid foundation.

Our core thesis: most mainstream Agent frameworks (CrewAI, AutoGen, etc.) can be mapped onto LangGraph's model of **StateGraph + Node + Conditional Edge**. Master LangChain and LangGraph, and you master the underlying paradigm of Agent orchestration.

## Language / 语言

- This project is **bilingual**: Simplified Chinese (default) and English (under `/en/`).
- 本文档提供**双语**：简体中文（默认）与 English（`/en/`）。

## Quick Start (recommended, one command)

This repo ships an **editor-agnostic** `Makefile` that works in the PyCharm / WebStorm terminal, VS Code, or CI:

```bash
make setup        # create .venv, install Python + Node deps, copy .env
make docs         # build the bilingual docs site -> docs/.vitepress/dist
make docs-dev     # live preview at http://localhost:5173
make run p=1      # run Phase 1 example (p=2..9 likewise)
make lint         # py_compile all examples
```

> **IDE usage (PyCharm + WebStorm)**: open the project root in PyCharm for the Python `examples/`; open `docs/` in WebStorm (or just run `make docs-dev` from the PyCharm terminal) for the docs site. Both IDEs have a built-in Terminal to run the `make` commands above.
>
> Requirements: Python 3.13+, Node 22+.

The sections below are the manual equivalent.

## Learning Path (9 Phases)

| Phase | Topic |
|-------|-------|
| 1 | LangChain Core Concepts & Environment (with skippable primer) |
| 2 | Chains, Memory & RAG Basics |
| 3 | Agent Principles: from ReAct to Autonomous Loops |
| 4 | Tools & Function Calling |
| 5 | Multi-Agent Patterns & Framework Comparison |
| 6 | LangGraph Graph Orchestration Core |
| 7 | State, Memory & Human-in-the-loop |
| 8 | Multi-Agent Workflow System (Capstone) |
| 9 | Production Deployment |

## Running the Examples

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # choose LLM_PROVIDER: openai / deepseek / ollama
python -m examples.p1.hello_chain
```

## Preview the Docs Locally

```bash
npm install
npm run docs:dev
```

## Runtime / Provider Abstraction

Every example switches models through one abstraction layer (`examples/common/llm.py`): `openai` (default), `deepseek` (OpenAI-compatible), or `ollama` (local, key-free). See `.env.example`.
