# Changelog

本项目采用语义化版本（SemVer）。所有重要变更记录于此。

## [v1.0.2] — 2026-08-17

> 修复 `verify.sh` 在后台运行时的稳定性问题，并补齐全量发布文档。

### 修复 / Fixed
- **修复 `verify.sh` 后台启动时 Phase 11 偶发失败**：原脚本用 `make run` 在后台子 shell 启动示例，上层 shell 退出时向进程组发 `SIGHUP`，`make` 会直接挂掉（`Hangup: 1`），而会拉起子进程（MCP server）的 Phase 11 最先中招。改为直接用 `nohup ./.venv/bin/python -m examples.pXX.hello_chain` 调用，绕过 `make`，`nohup` 让进程组忽略 `SIGHUP`。复跑确认 Phase 10–13 **通过 4 / 未通过 0**。

### 文档 / Docs
- 新增 `CHANGELOG.md` 的 v1.0.2 记录（即本段）。
- 仓库内 `RELEASE.md` 标题对齐为 v1.0.2 并补充修复说明。

### 标签说明 / Tags
- `v1.0.2`：指向当前 `main` 头 `246d953`，为最新完整发布（**Latest**）。
- `v1.0.1`：上一版完整发布（Phase 10–13 首次补齐）。
- `v1.0.0`：早期 P1–P9 基线快照，作为历史保留。

---

## [v1.0.1] — 2026-08-17

> 在 v1.0.0（P1–P9 基线）之上补齐生产级进阶实战，形成完整的 13 Phase 课程。

### 新增 / Added
- **Phase 10 · 可溯源记忆独立层**：独立的语义记忆库，字符级 n-gram 重合召回（阈值 ≥2 过滤偶然单字重合），每次回答带「来源溯源」，从机制上抑制记忆层张冠李戴式幻觉。
- **Phase 11 · MCP 标准协议工具接口**：启动真实 MCP server（stdio），用 `langchain-mcp-adapters` 把 MCP 工具挂到 `create_react_agent`，演示智能体按标准协议调用外部能力。
- **Phase 12 · 多智能体协作（LangGraph 原生 A2A）**：`StateGraph` 搭 supervisor + 多 worker（调研员 / 写作者），加确定性兜底保证双 worker 协作链路稳定可演示。
- **Phase 13 · Google A2A 标准协议**：对照官方规范实现 `AgentCard`（挂 `/.well-known/agent-card.json`）+ JSON-RPC 2.0 `message/send`，仅用 Python 标准库 `http`，零额外依赖，演示跨进程 / 跨语言智能体互联。
- **`verify.sh` 一键验证脚本**：自动跑通 Phase 10–13，对照各示例关键输出标记判分（不依赖非确定的 LLM 回答）。
- 仓库内可复制发布文案 `RELEASE.md`。

### 修复 / Fixed
- 修正 Phase 10 中文检索失效（FTS5 整句 MATCH 改为 n-gram 重合召回）。
- 修正 Phase 11 `NotImplementedError`（MCP 工具异步，改为 `await agent.ainvoke`）。
- 修正 Phase 12 路由只到调研员（加确定性兜底，保证调研员→写作者→结束链路）。
- 修正 `verify.sh` 在 macOS 上的兼容问题（无 GNU `timeout`，改用后台进程 + `wait` 实现超时）。

### 文档 / Docs
- 双语文档站新增 Phase 10–13 四篇讲解（`docs/` 中英文）。
- `docs/.vitepress/config.ts` 中英文导航 / 侧边栏补齐 Phase 10–13。
- 新增 `CHANGELOG.md`。

---

## [v1.0.0] — 基线

> 从零到生产的 LangChain / LangGraph 多智能体系统实战教程（P1–P9）。

### 特性
- 9 个循序渐进阶段（P1–P9）：每个阶段配「原理讲解 + 可运行示例 + 验收清单」。
- 统一运行时抽象层 `examples/common/llm.py`：一行 `LLM_PROVIDER` 切换 Ollama / OpenAI / DeepSeek。
- 双语文档站（VitePress + GitHub Pages），中文为主、英文 `/en/` 同步。
- `Makefile` 一键工程化：`make setup / run / docs / docs-dev / lint`。
- `make lint` 全量语法校验。

### 涵盖主题
P1 第一个 Chain · P2 组合链/记忆/RAG · P3 Agent 原理 · P4 Tools · P5 多 Agent 对比 · P6 LangGraph 图编排 · P7 HITL 与持久化 · P8 生产部署 · P9 Capstone 与复盘。
