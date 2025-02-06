# Ubuntu tabanlı bir image kullan
FROM ubuntu:latest

# Gerekli sistem kütüphanelerini yükle
RUN apt-get update && apt-get install -y \
    libgobject-2.0-0 \
    libcairo2 \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libffi-dev \
    fonts-liberation \
    fonts-dejavu \
    libgdk-pixbuf2.0-0 \
    libxml2 \
    && rm -rf /var/lib/apt/lists/*

# Python ve gerekli araçları yükle
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv gunicorn

# Çalışma dizini oluştur ve dosyaları kopyala
WORKDIR /app
COPY . /app/

# Virtual environment oluştur ve bağımlılıkları yükle
RUN python3 -m venv venv
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Port ve çalıştırma komutu
EXPOSE 8000
CMD ["bash", "start.sh"]
