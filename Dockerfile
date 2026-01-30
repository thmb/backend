# syntax=docker/dockerfile:1

FROM python:3.14-slim

WORKDIR /app

# Install uv for faster package installation
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv pip install --system --no-cache -r pyproject.toml

# Copy application code
COPY restapi/ ./restapi/

# Expose port
EXPOSE 8000

# Run with uvicorn
CMD ["uvicorn", "restapi.main:app", "--host", "0.0.0.0", "--port", "8000"]
