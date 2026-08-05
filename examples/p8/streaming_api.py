"""Phase 8 · 流式 API / Streaming API endpoint.

在 Phase 8 的 FastAPI 服务上增加 SSE 流式返回，让前端可以逐字渲染模型输出。
Adds SSE streaming on top of the Phase 8 FastAPI service so the UI can render
model output token-by-token.
"""
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from examples.common.llm import get_chat_model

app = FastAPI()


@app.post("/stream")
async def stream(payload: dict):
    llm = get_chat_model()

    def event_gen():
        for chunk in llm.stream(payload.get("question", "")):
            if chunk.content:
                yield f"data: {chunk.content}\n\n"

    return StreamingResponse(event_gen(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
