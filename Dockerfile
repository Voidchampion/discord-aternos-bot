# Base image
FROM python:3.11-slim

# Set Playwright env var
ENV PLAYWRIGHT_BROWSERS_PATH=0

# Set working directory
WORKDIR /app

# Install Linux dependencies for Playwright Chromium
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libgtk-3-0 \
    libasound2 \
    fonts-liberation \
    ca-certificates \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright Chromium (with dependencies)
RUN python -m playwright install chromium

# Copy all files
COPY . .

# Start command
CMD ["python", "bot.py"]
