# Phase 13 · A2A Standard Protocol (Google Agent-to-Agent)

## Why

Phase 12 used a native LangGraph multi-agent (supervisor + worker) to demonstrate "agent calls agent" — but that happens **inside one process**, orchestrated by a shared state graph.

In production, agents often run in **different processes, machines, or even companies**: a "researcher agent" hosted by company A, a "writer agent" hosted by company B. To call each other they cannot share memory — they need a **standard protocol**. That is Google's **A2A (Agent-to-Agent) protocol**: let arbitrary agents "discover each other, submit tasks, and get results back", independent of framework.

> One-liner: **MCP = agent ↔ tool; Phase 12 = agent ↔ agent (in-process); Phase 13 = agent ↔ agent (cross-process, standard protocol).**

This Phase implements a minimal, spec-faithful A2A server/client from scratch (zero extra dependencies) so you can see exactly what travels on the wire; for production, swap in the official `a2a-sdk`.

## What

The A2A protocol boils down to three things:

1. **Agent Card**: each agent exposes a JSON card over HTTP describing "who I am, what I can do (skills), and how to reach me (url, capabilities, input/output modes)". The card is served at `/.well-known/agent-card.json` by default.
2. **JSON-RPC 2.0 transport**: requests `{jsonrpc:"2.0", id, method, params}`, responses `{jsonrpc:"2.0", id, result}` or `{..., error}`. The most common method is `message/send` (non-streaming).
3. **Message data model**: `{role:"user"|"agent", parts:[{type:"text", text:"..."}]}` — a message is made of "parts" (text / file / data).

A typical exchange:

```
Client                                A2A Server (writer agent)
   │  GET /.well-known/agent-card.json │
   │ ─────────────────────────────────> │  returns AgentCard (name/skills/capabilities)
   │ <───────────────────────────────── │
   │  POST /  {jsonrpc, method:"message/send", params:{message:{...}}} │
   │ ─────────────────────────────────> │  runs the real LLM
   │ <───────────────────────────────── │  returns result:{role:"agent", parts:[...]}
```

## How

### 1. Agent Card (`a2a_server.py`)

```python
def make_agent_card() -> dict:
    return {
        "name": "LangGraph Writing Assistant",
        "description": "Expands points/questions into fluent prose.",
        "version": "1.0.0",
        "url": "http://127.0.0.1:9999",
        "capabilities": {"streaming": False, "pushNotifications": False},
        "defaultInputModes": ["text/plain"],
        "defaultOutputModes": ["text/plain"],
        "skills": [
            {"id": "expand", "name": "Expand into prose",
             "examples": ["Turn these points into a paragraph: ..."]}
        ],
    }
```

### 2. Server handles `message/send` (JSON-RPC 2.0)

```python
class A2AHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        req = json.loads(self.rfile.read(...))
        method = req.get("method")
        if method == "message/send":
            user_text = _extract_text(req["params"]["message"])
            answer = run_agent(user_text)          # call the real LLM
            result = {"role": "agent",
                      "parts": [{"type": "text", "text": answer}],
                      "messageId": uuid.uuid4().hex}
            self._send_json(200, {"jsonrpc": "2.0", "id": req["id"], "result": result})
```

### 3. Client: discover → send → receive (`hello_chain.py`)

```python
card = http_json(f"{base}/.well-known/agent-card.json")   # 1. discover
request = {"jsonrpc": "2.0", "id": "p13-demo-1",
           "method": "message/send",
           "params": {"message": {"role": "user",
                                  "parts": [{"type": "text", "text": question}]}}}
response = http_json(base, method="POST", payload=request)  # 2. send task
# 3. read the agent's answer from response["result"]["parts"]
```

The client does **not care** whether the server is LangChain, LangGraph, or another framework — that decoupling is exactly the value of A2A.

## Run

One-shot (the script starts the server in a background thread, then talks to it as a client):

```bash
make run p=13
# or python -m examples.p13.hello_chain
```

Or run manually in two terminals (closer to real cross-process):

```bash
# terminal 1: start the server
python -m examples.p13.a2a_server
# terminal 2: call it as a client, pointing A2A_BASE_URL at the remote server
A2A_BASE_URL=http://127.0.0.1:9999 python -m examples.p13.hello_chain
```

Typical output:

```
===== Agent Card discovered =====
Name: LangGraph Writing Assistant
Description: Expands points/questions into fluent prose.
Skills: ['Expand into prose']
Version: 1.0.0

===== Sending A2A request (message/send) =====
User: explain what an Agent is to a non-technical person in three sentences

===== Agent answer =====
An agent is like a digital assistant that understands you and figures out how to finish the task...
```

## Summary

- A2A = Agent Card (discovery) + JSON-RPC 2.0 (transport) + Message (data model), framework-agnostic, built for "cross-process / cross-org agent interconnection".
- This Phase implements its minimal equivalent from scratch and runs via `make run`; the data shapes are aligned with the official spec, and production can swap in `a2a-sdk`.
- By now the full agent-interconnection picture is assembled: **P11 MCP (agent↔tool) → P12 native multi-agent (agent↔agent, in-process) → P13 A2A (agent↔agent, cross-process standard protocol)**.
- Next steps: `message/stream` (SSE streaming), `tasks/get` / `tasks/cancel` (long-task state machine), auth (the `authentication` field in Agent Card + OAuth/mTLS), and the official `a2a-sdk`'s gRPC/REST transports.
