# LangChain & LangGraph 系统化学习

> 从底层范式理解 Agent 编排：**状态图 + 节点 + 条件边**。

## 这个项目是什么 / What is this

一个面向「会基础编程、但没碰过 LLM/Agent」开发者的开源学习项目。目标是帮你**从根本上理解 Agent 的工作原理**，为构建复杂应用打基础——而不是只会套模板。

## 核心价值主张 / Core Thesis

市面主流 Agent 框架（CrewAI、AutoGen 等）的底层逻辑，都可以映射到 LangGraph 的 **状态图（StateGraph）+ 节点（Node）+ 条件边（Conditional Edge）** 模型。

> 掌握 LangChain 与 LangGraph，就等于掌握了 Agent 编排的底层范式。

这也是本项目不同于「又一个 LangChain 教程」的地方：我们不做 API 罗列，而是帮你建立一套**通用心智模型**，让你能举一反三地理解和设计任何 Agent 系统。

## 学习路线（13 个 Phase）/ Learning Path

| Phase | 主题 | 关键产出 |
|-------|------|----------|
| 1 | LangChain 核心概念与开发环境（含可跳过速补） | 第一个 Chain |
| 2 | Chains、Memory 与 RAG 基础 | 多步链、记忆对话、RAG |
| 3 | Agent 原理：从 ReAct 到自主循环 | Agent 循环理解 |
| 4 | Tools 与 Function Calling | 工具调用 |
| 5 | 多 Agent 协作范式与主流框架对比 | 框架 → 图的映射 |
| 6 | LangGraph 图编排核心 | StateGraph 实战 |
| 7 | 状态、记忆与 Human-in-the-loop | 可中断工作流 |
| 8 | 生产部署实战 | 服务化 + 可观测 |
| 9 | Capstone 综合实战与全景复盘 | 端到端系统 |
| 10 | 记忆独立层：episodic + semantic + 溯源（防幻觉） | 可溯源记忆 |
| 11 | MCP 工具接口：让智能体调用标准协议工具 | agent ↔ tool |
| 12 | 多智能体协作（A2A）：supervisor + worker | agent ↔ agent（进程内） |
| 13 | A2A 标准协议：Agent Card + JSON-RPC | agent ↔ agent（跨进程） |

> **递进设计**：P1–P9 用具体框架建立直觉并收束到「一切皆图」的统一范式；P10–P13 为进阶实战——记忆独立层 → MCP → 原生多智能体 → A2A 标准协议，逐步补齐「生产级多智能体系统」的智能体互联拼图。

## 如何开始 / Getting Started

1. 配置 Python 环境与依赖（见 [Phase 1 · Python/环境速补](/primer)）。
2. 配置 `.env` 选择模型（OpenAI / DeepSeek / 通义千问 / 本地 Ollama）。
3. 运行你的[第一个 Chain](/p1-hello-chain)。

## 双语说明 / Bilingual

本文档提供**简体中文（默认）**与 **English**（`/en/`）两个版本。顶部可切换语言。
