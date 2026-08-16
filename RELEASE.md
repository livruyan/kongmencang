# LangChain & LangGraph 系统化实战教程 v1.0.1

一套从零讲透「用 LangChain / LangGraph 造 Agent，并理解各框架共通的图编排本质」的双语实战教程。

*A bilingual, hands-on course that takes you from zero to building Agents with LangChain / LangGraph — and reveals the shared graph-orchestration essence behind every agent framework.*

## 核心特性 / Highlights

- 📚 **13 个循序渐进的阶段（P1–P13）**：每个阶段都配「原理讲解 + 可运行示例 + 验收清单」。
- 🔌 **统一运行时抽象层** `examples/common/llm.py`：一行 `LLM_PROVIDER` 切换 `ollama` / `openai` / `deepseek` / `qwen`，示例与具体模型彻底解耦。
- 🧠 **P10 可溯源记忆独立层**：字符级 n-gram 召回 + 强溯源，从机制上抑制「张冠李戴」式幻觉。
- 🔗 **P11 MCP 工具接口**：让智能体按标准协议调用外部工具（真实异步 MCP server）。
- 🤝 **P12 / P13 多智能体协作（A2A）**：先用 LangGraph 原生 supervisor 编排多 worker，再落地 Google **A2A 标准协议**（AgentCard + JSON-RPC 2.0，零额外依赖）。
- ✅ **`verify.sh` 一键验证**：自动跑通 P10–P13 并对照关键输出标记判分（不依赖非确定的 LLM 回答）。
- 🌐 **双语文档站**（VitePress + GitHub Pages）：中文为主，英文 `/en/` 同步。
- 🛠️ **`Makefile` 一键工程化**：`make setup / run / docs / docs-dev / lint`。
- 🖼️ 仓库自带 1280×640 社交媒体预览图 `social-preview.png`。

## 教程结构 / Curriculum

| 阶段 Phase | 主题 Topic |
|---|---|
| P1 | 第一个 Chain / First Chain |
| P2 | 组合链、记忆与 RAG / Chains, Memory & RAG |
| P3 | Agent 原理：从 ReAct 到自主循环 / Agent Principles: ReAct → Autonomy |
| P4 | Tools：Agent 能力的真正来源 / Tools |
| P5 | 多 Agent 工作流对比：它们为什么是「同一张图」 / Multi-Agent: One Graph |
| P6 | LangGraph 图编排：状态图、节点与条件边 / LangGraph Orchestration |
| P7 | 人工介入与状态持久化 / Human-in-the-Loop & Persistence |
| P8 | 生产部署实战：从图到服务 / Production Deployment |
| P9 | Capstone 多 Agent 系统与 13 Phase 全景复盘 / Capstone & Review |
| **P10** | **可溯源记忆独立层与防幻觉 / Traceable Memory Layer** |
| **P11** | **MCP 标准协议工具接口 / MCP Tool Interface** |
| **P12** | **多智能体协作（LangGraph 原生 A2A）/ Multi-Agent (native A2A)** |
| **P13** | **Google A2A 标准协议 / Google A2A Protocol** |

## 本版新增（Phase 10–13）/ What's New

- **P10 · 记忆独立层**：独立的语义记忆库，检索走字符级 n-gram 重合召回（阈值 ≥2 过滤偶然单字重合），每次回答都带「来源溯源」，从机制上避免记忆层张冠李戴。
- **P11 · MCP 工具接口**：启动一个真实的 MCP server（stdio），用 `langchain-mcp-adapters` 把 MCP 工具挂到 `create_react_agent`，演示智能体按标准协议调用外部能力。
- **P12 · 多智能体协作（原生 A2A）**：用 LangGraph `StateGraph` 搭 supervisor + 多个 worker（调研员 / 写作者），并加确定性兜底保证双 worker 协作链路可被稳定演示。
- **P13 · Google A2A 标准协议**：对照官方规范实现 `AgentCard`（挂在 `/.well-known/agent-card.json`）+ JSON-RPC 2.0 `message/send`，仅用 Python 标准库 `http`，零额外依赖，演示跨进程 / 跨语言的智能体互联。

## 快速开始 / Quick Start

```bash
make setup        # 创建 .venv，安装 Python + Node 依赖，复制 .env
# 编辑 .env，把 LLM_PROVIDER 改成 ollama / openai / deepseek / qwen 之一
make docs-dev     # 打开 http://localhost:5173 读教程
make run p=1      # 跑 Phase 1 示例（p=2..13 同理）
```

## 一键验证（进阶实战）/ One-click Verify

```bash
make setup        # 先装好环境并配好 .env
./verify.sh       # 依次验证 Phase 10 -> 13，输出每阶段的判定标记
./verify.sh 11    # 也可只验证单个 Phase
```

`verify.sh` 会对照各示例的关键输出标记判断跑通与否（LLM 输出非确定，故按标记而非具体回答判分）。

## 文档站 / Docs

- 中文：https://shadowquill.github.io/langchain-langgraph-tutorial/
- English：https://shadowquill.github.io/langchain-langgraph-tutorial/en/

## 项目定位 / Positioning

本仓库脱胎于 LangChain 官方教程的工程化封装与扩展——我据此吃透了 LangGraph 状态机、checkpoint、HITL 的底层原理，并补齐了原教程缺失的生产要素（记忆独立层、MCP 通信底座、多智能体协作、部署与可观测性）。面试中若被问「是否独立设计」，请诚实说明这一点；重点应放在你真正吃透并可深挖的原理上。

---

> 完整改动见提交历史：`97991c1`（落地 P10–P13）与 `5bde29a`（修复 P10–P12 运行 bug 并新增 `verify.sh`）。
