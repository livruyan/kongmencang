# Phase 11 · MCP Tool Interface: let Agents call standard-protocol tools

> Maps to report P0 "MCP tool interface". Source: `examples/common/mcp_server.py`, `examples/p11/hello_chain.py`.
> Requires `pip install mcp langchain-mcp-adapters`.

## Why MCP

Earlier tools were hardcoded `@tool` inside the Agent. In production, tools often come from **external
systems / another Agent** and should not be hardcoded. MCP (Model Context Protocol) is the hot protocol
for Agent interconnection: it decouples tool provider from tool caller — swap a server via config, no Agent change.

## Tool server (standard MCP)

```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("langgraph-course-tools")

@mcp.tool()
def get_weather(city: str) -> str:
    """Query current weather for a city."""
    ...

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## Agent side (langchain-mcp-adapters)

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

client = MultiServerMCPClient({
    "course-tools": {"command": sys.executable,
                     "args": ["-m", "examples.common.mcp_server"],
                     "transport": "stdio"},
})
tools = await client.get_tools()
agent = create_react_agent(get_chat_model(), tools)
```

You can later replace `mcp_server.py` with any third-party MCP server (weather, DB, internal API) with zero Agent changes.

## Run

```bash
make run p=11
```

## Summary

- MCP decouples tool provider from tool caller: swap a tool / server via config, no Agent code change.
- This tutorial uses `langchain-mcp-adapters` to launch the built-in `mcp_server.py` over stdio; in production you can point it at any third-party MCP server (weather, DB, internal API).
- Note: `create_react_agent` is itself a state graph under the hood — exactly the "state graph + node + conditional edge" paradigm applied to tool calling.
