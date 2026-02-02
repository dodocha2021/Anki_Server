FROM debian:bullseye-slim

# 设置非交互模式和显示
ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:99

# 配置 UTF-8 locale
RUN apt-get update && apt-get install -y locales \
    && sed -i 's/^# *\(en_US.UTF-8\)/\1/' /etc/locale.gen \
    && locale-gen en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# 安装依赖
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    xvfb \
    xdg-utils \
    zstd \
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
    libegl1-mesa \
    libgl1-mesa-glx \
    libglu1-mesa \
    libglx0 \
    python3 \
    python3-pip \
    git \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 下载并安装 Anki 2.1.54（稳定版本）
WORKDIR /tmp
RUN wget -O anki.tar.zst https://github.com/ankitects/anki/releases/download/2.1.54/anki-2.1.54-linux-qt6.tar.zst \
    && tar xaf anki.tar.zst \
    && cd anki-2.1.54-linux-qt6 \
    && ./install.sh \
    && cd .. \
    && rm -rf anki*

# 创建工作目录
WORKDIR /app

# 创建 Anki 数据目录
RUN mkdir -p /root/.local/share/Anki2

# 复制脚本
COPY install_ankiconnect.sh /app/
COPY auto_sync.py /app/
COPY init_anki.py /app/
COPY start.sh /app/

RUN chmod +x /app/*.sh
RUN pip3 install requests

# 暴露 AnkiConnect 端口
EXPOSE 8765

# 启动脚本
CMD ["/app/start.sh"]


