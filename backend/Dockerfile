FROM python:3.12-slim

# Hämtar bara uv-binären från dess officiella image
# Installera hela uv separat via pip.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Kopierar in hela workspacet: root-metadata, båda paketen och datamappen.
# uv workspaces behöver hela strukturen för att kunna resolva paketen korrekt.
COPY pyproject.toml uv.lock ./
COPY backend/ backend/
COPY frontend/ frontend/
COPY data/ data/

# Installerar beroenden exakt enligt uv.lock
RUN uv sync --frozen --all-packages

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]