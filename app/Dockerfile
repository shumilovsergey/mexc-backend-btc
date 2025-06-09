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

# Launch the app directly (will bind 0.0.0.0 per app.py)
CMD ["python", "app.py"]
