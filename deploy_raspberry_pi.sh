#!/bin/bash
# ==============================================================================
# Edge AI Setup Script for Raspberry Pi & Debian/Ubuntu Systems
# On-Device Aesthetic Intelligence Engine
# ==============================================================================

set -e # Exit immediately if a command exits with a non-zero status

echo "====================================================================="
echo "  Setting up On-Device Aesthetic Intelligence Engine on Edge Host   "
echo "====================================================================="

# 1. Update OS Package Index
echo "[1/5] Updating system packages..."
sudo apt-get update -y

# 2. Install essential OS dependencies (Python, Virtualenv, and OpenCV bindings)
echo "[2/5] Installing OS dependencies (Python, venv, OpenCV GUI-less bindings)..."
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    sqlite3

# 3. Create Python Virtual Environment
echo "[3/5] Setting up Python virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "Virtual environment '.venv' created."
else
    echo "Virtual environment '.venv' already exists."
fi

# Activate virtual environment
source .venv/bin/activate

# 4. Install Python Dependencies
echo "[4/5] Installing python packages inside virtual environment..."
pip install --upgrade pip

# Note: We install opencv-python-headless to skip heavy X11 GUI dependencies
# and tflite-runtime to avoid standard tensorflow's massive ~500MB download
pip install \
    Flask \
    opencv-python-headless \
    mlflow \
    tflite-runtime

# 5. Ensure folder structures are correct
echo "[5/5] Checking workspace directories..."
mkdir -p models templates docs reports

# Verify initial model file exists
if [ ! -f "models/model_dynamic_quant.tflite" ]; then
    echo "⚠️ WARNING: models/model_dynamic_quant.tflite is missing!"
    echo "Please ensure the model file is copied before running the server."
fi

echo "====================================================================="
echo "🎉 Setup complete! To run the application:"
echo "  1. Activate virtual environment: source .venv/bin/activate"
echo "  2. Start Flask Server:           python app.py"
echo "  3. Start MLflow UI Dashboard:   mlflow ui --backend-store-uri sqlite:///mlflow.db"
echo "====================================================================="
