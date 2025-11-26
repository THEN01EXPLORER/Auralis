# Backend Dockerfile optimized for free tier (minimal memory)
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

# Use minimal requirements (no heavy dependencies like slither, boto3)
COPY requirements-minimal.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . /app

# Expose port 10000 for Render (uses $PORT env variable in production)
EXPOSE 10000

# Use single worker uvicorn (lowest memory footprint)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000", "--workers", "1"]
