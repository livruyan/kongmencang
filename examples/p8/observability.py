"""
Phase 8 · 示例 2：给图接上「可观测性」（Langfuse 为主 / LangSmith 可选）
========================================================================
目的：生产环境里你一定要能「看见」图每一步在干什么——哪个节点慢、
哪次调用贵、哪条链路出错。LangChain/LangGraph 通过 callbacks 把每次
执行上报到可观测平台。

项目决策（2026-08-04）：**以 Langfuse 为主**——开源、可自托管、对国内
读者友好、免费，原生支持 LangChain/LangGraph 的 tracing + eval。
LangSmith 作为「已有官方账号」的可选路径保留。

两者都通过把 CallbackHandler 透传给 graph.invoke 的 callbacks 参数来接线。
（运行需先在 .env / 环境变量配置对应 key，本文件只展示接线方式。）
"""

import os

from examples.p6.crew_graph import build_graph


# ---------------------------------------------------------------------------
# 主路线：Langfuse（开源 / 可自托管，推荐）
# 配置 LANGFUSE_PUBLIC_KEY / LANGFUSE_SECRET_KEY / LANGFUSE_HOST
# ---------------------------------------------------------------------------
def run_with_langfuse(topic: str):
    from langfuse.callback import CallbackHandler

    handler = CallbackHandler(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
    )
    graph = build_graph()
    return graph.invoke({"topic": topic}, config={"callbacks": [handler]})


# ---------------------------------------------------------------------------
# 可选路线：LangSmith（官方 SaaS）
# 配置 LANGCHAIN_TRACING_V2=true / LANGCHAIN_API_KEY / LANGCHAIN_PROJECT 后，
# LangChain 会自动上报；也可显式传入 CallbackHandler。
# ---------------------------------------------------------------------------
def run_with_langsmith(topic: str):
    from langchain_core.tracers import LangChainTracer

    tracer = LangChainTracer(
        project_name=os.getenv("LANGCHAIN_PROJECT", "langgraph-course")
    )
    graph = build_graph()
    return graph.invoke({"topic": topic}, config={"callbacks": [tracer]})


if __name__ == "__main__":
    # 默认走 Langfuse（需先配置 LANGFUSE_* 环境变量）
    # run_with_langfuse("用一句话介绍状态图")
    # 若用 LangSmith，取消下一行注释
    # run_with_langsmith("用一句话介绍状态图")
    print("本示例展示可观测性接线方式；配置 key 后取消注释即可上报。")
