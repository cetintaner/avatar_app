FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

# Python 3.10 yerine daha güncel bir sürüm seçebilirsiniz
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Gerekli sistem bağımlılıklarını yükleyin
RUN apt update && apt install -y \
    git \
    ffmpeg \
    wget \
    curl \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    python3 \
    python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python

# requirements.txt'i kopyala ve bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# SadTalker deposunu klonla
RUN git clone https://github.com/OpenTalker/SadTalker.git

# Uygulama dosyalarını kopyala
COPY app /app

# Streamlit uygulamasını başlat
EXPOSE 8501
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.enableCORS=false"]
