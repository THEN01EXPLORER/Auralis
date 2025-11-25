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

# Start with gunicorn for production with memory-optimized settings
# Use only 2 workers to stay under Render's 512MB free tier limit
CMD ["gunicorn", "main:app", "-c", "gunicorn.conf.py"]
