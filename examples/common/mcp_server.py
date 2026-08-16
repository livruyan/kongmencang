"""最小 MCP 工具服务器 / Minimal MCP tool server.
=========================================================================
基于官方 mcp SDK（FastMCP）暴露标准 MCP 工具，演示「智能体通信底座」：
外部系统 / 另一个智能体可通过标准 MCP 协议调用本进程提供的工具，
而**无需把工具逻辑写死在 Agent 里**——这正是改进报告 P0「MCP 工具接口」的落点。

本服务器暴露两个工具（示例用演示数据，真实场景替换为天气 API / 搜索 API）：
  - get_weather(city) : 查询城市天气
  - web_search(query) : 模拟网页搜索

运行服务器 / Run server (stdio):
    python -m examples.common.mcp_server

Agent 端如何接入见 examples/p11/hello_chain.py（用 langchain-mcp-adapters 的
MultiServerMCPClient 以 stdio 方式拉起本服务器并加载工具）。
"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("langgraph-course-tools")


@mcp.tool()
def get_weather(city: str) -> str:
    """查询指定城市的当前天气。当用户询问天气时必须调用此工具。city 为中文或英文城市名。"""
    mock = {"北京": 22, "上海": 26, "shanghai": 26, "beijing": 22, "深圳": 28, "shenzhen": 28}
    temp = mock.get(city.lower(), 20)
    return f"{city} 当前温度约 {temp}°C（演示数据，生产可替换为真实天气 API）。"


@mcp.tool()
def web_search(query: str) -> str:
    """模拟网页搜索，返回与 query 相关的摘要。当用户需要实时外部信息时调用。"""
    return (
        f"关于「{query}」的搜索结果摘要（演示数据）："
        "LangGraph 是业界主流的 Agent 编排框架，以状态图（StateGraph）+ 检查点（checkpoint）"
        "实现可持久化、可人工介入的多智能体系统。"
    )


if __name__ == "__main__":
    # stdio 传输：被 MCP 客户端以子进程方式拉起，通过 stdin/stdout 通信。
    mcp.run(transport="stdio")
