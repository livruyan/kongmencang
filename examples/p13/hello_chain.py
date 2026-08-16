"""
Phase 13 · A2A 标准协议（Google Agent-to-Agent Protocol）—— 客户端 + 一键演示
=========================================================================
目的：演示「智能体通过标准 A2A 协议跨进程互联」。与 Phase 12 的 LangGraph 原生
多智能体（进程内 supervisor + worker）不同，本 Phase 的客户端与服务端是两个独立
HTTP 进程，通过 A2A 协议（Agent Card 发现 + JSON-RPC 2.0）通信：
  1. 客户端先 GET 服务端的 Agent Card（「智能体名片」）；
  2. 客户端据此构造 JSON-RPC message/send 请求；
  3. 服务端跑真实 LLM，把回答封装成 A2A Message 返回。

本脚本默认把服务端起在本进程后台线程里，实现「一条命令跑完整个 A2A 对话」；
也可以设置 A2A_BASE_URL 指向一个已在跑的远端服务端，模拟真实跨进程调用（见文档）。

运行 / Run:
    python -m examples.p13.hello_chain                 # 一键：自带服务端
    A2A_BASE_URL=http://127.0.0.1:9999 python -m examples.p13.hello_chain  # 连远端服务端
    # 或 make run p=13
"""
import json
import os
import threading
import urllib.request

from examples.p13.a2a_server import start_server


def http_json(url: str, method: str = "GET", payload: dict | None = None) -> dict:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> None:
    # 1) 决定连接哪个服务端：默认本进程后台拉起；否则连 A2A_BASE_URL 指向的远端
    base = os.environ.get("A2A_BASE_URL")
    server = None
    if base is None:
        server = start_server()
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_port}"
        print(f"[本进程已拉起 A2A 服务端：{base}]")
    else:
        base = base.rstrip("/")

    try:
        # 2) 发现 Agent Card —— 这就是 A2A 的「智能体名片」
        card = http_json(f"{base}/.well-known/agent-card.json")
        print("===== 发现 Agent Card =====")
        print(f"名称: {card['name']}")
        print(f"描述: {card['description']}")
        print(f"技能: {[s['name'] for s in card['skills']]}")
        print(f"版本: {card['version']}")

        # 3) 构造 JSON-RPC message/send 请求，发给服务端智能体
        question = "用三句话向完全不懂技术的人解释：什么是 Agent？"
        request = {
            "jsonrpc": "2.0",
            "id": "p13-demo-1",
            "method": "message/send",
            "params": {
                "message": {
                    "role": "user",
                    "parts": [{"type": "text", "text": question}],
                }
            },
        }
        print(f"\n===== 发送 A2A 请求（message/send）=====\n用户: {question}\n")
        response = http_json(base, method="POST", payload=request)

        # 4) 解析 A2A Message 结果
        if "result" in response:
            parts = response["result"]["parts"]
            answer = "\n".join(p.get("text", "") for p in parts if p.get("type") == "text")
            print(f"===== 智能体回答 =====\n{answer}")
        else:
            print(f"===== 出错 =====\n{response.get('error')}")
    finally:
        if server is not None:  # 远端模式下不关闭别人的服务端
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    main()
