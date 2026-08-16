# Phase 11 · MCP 工具接口：让智能体调用标准协议工具

> 对应改进报告 P0「MCP 工具接口」。源码：`examples/common/mcp_server.py`、`examples/p11/hello_chain.py`。
> 需先 `pip install mcp langchain-mcp-adapters`。

## 为什么要做 MCP 接口

之前的工具是写死在 Agent 代码里的 `@tool`。生产里工具往往来自**外部系统 / 另一个智能体**，
不应硬编码。MCP（Model Context Protocol）是智能体互联的热点协议，把「工具提供方」与「工具调用方」
解耦：换工具、换服务器只改连接配置，不改 Agent 代码。

## 工具服务器（标准 MCP）

`examples/common/mcp_server.py` 用官方 `mcp` SDK 暴露两个工具：

```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("langgraph-course-tools")

@mcp.tool()
def get_weather(city: str) -> str:
    """查询指定城市的当前天气。"""
    ...

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## Agent 端接入（langchain-mcp-adapters）

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from examples.common.llm import get_chat_model

client = MultiServerMCPClient({
    "course-tools": {"command": sys.executable,
                     "args": ["-m", "examples.common.mcp_server"],
                     "transport": "stdio"},
})
tools = await client.get_tools()        # 以子进程拉起服务器、加载工具
agent = create_react_agent(get_chat_model(), tools)
```

之后可把 `mcp_server.py` 换成任意第三方 MCP 服务器（天气、数据库、企业内部 API），Agent 零改动。

## 运行

```bash
make run p=11
# 或 python -m examples.p11.hello_chain
```

## 小结

- MCP 把「工具提供方」与「工具调用方」解耦：换工具 / 换服务器只改连接配置，不改 Agent 代码。
- 本教程用 `langchain-mcp-adapters` 以 stdio 拉起内置 `mcp_server.py`；生产可换成任意第三方 MCP 服务器（天气、数据库、企业内部 API）。
- 注意：`create_react_agent` 底层就是一张状态图——这正是 LangGraph「状态图 + 节点 + 条件边」范式在工具调用上的落地。
