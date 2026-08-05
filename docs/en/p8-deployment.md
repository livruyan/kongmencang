# Phase 8 · Production Deployment: From Graph to Service

> Goal: turn the graphs, tools, HITL, and persistence learned so far into something *others can call*. This chapter closes the "serviceize → containerize → observe" last mile.

## 1) Serviceize: expose the graph with FastAPI

The Phase 6 graph runs via `graph.invoke(...)` in a script. Production wants "an HTTP endpoint anyone can call". Example `examples/p8/serve.py` wraps the "Researcher → Writer → Reviewer" graph into a `/run` endpoint:

```python
GRAPH = build_graph_with_checkpointer()   # compiled graph with persistence

@app.post("/run")
def run_crew(payload: dict):
    config = {"configurable": {"thread_id": payload["thread_id"]}}
    return GRAPH.invoke({"topic": payload["topic"]}, config)
```

- **thread_id isolates sessions**: different users/requests use different `thread_id`, each persisted (ties back to Phase 7 checkpointing);
- **Run**: `uvicorn serve:app --port 8000` (use multiple workers or gunicorn in production).

```bash
cd examples && pip install -r ../requirements.txt
python -m examples.p8.serve
# another shell: curl -X POST localhost:8000/run -d '{"topic":"benefits of state graphs","thread_id":"u1"}' -H 'Content-Type: application/json'
```

## 2) Containerize: package with Docker (provided in repo) {#docker}

Pin dependencies and the start command into an image to avoid "works on my machine". The repo root already ships the standard trio:

- `Dockerfile`: based on `python:3.11-slim`, installs deps then launches the service via `uvicorn examples.p8.serve:app`;
- `docker-compose.yml`: one-command orchestration, `env_file: .env` auto-injects LLM keys / Langfuse vars;
- `.dockerignore`: excludes `node_modules`, `docs`, `.env`, etc. to keep the image small.

Run locally with one command:

```bash
docker compose up --build
# in another shell
curl -X POST localhost:8000/run \
  -H 'Content-Type: application/json' \
  -d '{"topic":"benefits of state graphs","thread_id":"u1"}'
```

The image is platform-agnostic — if it runs locally, shipping it to the cloud is just "handing the image to a platform". The next section deploys it to CloudBase.

## 3) Observability: see every step

In production you must answer: "which call was slow? which trace errored? which node was costliest?" Example `examples/p8/observability.py` shows wiring an observability platform into `graph.invoke`'s `callbacks`:

- **LangSmith** (official SaaS): auto-reports after setting `LANGCHAIN_TRACING_V2` / `LANGCHAIN_API_KEY`;
- **Langfuse** (open-source / self-hostable): pass `CallbackHandler` explicitly into callbacks.

Neither binds you to a framework — another perk of the graph paradigm: **the same graph, swap observability backend by swapping one callback**.

## 4) Comparing with CrewAI / AutoGen

| Dimension | LangGraph (this project) | CrewAI | AutoGen |
|-----------|--------------------------|--------|---------|
| Orchestration | explicit state graph | role pipeline | conversation chat |
| Persistence/HITL | first-class (checkpointer/interrupt) | wire yourself | wire yourself |
| Observability | native callback ecosystem | weaker | weaker |
| Best for | complex, controllable, auditable flows | lightweight multi-role writing | multi-role negotiation |

Conclusion returns to the central claim: **they're all graphs underneath**. LangGraph just models "graph" as a first-class citizen, so it's more natural for production needs like persistence, HITL, and observability. Which to pick depends on how much control you need.

## 5) Cloud deploy: CloudBase Run (recommended) {#cloud-deploy}

Decision (2026-08-04): the cloud target is **CloudBase (CloudBase Run / 云托管)** for the FastAPI service, because it **consumes our Docker image directly** — one command to go live. The docs site (VitePress build output) can optionally use **EdgeOne** for edge acceleration / CDN; both are in the same ecosystem and work in China.

### Deploy with CloudBase Framework (recommended, reproducible)
The repo root ships `cloudbase.json`, declaring a CloudBase Run container service:

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

Deploy steps:

```bash
npm install -g @cloudbase/cli     # install CloudBase CLI
tcb login                          # authorize via browser
tcb framework deploy               # build image & deploy to CloudBase Run per cloudbase.json
```

After deployment you get a public URL (e.g. `https://<service>.api.tcloudbase.com`) — just `curl` it. You can also bind an image registry (TCR) and create the service manually in the CloudBase console.

> Note: CLI subcommands evolve; if `tcb framework deploy` is unavailable, fall back to `tcb -h` or the official docs.

### EdgeOne: edge acceleration for the docs site (optional)
VitePress build output lives in `docs/.vitepress/dist`. Deploy it to **EdgeOne Pages / Makers** or CloudBase static hosting, and let EdgeOne provide global CDN + edge caching so the docs load faster and more reliably. Steps omitted; the gist is pushing `dist/` and binding a domain.

---

## Acceptance checklist

- [ ] Can describe what changes are needed to go "graph → FastAPI service"
- [ ] Understand how thread_id isolates sessions and pairs with checkpointing
- [ ] Can write a minimal Dockerfile and observability callback wiring
- [ ] Can explain this project's production differences vs CrewAI/AutoGen

## Next

Phase 9: **Capstone multi-Agent system + full retrospective**. Integrate everything into one runnable end-to-end multi-Agent app, and close the loop with a 9-Phase knowledge review plus a next-steps roadmap.

## Extra Example {#extra-p8}

### Streaming API (examples/p8/streaming_api.py)
Add SSE streaming on top of the FastAPI service so the UI can render model output token-by-token.

```bash
python -m examples.p8.streaming_api
```

