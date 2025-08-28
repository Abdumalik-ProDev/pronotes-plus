# Use official Python slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies (required for psycopg2-binary or other C extensions)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire app
COPY . .

# Optional: Install dumb-init to handle signals properly in containers
RUN pip install dumb-init

# Expose port
EXPOSE 8000

# Run with dumb-init to properly handle shutdown signals
ENTRYPOINT ["dumb-init", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]