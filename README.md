# LangChain & LangGraph 系统化学习

> 从底层范式理解 Agent 编排：**状态图 + 节点 + 条件边**。

本项目是一个面向「会基础编程、但没碰过 LLM/Agent」开发者的开源学习项目，目标是帮你从根本上理解 Agent 的工作原理，为构建复杂应用打基础。

我们认为：市面主流 Agent 框架（CrewAI、AutoGen 等）的底层逻辑，都可以映射到 LangGraph 的 **状态图（StateGraph）+ 节点（Node）+ 条件边（Conditional Edge）** 模型。掌握 LangChain 与 LangGraph，就等于掌握了 Agent 编排的底层范式。

## 语言 / Language

- 本文档提供**双语**：简体中文（默认）与 English（`/en/`）。
- This project is **bilingual**: Simplified Chinese (default) and English (`/en/`).

## 快速开始（推荐一键）

本仓库提供**编辑器无关**的 `Makefile`，在 PyCharm / WebStorm 终端、VS Code 或 CI 中都能直接运行：

```bash
make setup        # 创建 .venv 并安装 Python + Node 依赖，复制 .env
make docs         # 构建双语文档站 -> docs/.vitepress/dist
make docs-dev     # 本地实时预览 http://localhost:5173
make run p=1      # 运行 Phase 1 示例（p=2..9 同理，需先配置 .env，见下方「配置大模型」）
make lint         # 对所有示例做语法校验
```

💡 **环境就绪后，先看文档再动手（推荐）**：上面 `make setup` 装好 Node 依赖后，运行 `make docs-dev`（或 `npm run docs:dev`）即可在浏览器打开 **http://localhost:5173** 阅读教程——文档站对每个 Phase 的原理、代码、验收清单都有详细说明。建议按 Phase 顺序读完对应章节，再回来 `make run p=N` 跑示例，效果更佳。

> **IDE 用法（PyCharm + WebStorm）**：Python 代码用 PyCharm 打开项目根目录即可识别 `examples/`；文档站用 WebStorm 打开 `docs/`，或在 PyCharm 终端跑 `make docs-dev`。两者都自带 Terminal，可直接执行上面的 `make` 命令。
>
> 开发环境要求：Python 3.13+、Node 22+。

## 配置大模型（.env）

> ⚠️ **运行示例前必须完成这一步。** 上面的 `make setup` 已经自动从 `.env.example` 复制出了 `.env`，但它的默认值是 `LLM_PROVIDER=ollama`——如果你没启动本地 Ollama 就直接 `make run`，会报 `httpx.ConnectError: [Errno 61] Connection refused`。请按下面二选一编辑 `.env`（例如 `nano .env` 或直接在编辑器打开），再回来跑示例。

### 方式 A：本地 Ollama（推荐新手，免费、零 key）

1. 安装 Ollama：Homebrew `brew install ollama`，或前往 <https://ollama.com> 下载 App。
2. 启动服务：打开 Ollama App 即自动后台启动；命令行则 `ollama serve &`。
3. 拉取模型：
   ```bash
   ollama pull qwen2.5:7b        # 对话模型（Phase 1–9 通用）
   ollama pull nomic-embed-text  # 嵌入模型（Phase 2 RAG 章节需要）
   ```
4. 在 `.env` 中确认：
   ```ini
   LLM_PROVIDER=ollama
   ```
5. 验证服务已起来：
   ```bash
   curl http://localhost:11434     # 返回 "Ollama is running" 即正常
   ```

### 方式 B：云端 API（OpenAI / DeepSeek）

编辑 `.env`，二选一：

```ini
# DeepSeek（便宜、国内可达，推荐）
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=你的key

# 或 OpenAI
# LLM_PROVIDER=openai
# OPENAI_API_KEY=你的key
```

> 用云端 API 时无需安装/启动 Ollama，示例会直接走官方或兼容接口。配置好 `.env` 后即可 `make run p=N`。

下面章节为等价的手动步骤。

## 学习路线（9 个 Phase）

| Phase | 主题 |
|-------|------|
| 1 | LangChain 核心概念与开发环境（含可跳过速补） |
| 2 | Chains、Memory 与 RAG 基础 |
| 3 | Agent 原理：从 ReAct 到自主循环 |
| 4 | Tools 与 Function Calling |
| 5 | 多 Agent 协作范式与主流框架对比 |
| 6 | LangGraph 图编排核心 |
| 7 | 状态、记忆与 Human-in-the-loop |
| 8 | 生产部署实战 |
| 9 | Capstone 综合实战与全景复盘 |

## 运行示例

1. 安装依赖：
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. 复制并配置环境变量：
   ```bash
   cp .env.example .env
   # 编辑 .env，选择 LLM_PROVIDER（openai / deepseek / ollama）
   ```
3. 运行示例（以 Phase 1 为例）：
   ```bash
   python -m examples.p1.hello_chain
   ```

## 本地预览文档站

```bash
npm install
npm run docs:dev      # 开发预览
npm run docs:build    # 构建静态站
```

## 部署文档站（GitHub Pages）

文档站通过 GitHub Actions 自动构建并部署到 GitHub Pages，无需手动上传。

1. 在仓库 **Settings → Pages → Source** 选择 **GitHub Actions**（仅需设置一次）。
2. 推送 `main` 分支即触发部署：
   ```bash
   make deploy-docs   # = npm run docs:build + git push origin main
   ```
3. 部署完成后，站点地址为：
   `https://shadowquill.github.io/langchain-langgraph-tutorial/`

> 部署工作流见 `.github/workflows/deploy-docs.yml`；`docs/.vitepress/config.ts` 中的 `base` 已按仓库名 `langchain-langgraph-tutorial` 配置好，无需改动。

## 示例运行环境说明

所有示例通过一个**统一的 LLM Provider 抽象层**（`examples/common/llm.py`）切换模型：

- `openai`：官方 OpenAI（默认），需 `OPENAI_API_KEY`。
- `deepseek`：DeepSeek，OpenAI 兼容接口，需 `DEEPSEEK_API_KEY`。
- `ollama`：本地 Ollama，**免 key**，前几章推荐用于零门槛体验。

详见 `.env.example` 与各 Phase 文档。
