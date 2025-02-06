# 1. Resmi Python tabanlı bir Linux görüntüsü kullan (Debian tabanlı)
FROM python:3.12-slim

# 2. Çalışma dizinini belirle
WORKDIR /app

# 3. Sistemde gerekli bağımlılıkları yükle (Aptfile'ı kullanarak)
COPY Aptfile /Aptfile
RUN apt-get update && xargs apt-get install -y < /Aptfile

# 4. Gerekli Python bağımlılıklarını yükle
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Uygulama dosyalarını kopyala
COPY . /app/

# 6. Çalıştırma komutunu belirle
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ShipRepairPlatform60.wsgi:application"]
