# Phase 8 · 生产部署实战：从图到服务

> 目标：把前面学到的图、工具、HITL、持久化，真正变成「能被别人调用的服务」。这一章走通「服务化 → 容器化 → 可观测」最后一公里。

## 1) 服务化：用 FastAPI 暴露图

Phase 6 的图是 `graph.invoke(...)` 跑在脚本里。生产环境要的是「一个 HTTP 接口，谁都能调」。示例 `examples/p8/serve.py` 用 FastAPI 把「研究员→写手→审校」图包成 `/run` 接口：

```python
GRAPH = build_graph_with_checkpointer()   # 带持久化的编译图

@app.post("/run")
def run_crew(payload: dict):
    config = {"configurable": {"thread_id": payload["thread_id"]}}
    return GRAPH.invoke({"topic": payload["topic"]}, config)
```

- **thread_id 隔离会话**：不同用户/请求用不同 `thread_id`，各自持久化（接 Phase 7 的 checkpoint）；
- **启动**：`uvicorn serve:app --port 8000`（生产用多 worker 或 gunicorn）。

```bash
cd examples && pip install -r ../requirements.txt
python -m examples.p8.serve
# 另开终端：curl -X POST localhost:8000/run -d '{"topic":"状态图的优点","thread_id":"u1"}' -H 'Content-Type: application/json'
```

## 2) 容器化：用 Docker 打包（仓库已提供） {#docker}

把依赖与启动命令固化进镜像，避免「我机器上能跑」。仓库根目录已提供标准三件套：

- `Dockerfile`：基于 `python:3.11-slim`，装依赖后直接用 `uvicorn examples.p8.serve:app` 拉起服务；
- `docker-compose.yml`：一键编排，`env_file: .env` 自动注入 LLM key / Langfuse 等环境变量；
- `.dockerignore`：排除 `node_modules`、`docs`、`.env` 等，缩小镜像。

本地一键起服务：

```bash
docker compose up --build
# 另开终端验证
curl -X POST localhost:8000/run \
  -H 'Content-Type: application/json' \
  -d '{"topic":"状态图的优点","thread_id":"u1"}'
```

镜像是平台无关的——本地能跑，上云也只是「把镜像交给平台」。下一节就把它部署到 CloudBase。

## 3) 可观测性：看见每一步

生产环境必须能回答：「哪次调用慢了？哪条链路报错了？哪个节点最贵？」示例 `examples/p8/observability.py` 演示把可观测平台接到 `graph.invoke` 的 `callbacks` 上：

- **LangSmith**（官方 SaaS）：配 `LANGCHAIN_TRACING_V2` / `LANGCHAIN_API_KEY` 后自动上报；
- **Langfuse**（开源 / 可自托管）：用 `CallbackHandler` 显式传入 callbacks。

两种都不绑定框架——这正是「图范式」的好处：**同一张图，换可观测后端只是换一个 callback**。

## 4) 和 CrewAI / AutoGen 方案对照

| 维度 | LangGraph（本项目） | CrewAI | AutoGen |
|------|---------------------|--------|---------|
| 编排模型 | 显式状态图 | 角色流水线 | 对话群聊 |
| 持久化/HITL | 一等公民（checkpointer/interrupt） | 需自行接 | 需自行接 |
| 可观测 | 原生 callback 生态 | 较弱 | 较弱 |
| 适用 | 复杂、可控、需审计的流程 | 轻量多角色写作 | 多角色协商 |

结论回到核心主张：**它们底层都是图**。LangGraph 只是把「图」作为一等公民显式建模，因此在持久化、HITL、可观测这些生产诉求上更顺手。选哪个，取决于你对「可控性」的要求。

## 5) 云部署：CloudBase Run（推荐） {#cloud-deploy}

项目决策（2026-08-04）：云部署平台选 **CloudBase（CloudBase Run / 云托管）** 作为 FastAPI 服务的主目标，理由是它能**直接吃下我们刚打好的 Docker 镜像**，一条命令上线；文档站（VitePress 构建产物）则可选 **EdgeOne** 做边缘加速 / CDN，二者同属一个生态、国内可用。

### 用 CloudBase Framework 部署（推荐，可复现）
仓库根已提供 `cloudbase.json`，声明一个 CloudBase Run 容器服务：

```json
{
  "envId": "<your-cloudbase-env-id>",
  "framework": {
    "name": "langgraph-crew",
    "plugins": {
      "crew-service": {
        "use": "@cloudbase/framework-plugin-container",
        "inputs": {
          "serviceName": "crew-service",
          "serviceType": "cloudrun",
          "dockerfilePath": "Dockerfile",
          "containerPort": 8000,
          "buildDir": ""
        }
      }
    }
  }
}
```

部署步骤：

```bash
npm install -g @cloudbase/cli     # 安装 CloudBase CLI
tcb login                          # 浏览器授权登录
tcb framework deploy               # 按 cloudbase.json 构建镜像并部署到 CloudBase Run
```

部署完成后会得到一个公网访问地址（形如 `https://<service>.api.tcloudbase.com`），直接 `curl` 即可。也可在 CloudBase 控制台用同样的方式绑定镜像仓库（TCR）手动创建服务。

> 注：CLI 子命令随版本演进，若 `tcb framework deploy` 不可用，以 `tcb -h` 或官方文档为准。

### EdgeOne：给文档站做边缘加速（可选）
VitePress 构建产物在 `docs/.vitepress/dist`，可部署到 **EdgeOne Pages / Makers** 或 CloudBase 静态托管，由 EdgeOne 提供全球 CDN 与边缘缓存，让文档访问更快、更稳。步骤从略，核心就是把 `dist/` 目录推上去并绑定域名。

---

## 验收清单

- [ ] 能描述「图 → FastAPI 服务」需要哪些改动
- [ ] 理解 thread_id 如何隔离会话并与 checkpoint 配合
- [ ] 能写出最小 Dockerfile 与可观测 callback 接线
- [ ] 能讲清本项目与 CrewAI/AutoGen 在生产诉求上的差异

## 下一步

Phase 9：**Capstone 多 Agent 系统 + 全景复盘**。把全部知识整合进一个可运行的端到端多 Agent 应用，并对 9 个 Phase 做一次知识闭环总结，给出后续进阶路线。

## 扩展示例 / Extra Example {#extra-p8}

### 流式 API（examples/p8/streaming_api.py）
在 FastAPI 服务上增加 SSE 流式返回，让前端逐字渲染模型输出。

```bash
python -m examples.p8.streaming_api
```

