FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY backend/ backend/
COPY frontend/ frontend/
COPY data/ data/

RUN uv sync --frozen --all-packages

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "frontend/src/frontend/app.py", "--server.address=0.0.0.0", "--server.port=8501"]