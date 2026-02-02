FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装必要的依赖
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安装 Anki（包含同步服务器）
RUN pip install --no-cache-dir anki

# 创建数据目录
RUN mkdir -p /data/collections

# 创建启动脚本
COPY sync-server-start.sh /app/
RUN chmod +x /app/sync-server-start.sh

# 暴露同步服务器端口
EXPOSE 8080

# 设置环境变量
ENV SYNC_BASE=/data
ENV SYNC_PORT=8080
ENV SYNC_HOST=0.0.0.0

# 启动同步服务器
CMD ["/app/sync-server-start.sh"]

