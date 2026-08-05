# 项目文件说明 / Project File Reference

> **LangChain & LangGraph 系统化学习（开源教程）**
> 本文档逐项说明 `langchain-langgraph-course/` 内每个目录与文件的作用，并标注其 **git 版本管理归属**。
> 项目已 **中英双语完整**（中文 `docs/` 含 p1–p9 + primer + index；英文 `docs/en/` 为镜像）。

---

## 图例 / Legend

| 标记 | 含义 |
|---|---|
| ✅ `[COMMIT]` | 建议纳入 git（源码 / 配置 / 文档 / 模板） |
| 🚫 `[IGNORE]` | 生成物或依赖，应加入 `.gitignore`，不提交 |
| 🔒 `[SECRET]` | 含密钥，绝对不能提交（当前仅本地 `.env`） |

---

## 目录结构总览

```
langchain-langgraph-course/
├── LICENSE                  # Apache 2.0 协议
├── README.md                # 中文项目说明（含快速开始 / 构建）
├── README.en.md             # 英文项目说明
├── menu.md                  # 本文件：目录与文件说明
├── Makefile                 # 一键构建/运行入口
├── requirements.txt         # Python 依赖清单
├── package.json             # VitePress 文档站依赖与脚本
├── package-lock.json        # npm 锁定文件
├── .env.example             # 环境变量模板（无密钥）
├── .env                     # 本地密钥（🔒 不提交）
├── .gitignore               # git 忽略规则
├── Dockerfile               # Phase8 服务容器化
├── .dockerignore            # Docker 构建上下文排除
├── docker-compose.yml       # 本地一键起服务
├── cloudbase.json           # CloudBase Run 部署声明
├── examples/                # 26 个可运行示例（✅ 全提交）
└── docs/                    # 双语文档站（✅ 除构建产物）
```

---

## 一、顶层文件 / Top-level files

| 文件 | 作用 | git |
|---|---|---|
| `LICENSE` | Apache 2.0 开源协议，规定他人可自由使用/修改/分发 | ✅ |
| `README.md` | 中文项目说明：项目简介、快速开始、构建命令（`make`）、环境要求 | ✅ |
| `README.en.md` | 英文项目说明，与中文版镜像 | ✅ |
| `menu.md` | 本文件：项目目录与文件导航说明 | ✅ |
| `Makefile` | 一键构建/运行：`setup` / `docs` / `docs-dev` / `run p=N` / `lint` / `clean`（编辑器无关，PyCharm/WebStorm 终端通用） | ✅ |
| `requirements.txt` | Python 依赖清单（`langchain` / `langgraph` / `fastapi` / `faiss-cpu` / `langfuse` 等）。注意：`langchain>=0.3` 会被解析到 1.x 大版本，项目已迁移到 1.x 原生 Agent | ✅ |
| `package.json` | VitePress 文档站依赖与脚本（`docs:dev` / `docs:build` / `docs:preview`） | ✅ |
| `package-lock.json` | npm 锁定文件，保证依赖可复现 | ✅ |
| `.env.example` | 环境变量**模板**（无密钥），复制为 `.env` 后填写 `LLM_PROVIDER` / API Key | ✅ |
| `.env` | 本地密钥文件（含 DeepSeek/OpenAI Key）。**切勿提交** | 🔒 |
| `.gitignore` | git 忽略规则：Python/Node/VitePress 构建产物与 `.env` | ✅ |
| `Dockerfile` | 将 Phase8 的 FastAPI 服务（`examples.p8.serve:app`）打包成镜像，暴露端口 8000 | ✅ |
| `.dockerignore` | Docker 构建上下文排除：`node_modules` / `docs` / `.env` 等 | ✅ |
| `docker-compose.yml` | 本地一键起服务（`docker compose up --build`），端口 8000 | ✅ |
| `cloudbase.json` | CloudBase Run 容器部署声明（`envId` 为占位符 `<your-cloudbase-env-id>`，无密钥） | ✅ |

---

## 二、生成物与依赖（全部 🚫 `[IGNORE]`，不提交）

| 路径 | 说明 |
|---|---|
| `node_modules/` | npm 安装的依赖 |
| `.venv/` | Python 虚拟环境（`make setup` 生成） |
| `__pycache__/` `*.pyc` | Python 字节码缓存 |
| `docs/.vitepress/dist/` | 文档站构建产物（`make docs` 生成） |
| `docs/.vitepress/cache/` | VitePress 缓存 |
| `docs/.vitepress/*.timestamp-*.mjs` | VitePress 配置编译缓存（自动生成，如 `config.ts.timestamp-*.mjs`） |

> 上述规则已写入 `.gitignore`，`git add .` 时会自动跳过。

---

## 三、`examples/` —— 26 个可运行示例（全部 ✅ `[COMMIT]`）

每个 `pN/` 目录均含空 `__init__.py`（标记为 Python 包）。所有示例复用 `common/llm.py` 抽象层。

