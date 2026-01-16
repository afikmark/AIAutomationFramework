FROM --platform=$BUILDPLATFORM python:3.12-slim-bullseye

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    zip \
    unzip \
    curl \
    ca-certificates \
    gnupg \
    git \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver

WORKDIR /app
