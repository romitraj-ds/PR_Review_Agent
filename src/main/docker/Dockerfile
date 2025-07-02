# Use the official Python 3.11 slim image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/src/
COPY .env /app/.env

# Expose port 8080 to allow external access to the application
EXPOSE 8000

# Set the default command to run the client application
CMD ["uvicorn", "src.main.python.Client.client:app", "--host", "0.0.0.0", "--port", "8000"]
