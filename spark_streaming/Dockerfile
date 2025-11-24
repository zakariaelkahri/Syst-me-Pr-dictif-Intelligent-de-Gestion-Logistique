# Use Python 3.11 slim as base
FROM python:3.11-slim

# Set metadata
LABEL maintainer="your-email@example.com"
LABEL description="Spark Streaming application container"

# Install Java (Required for Spark) and system utilities
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    default-jre \
    procps \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set Environment Variables
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a non-root user
RUN useradd -m sparkuser && chown -R sparkuser:sparkuser /app
USER sparkuser

# Command to run the application
# Using python directly is fine for local/standalone mode. 
# For cluster mode, you might use spark-submit.
CMD ["python", "-u", "main.py"]