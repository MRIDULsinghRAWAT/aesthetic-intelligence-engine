# ==============================================================================
# Dockerfile for Edge Containerization
# On-Device Aesthetic Intelligence Engine
# ==============================================================================

# Use official Python lightweight image
FROM python:3.10-slim

# Set environment variables to prevent pyc files and buffer logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# Set active working directory
WORKDIR /app

# Install system packages required for OpenCV and SQLite
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install backend dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir \
    flask \
    numpy \
    opencv-python-headless \
    mlflow \
    tensorflow-cpu

# Copy the project files to the container
COPY . /app

# Expose port 5000 for Flask Server
EXPOSE 5000

# Start Flask Application
CMD ["python", "app.py"]
