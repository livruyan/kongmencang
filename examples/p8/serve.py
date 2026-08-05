"""
Phase 8 · 示例 1：把图包装成 HTTP 服务（FastAPI）
================================================
目的：把 Phase 6 的「研究员→写手→审校」图，用 FastAPI 暴露成对外 API。
这样它就能被前端、其他服务、或定时任务调用——从「脚本」变成「服务」。

要点：
  - 用 MemorySaver（生产换 PostgresSaver）给图挂上持久化，thread_id 隔离会话；
  - /run 接收 {topic, thread_id}，返回最终 State；同一 thread_id 可续跑；
  - 真实部署配 Docker + 进程管理器（uvicorn 多 worker / gunicorn）。
"""

from fastapi import FastAPI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END

# 复用 Phase 6 的节点，避免重复实现
from examples.p6.crew_graph import CrewState, researcher, writer, reviewer

app = FastAPI(title="LangGraph Crew Service")


def _build_served_graph():
    builder = StateGraph(CrewState)
    builder.add_node("researcher", researcher)
    builder.add_node("writer", writer)
    builder.add_node("reviewer", reviewer)
    builder.add_edge(START, "researcher")
    builder.add_edge("researcher", "writer")
    builder.add_edge("writer", "reviewer")
    builder.add_edge("reviewer", END)
    # checkpointer 让不同 thread_id 的会话各自持久化
    return builder.compile(checkpointer=MemorySaver())


# 实际项目里可用全局单例 / 依赖注入；这里每次构建便于演示
GRAPH = _build_served_graph()


@app.post("/run")
def run_crew(payload: dict):
    topic = payload.get("topic", "")
    thread_id = payload.get("thread_id", "default")
    config = {"configurable": {"thread_id": thread_id}}
    result = GRAPH.invoke({"topic": topic}, config)
    return {
        "research": result.get("research", ""),
        "draft": result.get("draft", ""),
        "review": result.get("review", ""),
        "thread_id": thread_id,
    }


if __name__ == "__main__":
    import uvicorn

    # 生产：uvicorn serve:app --workers 4 ；或 gunicorn -k uvicorn.workers.UvicornWorker
    uvicorn.run(app, host="0.0.0.0", port=8000)
