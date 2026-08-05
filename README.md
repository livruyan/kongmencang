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
make run p=1      # 运行 Phase 1 示例（p=2..9 同理）
make lint         # 对所有示例做语法校验
```

> **IDE 用法（PyCharm + WebStorm）**：Python 代码用 PyCharm 打开项目根目录即可识别 `examples/`；文档站用 WebStorm 打开 `docs/`，或在 PyCharm 终端跑 `make docs-dev`。两者都自带 Terminal，可直接执行上面的 `make` 命令。
>
> 开发环境要求：Python 3.13+、Node 22+。

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
