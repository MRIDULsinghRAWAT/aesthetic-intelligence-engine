# Aesthetic Intelligence Engine (Æ)

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Vercel%20Production-success?logo=vercel&logoColor=white)](https://aesthetic-intelligence-engine.vercel.app)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org)
[![ML Framework](https://img.shields.io/badge/ML%20Framework-TensorFlow%20%2F%20TFLite%20%2F%20LiteRT-orange?logo=tensorflow&logoColor=white)](https://tensorflow.org)
[![Backend](https://img.shields.io/badge/Backend-Flask-lightgrey?logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![OpenCV](https://img.shields.io/badge/CV-OpenCV-green?logo=opencv&logoColor=white)](https://opencv.org)
[![Docker](https://img.shields.io/badge/Container-Docker-blue?logo=docker&logoColor=white)](https://docker.com)

An on-device **Edge AI pipeline** that evaluates, scores, and enhances image aesthetics in real time. Powered by an optimized, dynamically quantized **TensorFlow Lite (LiteRT)** model running locally to guarantee **sub-5ms scoring**, zero network overhead, and absolute privacy. Equipped with a **live model hot-swapping controller** and server-side **computer vision auto-enhancement**.

🚀 **Live Production Application**: [https://aesthetic-intelligence-engine.vercel.app](https://aesthetic-intelligence-engine.vercel.app)

---

## 1. Project Overview

The **Aesthetic Intelligence Engine** is designed to analyze image aesthetic quality directly on edge devices (like Raspberry Pi), mobile hardware (Android), and cloud serverless platforms (Vercel).

By leveraging **transfer learning** on MobileNetV2 and applying **Dynamic Range Quantization**, the neural network is compressed from over 10 MB to **2.54 MB** (a 75% reduction), achieving **sub-5ms CPU inference**.

### Key System Highlights:
- **Responsive Single-Page Dashboard**: Swiss-style glassmorphic design optimized for both desktop and mobile screens.
- **Webcam & Camera Integration**: Real-time live camera capture via WebRTC / native device camera picker.
- **Computer Vision Auto-Enhancement**: Server-side image enhancement (YCrCb-space CLAHE contrast tuning & 2D sharpening kernel filter) via OpenCV.
- **Live MLOps Hot-Swapping**: Thread-safe dynamic model registry and re-allocator to swap active interpreters (`v1.0.0` ⇄ `v2.0.0`) on the fly without server restart.
- **Multi-Environment Support**: Auto-detects local host, Raspberry Pi OS, Docker containers, and Vercel serverless read-only environments.

---

## 2. Interface & Live Screenshots

| Live Model Hot-Swapping | Responsive Mobile & Camera Capture |
| :---: | :---: |
| ![MLOps Dynamic Updates](reports/phase3_mlops_demo.webp) | ![Webcam Capture Mode](docs/web_app_screenshot_2.png) |

---

## 3. Architecture & Core Features

```
[User / Browser Client] 
       │
       ▼ (Upload Photo / Web Camera Snap / Live Model Hot-Swap)
[Flask Web Server (app.py)] ───► [OpenCV Preprocessing (YCrCb CLAHE / 2D Sharpening)]
       │                                            │
       ├─► (Returns active version/meta)            ▼ (Invoke Thread-Locked Interpreter)
       │                                        [TFLite Interpreter Class]
       │                                            ▲
       ▼ (Returns score, latency & base64 image)    │ (Reloads versioned binary)
[User / Browser Client] ◄─────────────────────── [model_dynamic_quant_vX.tflite]
```

![System Architecture Schema](docs/architecture_diagram.png)

- **On-Device Inference**: Locally loaded TFLite models analyze inputs without any cloud API dependencies.
- **Webcam Integration**: Stream and process live images directly from mobile/desktop browser cameras.
- **Image Enhancement**: Auto-enhance low-contrast or noisy images using YCrCb-space CLAHE and 2D sharpening filters to boost aesthetic scores.
- **Live Hot-Swapping**: Dynamically re-allocate active production models (`v1.0.0` ⇄ `v2.0.0`) from the UI without restarting `app.py`.
- **Edge & Cloud Engine Fallback**: Backend dynamically imports `tensorflow`, `tflite_runtime`, or `ai_edge_litert` (lightweight wheels under 15MB for Raspberry Pi & Vercel serverless).

---

## 4. API Reference

### 1. Predict Aesthetic Score
* **Endpoint**: `POST /predict`
* **Body**: `multipart/form-data` (`image`: File)
* **Response**:
  ```json
  {
    "score": 0.842,
    "label": "Good Aesthetic",
    "latency_ms": 4.12,
    "model_version": "v1.0.0"
  }
  ```

### 2. Auto-Enhance Image
* **Endpoint**: `POST /enhance`
* **Body**: `multipart/form-data` (`image`: File)
* **Response**: Returns enhanced base64 PNG data, newly calculated score, and latency.

### 3. Model Status
* **Endpoint**: `GET /model/status`
* **Response**: Returns active version, active model path, and registered available versions.

### 4. Dynamic Model Update (Hot-Swap)
* **Endpoint**: `POST /model/update`
* **Body**: `{"version": "v2.0.0"}`
* **Response**: Re-allocates TFLite interpreter atomically under thread safety locks.

---

## 5. Model Quantization Benchmarks

| Metric | Baseline Float32 Model | Dynamic Range Quantized Model |
| :--- | :--- | :--- |
| **File Size** | ~10.2 MB | **2.54 MB** (75% savings) |
| **Precision** | 32-bit Floating Point | 8-bit Integer (quantized weights) |
| **CPU Latency** | ~15ms - 20ms | **Sub-5ms** (4x speedup) |
| **Accuracy Loss** | Reference Base | Negligible ($\le 1\%$ deviation) |

---

## 6. Getting Started & Local Development

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/MRIDULsinghRAWAT/aesthetic-intelligence-engine.git
cd aesthetic-intelligence-engine
pip install flask numpy opencv-python tensorflow
```

### 2. Start Application
```bash
python app.py
```
Open your browser at `http://localhost:5000`.

---

## 7. Deployment Guide

### Option A: Vercel Cloud Production (Instant HTTPS)
Live URL: [https://aesthetic-intelligence-engine.vercel.app](https://aesthetic-intelligence-engine.vercel.app)
```bash
npx vercel --prod
```
*Note: Configured with `ai-edge-litert` (LiteRT) to keep total serverless bundle size under 300MB.*

### Option B: Local Network Mobile Testing (Wi-Fi)
1. Run `python app.py` on your laptop.
2. Connect your mobile phone to the same Wi-Fi.
3. Open `http://<YOUR_LAPTOP_IP>:5000` in your phone browser.

### Option C: Raspberry Pi OS Native Deployment
```bash
chmod +x deploy_raspberry_pi.sh
./deploy_raspberry_pi.sh
source .venv/bin/activate
python app.py
```

### Option D: Docker Container Setup
```bash
docker build -t aesthetic-intelligence-engine .
docker run -p 5000:5000 aesthetic-intelligence-engine
```

---

## 8. Presentation & Technical Documentation

For a step-by-step mentor presentation script and line-by-line code mapping, refer to:
* **[PROJECT_DEMO_AND_CODE_GUIDE.md](PROJECT_DEMO_AND_CODE_GUIDE.md)**: Mentor presentation script, Q&A code locations, and technical term definitions.
