FROM ai-automation-framework-base:latest

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock* ./

# Install Python dependencies
RUN uv sync --frozen --no-dev || uv sync --no-dev

# Install Playwright browsers and system dependencies
RUN uv run playwright install --with-deps chromium

# Copy the rest of the application
COPY . .

# Set default command to run tests
CMD ["uv", "run", "pytest", "--alluredir=allure-results"]
