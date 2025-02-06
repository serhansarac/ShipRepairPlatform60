# 1️Ubuntu tabanlı bir image kullan
FROM ubuntu:latest

# 2️Gerekli sistem kütüphanelerini yükle
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    gunicorn \
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

# 3️Çalışma dizini oluştur ve dosyaları kopyala
WORKDIR /app
COPY . /app/

# 4️Virtual environment oluştur ve bağımlılıkları yükle
RUN python3 -m venv venv
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# 5️Django migration işlemlerini çalıştır
RUN . venv/bin/activate && python manage.py migrate

# 6️Statik dosyaları toplamak için
RUN . venv/bin/activate && python manage.py collectstatic --noinput

# 7️Port ve çalıştırma komutu
EXPOSE 8000
CMD ["bash", "start.sh"]
