# ---- LangGraph Crew Service 镜像 ----
# 对应 Phase 8 的 FastAPI 服务（examples/p8/serve.py 暴露的 app）
FROM python:3.11-slim

WORKDIR /app

# 先装依赖，利用 Docker 层缓存
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再拷贝源码（.dockerignore 已排除 docs/node_modules/.env 等非运行时文件）
COPY . .

EXPOSE 8000

# 直接用 uvicorn 拉起服务；生产可加 --workers N
CMD ["uvicorn", "examples.p8.serve:app", "--host", "0.0.0.0", "--port", "8000"]
