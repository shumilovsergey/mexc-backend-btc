FROM python:3.11-slim

# Install CA certs and curl for in-container debugging
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
         ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use Flask CLI with env vars from docker-compose
CMD ["flask", "run"]
