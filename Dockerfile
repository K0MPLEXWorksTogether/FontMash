FROM python:3.11-slim

WORKDIR /app

# Install deps first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# WebSocket port
EXPOSE 8765

# No ENV values here — pulled from runtime
CMD ["python", "app.py"]