| 路径 | 作用 | Phase |
|---|---|---|
| `common/llm.py` | 统一 LLM Provider 抽象层，按 `.env` 的 `LLM_PROVIDER` 切换 `openai` / `deepseek` / `ollama` | — |
| `p1/hello_chain.py` | 第一个 Chain（LCEL 入门） | P1 |
| `p1/streaming.py` | 流式输出扩展示例 | P1 |
| `p2/compose_chain.py` | 组合链 | P2 |
| `p2/memory_chat.py` | 带记忆的对话 | P2 |
| `p2/simple_rag.py` | RAG 基础（需 embeddings；DeepSeek 无此接口，换 OpenAI 即过） | P2 |
| `p2/conversational_rag.py` | 带记忆的 RAG | P2 |
| `p3/react_loop.py` | 手写 ReAct 循环（已迁移到 1.x `create_agent`） | P3 |
| `p3/builtin_agent.py` | 内置 Agent（框架托管） | P3 |
| `p3/plan_execute.py` | Plan-and-Execute 模式 | P3 |
| `p4/custom_tools.py` | 自定义工具 | P4 |
| `p4/tool_calling_raw.py` | 原生 tool-calling 循环（规避 400 的修复版本） | P4 |
| `p4/structured_output.py` | 结构化输出（改用 `function_calling` 路径） | P4 |
| `p5/agent_router.py` | 路由 Agent | P5 |
| `p5/debate.py` | 双 Agent 辩论 | P5 |
| `p5/mini_crew.py` | 迷你 Crew（多 Agent 协作） | P5 |
| `p6/branching.py` | LangGraph 分支图 | P6 |
| `p6/router_graph.py` | 路由图 | P6 |
| `p6/crew_graph.py` | 团队图（多节点协作） | P6 |
| `p7/hitl_approve.py` | Human-in-the-loop 审批（`interrupt`） | P7 |
| `p7/persistence.py` | 状态持久化（`MemorySaver`） | P7 |
| `p7/time_travel.py` | 时间旅行（状态回溯） | P7 |
| `p8/serve.py` | FastAPI 服务（Docker 入口 `app`） | P8 |
| `p8/streaming_api.py` | SSE 流式 API | P8 |
| `p8/observability.py` | Langfuse 可观测性（主路线） | P8 |
| `p9/capstone.py` | 综合 Capstone 端到端系统 | P9 |
| `p9/eval_pipeline.py` | 简易评测流水线 | P9 |

> **验收结果**：26 示例 = 24 通过 / 2 受限（P2 RAG，受 DeepSeek 无 embeddings 限制，非缺陷）/ 0 缺陷。

---

## 四、`docs/` —— 双语文档站（✅ `[COMMIT]` 除构建产物）

| 路径 | 作用 |
|---|---|
| `index.md` | 中文首页（项目简介 + 核心主张） |
| `primer.md` | Python / LLM 速补前置（可选） |
| `p1-hello-chain.md` … `p9-capstone.md` | 9 个 Phase 中文文档 |
| `en/index.md` `en/primer.md` `en/p1-hello-chain.md` … `en/p9-capstone.md` | 英文镜像（完整 9 Phase） |
| `.vitepress/config.ts` | 站点配置：导航（`nav`）+ 侧边栏（`zhSidebar` / `enSidebar`）+ 构建参数。**注意：中英文 nav/sidebar 需同步维护** |
| `.vitepress/dist` `cache` `*.timestamp-*.mjs` | 🚫 构建产物（见第二节） |

> **学习重点**：`p3-agent-principles.md`（ReAct 原理，图思维种子）→ `p6-langgraph.md`（状态图/节点/条件边，点明各框架共通本质）→ `p9-capstone.md`（全景复盘）。

---

## 五、`.gitignore`（已落盘，直接可用）

```gitignore
# ===== Python =====
__pycache__/
*.py[cod]
*.egg-info/
.pytest_cache/

# Virtual environments (managed by `make setup`)
.venv/
venv/
env/

# ===== Node / VitePress =====
node_modules/
docs/.vitepress/dist/
docs/.vitepress/cache/
docs/.vitepress/*.timestamp-*.mjs

# ===== Secrets (NEVER commit real keys) =====
.env
.env.local
.env.*.local

# ===== Build / OS / Editor =====
.DS_Store
*.log
.idea/
*.swp
.vscode/
```

---

## 六、git 提交清单

```bash
# 一次性添加所有应提交的内容：
git add LICENSE README.md README.en.md menu.md Makefile \
        requirements.txt package.json package-lock.json \
        .env.example .gitignore Dockerfile .dockerignore \
        docker-compose.yml cloudbase.json \
        examples docs

# 切勿提交：
#   .env  node_modules/  .venv/  __pycache__/  docs/.vitepress/dist/

# 首次提交示例：
#   git init && git add -A -- :/node_modules :/.venv :/.env
#   （或先用上面的显式清单，更安全）
```
