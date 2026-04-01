FROM python:3.12-slim

WORKDIR /app

# 設定時區為台灣時間
ENV TZ=Asia/Taipei
RUN ln -sf /usr/share/zoneinfo/Asia/Taipei /etc/localtime

# 安裝 Playwright 系統依賴（手動安裝避免字型套件不存在的問題）
RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libdrm2 libdbus-1-3 libxkbcommon0 libatspi2.0-0 \
    libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libgbm1 libpango-1.0-0 libcairo2 libasound2 \
    fonts-unifont fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 安裝 Playwright Chromium（不用 --with-deps，系統依賴已手動安裝）
RUN playwright install chromium

COPY app/ ./app/

ENV FLASK_APP=app
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
