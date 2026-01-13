FROM ai-automation-framework-base:latest

# Set Playwright browsers path to a fixed location (not dependent on HOME)
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/playwright-browsers

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock* ./

# Install Python dependencies
RUN uv sync --frozen --no-dev || uv sync --no-dev

# Install Playwright browsers and system dependencies
RUN uv run playwright install --with-deps chromium

# Copy the rest of the application
COPY . .

# Make .venv and app directory writable for any user (needed for Jenkins user mapping)
RUN chmod -R 777 /app/.venv /app

# Set default command to run tests
CMD ["uv", "run", "pytest", "--alluredir=allure-results"]
