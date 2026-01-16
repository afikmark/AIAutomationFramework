FROM ai-automation-framework-base:latest

# Install system dependencies required for Playwright browsers
USER root
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN uv sync --frozen --no-dev

# Install Playwright browsers with proper permissions
# Set HOME to /tmp so Playwright cache is accessible to all users
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
RUN mkdir -p /ms-playwright && \
    chmod -R 777 /ms-playwright && \
    uv run playwright install chromium --with-deps && \
    chmod -R 777 /ms-playwright

# Copy application code
COPY . .

# Set proper permissions
RUN chmod -R 777 /app

CMD ["uv", "run", "pytest"]
