# Dockerfile

FROM python:3.13-slim

# 1️⃣ Install system dependencies (Postgres headers + Playwright libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libxcomposite1 libxdamage1 libxrandr2 libxss1 libxtst6 \
    libgbm1 libgtk-3-0 libasound2 libpangocairo-1.0-0 libpango1.0-0 \
    libgdk-pixbuf2.0-0 wget ca-certificates \
 && rm -rf /var/lib/apt/lists/*


WORKDIR /app

# 2️⃣ Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3️⃣ Install Playwright & its browsers
#    --with-deps installs additional OS libs if needed
RUN pip install playwright && playwright install --with-deps

# 4️⃣ Copy your application code
COPY . .

EXPOSE 8000

# 5️⃣ Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
