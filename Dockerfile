# Start from Python base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install all Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Default command (can be overridden)
CMD ["python", "src/producer.py"]