FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY . ./
RUN uv sync --frozen --no-cache --no-dev
EXPOSE 8000

CMD ["uv", "run", "streamlit", "run", "main.py"]