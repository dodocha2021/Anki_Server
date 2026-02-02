FROM debian:bullseye-slim

# 设置非交互模式
ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:99

# 安装依赖
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    xvfb \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    libxkbcommon-x11-0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libnss3 \
    libnspr4 \
    libasound2 \
    libdbus-1-3 \
    libglib2.0-0 \
    python3 \
    python3-pip \
    git \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 下载并安装 Anki
WORKDIR /tmp
RUN wget -O anki.tar.zst https://github.com/ankitects/anki/releases/download/24.11/anki-24.11-linux-qt6.tar.zst \
    && apt-get update && apt-get install -y zstd \
    && tar xaf anki.tar.zst \
    && cd anki-24.11-linux-qt6 \
    && ./install.sh \
    && cd .. \
    && rm -rf anki* \
    && rm -rf /var/lib/apt/lists/*

# 创建工作目录
WORKDIR /app

# 创建 Anki 数据目录
RUN mkdir -p /root/.local/share/Anki2

# 复制 AnkiConnect 插件安装脚本
COPY install_ankiconnect.sh /app/
RUN chmod +x /app/install_ankiconnect.sh

# 复制自动同步脚本
COPY auto_sync.py /app/
RUN pip3 install requests

# 复制启动脚本
COPY start.sh /app/
RUN chmod +x /app/start.sh

# 暴露 AnkiConnect 端口
EXPOSE 8765

# 启动脚本
CMD ["/app/start.sh"]
