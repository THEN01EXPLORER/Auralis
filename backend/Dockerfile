# Backend Dockerfile for production deployment
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install system dependencies needed to build some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . /app

# Expose port 10000 for Render (uses $PORT env variable in production)
EXPOSE 10000

# Start Uvicorn with PORT environment variable (Render injects this)
# Falls back to 10000 if PORT is not set
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000}
