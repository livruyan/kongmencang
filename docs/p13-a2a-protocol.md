# Phase 13 · A2A 标准协议（Google Agent-to-Agent Protocol）

## 为什么需要它（Why）

Phase 12 用 LangGraph 原生多智能体（supervisor + worker）演示了「智能体调用智能体」——但那是在**同一个进程**里，靠一张共享状态图编排。

生产里，智能体往往跑在**不同进程、不同机器、甚至不同公司**：一个「调研智能体」由 A 公司托管，一个「写作智能体」由 B 公司托管，它们要互相调用，就不能共享内存，必须走**标准协议**。这就是 Google 提出的 **A2A（Agent-to-Agent）协议**——让任意智能体之间「发现彼此、发起任务、拿回结果」，与框架无关。

> 一句话区分：**MCP = agent ↔ tool（接工具），Phase 12 = agent ↔ agent（进程内），Phase 13 = agent ↔ agent（跨进程、标准协议）。**

本 Phase 从零实现 A2A 协议的最小等价物（零额外依赖），让你看清协议在线上真正传输的东西；生产可直接换官方 `a2a-sdk`。

## 是什么（What）

A2A 协议的核心就三件事：

1. **Agent Card（智能体名片）**：每个智能体用 HTTP 暴露一张 JSON 卡片，写清「我是谁、能干什么（skills）、怎么连我（url、capabilities、input/output modes）」。卡片默认挂在 `/.well-known/agent-card.json`。
2. **JSON-RPC 2.0 传输**：请求 `{jsonrpc:"2.0", id, method, params}`，响应 `{jsonrpc:"2.0", id, result}` 或 `{..., error}`。最常用的方法是 `message/send`（非流式）。
3. **Message 数据模型**：`{role:"user"|"agent", parts:[{type:"text", text:"..."}]}`——消息由若干「part」（文本/文件/数据）组成。

一张典型交互图：

```
客户端                              A2A 服务端（写作助手）
   │  GET /.well-known/agent-card.json │
   │ ─────────────────────────────────> │  返回 AgentCard（name/skills/capabilities）
   │ <───────────────────────────────── │
   │  POST /  {jsonrpc, method:"message/send", params:{message:{...}}} │
   │ ─────────────────────────────────> │  跑真实 LLM
   │ <───────────────────────────────── │  返回 result:{role:"agent", parts:[...]}
```

## 怎么写（How）

### 1. Agent Card（`a2a_server.py`）

```python
def make_agent_card() -> dict:
    return {
        "name": "LangGraph 写作助手",
        "description": "把要点/问题扩写成通顺的中文短文。",
        "version": "1.0.0",
        "url": "http://127.0.0.1:9999",
        "capabilities": {"streaming": False, "pushNotifications": False},
        "defaultInputModes": ["text/plain"],
        "defaultOutputModes": ["text/plain"],
        "skills": [
            {"id": "expand", "name": "扩写成短文",
             "examples": ["把下面的要点写成一段话：……"]}
        ],
    }
```

### 2. 服务端处理 `message/send`（JSON-RPC 2.0）

```python
class A2AHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        req = json.loads(self.rfile.read(...))
        method = req.get("method")
        if method == "message/send":
            user_text = _extract_text(req["params"]["message"])
            answer = run_agent(user_text)          # 调真实 LLM
            result = {"role": "agent",
                      "parts": [{"type": "text", "text": answer}],
                      "messageId": uuid.uuid4().hex}
            self._send_json(200, {"jsonrpc": "2.0", "id": req["id"], "result": result})
```

### 3. 客户端：发现卡片 → 发任务 → 取结果（`hello_chain.py`）

```python
card = http_json(f"{base}/.well-known/agent-card.json")   # 1. 发现
request = {"jsonrpc": "2.0", "id": "p13-demo-1",
           "method": "message/send",
           "params": {"message": {"role": "user",
                                  "parts": [{"type": "text", "text": question}]}}}
response = http_json(base, method="POST", payload=request)  # 2. 发任务
# 3. response["result"]["parts"] 里取出 agent 的回答
```

客户端**不关心**服务端是 LangChain、LangGraph 还是别的框架——这就是 A2A 的价值：解耦。

## 跑一下（Run）

一键跑（脚本自动在后台线程起服务端，再以客户端身份对话）：

```bash
make run p=13
# 或 python -m examples.p13.hello_chain
```

也可分两个终端手动跑（更贴近真实跨进程）：

```bash
# 终端 1：起服务端
python -m examples.p13.a2a_server
# 终端 2：以客户端身份调用，通过 A2A_BASE_URL 指向远端服务端
A2A_BASE_URL=http://127.0.0.1:9999 python -m examples.p13.hello_chain
```

典型输出：

```
===== 发现 Agent Card =====
名称: LangGraph 写作助手
描述: 一个演示 A2A 标准协议的智能体：把要点/问题扩写成通顺的中文短文。
技能: ['扩写成短文']
版本: 1.0.0

===== 发送 A2A 请求（message/send）=====
用户: 用三句话向完全不懂技术的人解释：什么是 Agent？

===== 智能体回答 =====
Agent 就像一个能听懂你的话、自己想办法去完成任务的数字助手……
```

## 小结（Summary）

- A2A 协议 = Agent Card（发现）+ JSON-RPC 2.0（传输）+ Message（数据模型），与框架无关，专治「跨进程/跨组织智能体互联」。
- 本 Phase 从零实现了它的最小等价物，`make run` 即可跑通；字段结构已与官方对齐，生产可换 `a2a-sdk`。
- 到这一章，智能体互联的完整拼图已经集齐：**P11 MCP（agent↔tool）→ P12 原生多智能体（agent↔agent 进程内）→ P13 A2A（agent↔agent 跨进程标准协议）**。
- 进阶方向：`message/stream`（SSE 流式）、`tasks/get`/`tasks/cancel`（长任务状态机）、鉴权（Agent Card 里的 `authentication` 声明 + OAuth/mTLS）、以及官方 `a2a-sdk` 的 gRPC/REST 传输。
