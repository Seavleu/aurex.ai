# AUREX.AI - Pipeline Worker Dockerfile
# Prefect Worker for Data Ingestion & AI Inference

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY apps/pipeline /app/pipeline
COPY packages /app/packages

# Create models directory
RUN mkdir -p /app/models

# Set Python path
ENV PYTHONPATH=/app

# Download FinBERT model (optional - can be done at runtime)
# RUN python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; \
#     AutoTokenizer.from_pretrained('ProsusAI/finbert'); \
#     AutoModelForSequenceClassification.from_pretrained('ProsusAI/finbert')"

# Run pipeline worker
CMD ["python", "-m", "pipeline.main"]

