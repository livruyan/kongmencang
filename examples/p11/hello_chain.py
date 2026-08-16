"""
Phase 11 · MCP 工具接口：让智能体调用标准协议工具
=========================================================================
目的：把 Agent 的能力来源从「写死在代码里的 @tool」升级为「标准 MCP 协议可调用的
外部工具」，对应改进报告 P0「MCP 工具接口」。你已有的网络工程底子正好做 MCP 工具服务器。

要点：
  1. 工具服务器 examples/common/mcp_server.py 用官方 mcp SDK 暴露标准 MCP 工具；
  2. Agent 端用 langchain-mcp-adapters 的 MultiServerMCPClient 以 stdio 拉起服务器、加载工具；
  3. 工具逻辑与 Agent 解耦——换工具 / 换服务器不用改 Agent 代码，只需改连接配置；
  4. 之后可把 mcp_server.py 换成任意第三方 MCP 服务器（天气、数据库、企业内部 API）。

运行 / Run（需先 pip install mcp langchain-mcp-adapters）:
    python -m examples.p11.hello_chain
    # 或 make run p=11
"""
import asyncio
import sys

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

from examples.common.llm import get_chat_model


async def main_async() -> None:
    # 以 stdio 方式拉起本仓库内置的 MCP 工具服务器（examples/common/mcp_server.py）
    client = MultiServerMCPClient(
        {
            "course-tools": {
                "command": sys.executable,
                "args": ["-m", "examples.common.mcp_server"],
                "transport": "stdio",
            }
        }
    )
    tools = await client.get_tools()
    print(f"已从 MCP 服务器加载 {len(tools)} 个工具：{[t.name for t in tools]}")

    agent = create_react_agent(get_chat_model(), tools)  # 底层即一张状态图：Node=模型调用，边=工具循环
    result = agent.invoke({"messages": [("user", "北京现在多少度？另外帮我搜一下 LangGraph 是什么。")]})

    print("\n===== 最终答案 =====")
    print(result["messages"][-1].content)


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
