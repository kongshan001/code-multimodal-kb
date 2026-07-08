# 在官方 mem0 镜像上补旧版缺失依赖（psycopg / langchain-neo4j），按 mem0.ai self-host 指南。
FROM mem0ai/mem0:latest
RUN pip install --no-cache-dir "psycopg[binary]" langchain-neo4j
