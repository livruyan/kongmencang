"""
Phase 13 · A2A 标准协议（Google Agent-to-Agent Protocol）—— 服务端
=========================================================================
这是一个从零实现、严格遵循 Google A2A 协议规范（a2a-protocol.org）的最小服务端：
  - 通过 HTTP 暴露 Agent Card（智能体名片，描述「我是谁、能干什么、怎么连我」）；
  - 通过 JSON-RPC 2.0 处理 message/send（非流式）任务请求；
  - 使用 examples/common/llm.py 的真实 LLM 做推理。

为什么从零写而不是直接装官方 a2a-sdk？——本教程主线是「从底层范式理解」，手写一遍
Agent Card + JSON-RPC 封装，才能真正看懂协议在线上传输的是什么。字段与结构已与官方
对齐；生产环境可直接换成 `pip install a2a-sdk`（官方 SDK），本文件即它的「最小等价物」。

协议要点（与官方规范对齐）：
  - Agent Card 暴露在 /.well-known/agent-card.json（同时兼容旧版 /.well-known/agent.json）；
  - 请求/响应遵循 JSON-RPC 2.0：{jsonrpc:"2.0", id, method, params} / {..., result|error}；
  - message/send 的 params.message = {role:"user", parts:[{type:"text", text}]}；
  - 响应 result 是一个 Message = {role:"agent", parts:[{type:"text", text}], messageId}。

运行（独立起服务，配合 examples/p13/hello_chain.py 或任意 A2A 客户端）:
    python -m examples.p13.a2a_server
"""
import json
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from langchain_core.messages import HumanMessage

from examples.common.llm import get_chat_model

AGENT_CARD_PATHS = ("/.well-known/agent-card.json", "/.well-known/agent.json")


# ---- Agent Card：A2A 的「智能体名片」 -----------------------------------------
def make_agent_card() -> dict:
    return {
        "name": "LangGraph 写作助手",
        "description": "一个演示 A2A 标准协议的智能体：把要点/问题扩写成通顺的中文短文。",
        "version": "1.0.0",
        "url": "http://127.0.0.1:9999",
        "provider": {"organization": "langchain-langgraph-tutorial"},
        "capabilities": {"streaming": False, "pushNotifications": False},
        "defaultInputModes": ["text/plain"],
        "defaultOutputModes": ["text/plain"],
        "skills": [
            {
                "id": "expand",
                "name": "扩写成短文",
                "description": "把给定的要点/问题扩写成一段通顺的中文短文",
                "tags": ["写作", "扩写"],
                "examples": ["把下面的要点写成一段话：……"],
                "inputModes": ["text/plain"],
                "outputModes": ["text/plain"],
            }
        ],
    }


def run_agent(user_text: str) -> str:
    """真实推理：调用统一的 LLM provider（同步 invoke，线程安全）。"""
    model = get_chat_model()
    prompt = (
        "你是一个写作助手。根据用户给出的要点或问题，写一段通顺、面向外行的中文短文"
        "（3-5 句）。直接给出正文，不要任何解释。\n\n用户输入：\n" + user_text
    )
    return model.invoke([HumanMessage(content=prompt)]).content


def _extract_text(message: dict) -> str:
    parts = message.get("parts", [])
    texts = [p.get("text", "") for p in parts if p.get("type") == "text"]
    return "\n".join(texts)


class A2AHandler(BaseHTTPRequestHandler):
    """A2A 协议 HTTP 处理器：Agent Card（GET） + JSON-RPC 2.0（POST）。"""

    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path in AGENT_CARD_PATHS:
            self._send_json(200, make_agent_card())
        else:
            self._send_json(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        try:
            req = json.loads(raw)
        except json.JSONDecodeError:
            self._send_json(
                200,
                {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}},
            )
            return

        rid = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        if method == "message/send":
            user_text = _extract_text(params.get("message", {}))
            answer = run_agent(user_text)
            result = {
                "role": "agent",
                "parts": [{"type": "text", "text": answer}],
                "messageId": uuid.uuid4().hex,
            }
            self._send_json(200, {"jsonrpc": "2.0", "id": rid, "result": result})
        else:
            self._send_json(
                200,
                {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}},
            )

    def log_message(self, fmt, *args):  # 关闭默认访问日志，保持输出清爽
        pass


def start_server(port: int = 9999) -> ThreadingHTTPServer:
    return ThreadingHTTPServer(("127.0.0.1", port), A2AHandler)


if __name__ == "__main__":
    server = start_server()
    print(f"A2A 服务端已启动：http://127.0.0.1:{server.server_port}")
    print(f"Agent Card 见 http://127.0.0.1:{server.server_port}/.well-known/agent-card.json")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。")
