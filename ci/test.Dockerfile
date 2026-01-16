FROM ai-automation-framework-base:latest

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY . .

RUN chmod -R 777 /app

CMD ["uv", "run", "pytest"]
