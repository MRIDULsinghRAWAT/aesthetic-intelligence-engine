# Aesthetic Intelligence Engine (Æ) - Live Demo & Code Mapping Guide

This document provides a streamlined presentation guide to showcase the **Aesthetic Intelligence Engine** to your mentor, followed by a complete mapping of all major features to their exact file and line-level implementation details in the codebase.

---

## Part 1: How to Give a Focused Demo to Your Mentor

### 1. The 30-Second Elevator Pitch
> *"The Aesthetic Intelligence Engine is an on-device Edge AI solution that evaluates and enhances image aesthetic quality in real time. We compressed a MobileNetV2 model by 75% down to **2.54 MB** using **Dynamic Range Quantization**, achieving **sub-5ms CPU scoring** with zero cloud latency and total data privacy. It also includes an automated OpenCV enhancement pipeline and a live model hot-swapping controller."*

---

### 2. Pre-Demo Startup Command

Run this single command in your terminal (`c:\Users\Mridul\Desktop\aesthetic-intelligence-engine`):

```bash
python app.py
```
* **Local Web App**: Opens automatically at `http://localhost:5000`
* **Mobile / Local Network Access**: Binds to `0.0.0.0:5000` so anyone on the same Wi-Fi can open `http://<YOUR_LOCAL_IP>:5000` directly on their phone camera.

---

### 3. Step-by-Step Live Demo Flow

#### Step 1: Real-Time Image Aesthetic Evaluation
1. Go to `http://localhost:5000`.
2. Drag and drop any image (e.g. `test_image.jpg` or `mridul.jpg`) or select one.
3. Click **"Analyze Aesthetic"**.
4. **Point out to your mentor**:
   - **Score**: Numerical aesthetic score from `0.00` to `1.00`.
   - **Classification Badge**: *"Good Aesthetic"* vs *"Bad Aesthetic"*.
   - **Sub-5ms Latency**: Real-time evaluation running completely on CPU locally.

#### Step 2: Live Webcam Mode (Edge AI Capture)
1. Click **"Use Web Camera"** to open your live browser camera stream.
2. Click **"Capture Photo"**.
3. Click **"Analyze Aesthetic"** to score live camera frames immediately.
4. **Point out to your mentor**: Complete on-device processing—no image frame ever leaves the local machine.

#### Step 3: Server-Side Computer Vision Auto-Enhancement
1. Click **"Auto-Enhance Image"**.
2. **Point out to your mentor**:
   - OpenCV applies YCrCb CLAHE (Adaptive Histogram Equalization) + a 2D sharpening kernel filter.
   - The enhanced image is rendered side-by-side and re-scored immediately by the TFLite model, showing a quantifiable score jump!

#### Step 4: Live Model Hot-Swapping & Dynamic Rollbacks
1. Scroll down to the **MLOps Model Controller** card on the dashboard.
2. Click **"Deploy v2.0.0 (Upgrade)"**.
   - Notice how the active model version updates to `v2.0.0` live without restarting the Flask server!
3. Click **"Rollback to v1.0.0"**.
   - Watch the dynamic interpreter re-allocate back to `v1.0.0` in real time.
4. **Point out to your mentor**: Complete thread-safe dynamic interpreter swapping while the Flask app remains 100% active.

---

## Part 2: Important Features & Code Implementation Mapping

Below is the architectural mapping showing where every key feature is implemented in the codebase.

| # | Feature Name | Description | Key Code Files & Line Numbers |
|---|---|---|---|
| **1** | **Dynamic Range Quantized TFLite Model** | Compressed MobileNetV2 regression model from 10MB+ down to **2.54MB** (75% savings) with sub-5ms CPU latency. | • Model Binary: [`models/model_dynamic_quant.tflite`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/models/model_dynamic_quant.tflite)<br>• Training Notebook: [`notebooks/phase1_training.ipynb`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/notebooks/phase1_training.ipynb) |
| **2** | **Dual-Engine Edge Fallback** | Fallback system importing full `tensorflow` or lightweight `tflite_runtime` (15MB wheel for Raspberry Pi / micro-controllers). | • Implementation: [`app.py:L13-L25`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/app.py#L13-L25)<br>• Edge Script: [`deploy_raspberry_pi.sh:L40-L55`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/deploy_raspberry_pi.sh) |
| **3** | **Thread-Safe Model Interpreter Manager** | Global `threading.Lock()` and interpreter state loader preventing concurrency issues when executing TFLite tensor allocations. | • Initializer & Locks: [`app.py:L54-L111`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/app.py#L54-L111) |
| **4** | **Live Hot-Swapping & Model Rollback** | Dynamic `POST /model/update` endpoint that downloads or copies new TFLite versions and re-initializes `InterpreterClass` on the fly. | • Backend Endpoint: [`app.py:L136-L211`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/app.py#L136-L211)<br>• Status Endpoint: [`app.py:L126-L134`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/app.py#L126-L134)<br>• UI Controller Card: [`templates/index.html:L815-L836`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/templates/index.html#L815-L836)<br>• JS Update Handler: [`templates/index.html:L1087-L1138`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/templates/index.html#L1087-L1138) |
| **5** | **Computer Vision Image Auto-Enhancement** | OpenCV YCrCb-space CLAHE contrast tuning + 2D sharpening kernel filter (`POST /enhance`), returning Base64 image and improved score. | • Backend Logic: [`app.py:L250-L303`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/app.py#L250-L303)<br>• JS Enhance Handler: [`templates/index.html:L1014-L1054`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/templates/index.html#L1014-L1054) |
| **6** | **Real-Time Aesthetic Scoring Pipeline** | OpenCV image decoder, `(128,128,3)` standardizer, TFLite tensor invoker, and JSON latency responder (`POST /predict`). | • Backend Logic: [`app.py:L213-L249`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/app.py#L213-L249)<br>• JS Predict Handler: [`templates/index.html:L975-L1012`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/templates/index.html#L975-L1012) |
| **7** | **Vercel Serverless Read-Only Filesystem Adaptor** | Dynamic detection of `VERCEL=1` redirecting database writes, logs, and TFLite model downloads to the writable `/tmp` directory. | • Environment Handler: [`app.py:L29-L51`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/app.py#L29-L51)<br>• Vercel Entrypoint: [`api/index.py:L1-L2`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/api/index.py#L1-L2)<br>• Vercel Config: [`vercel.json:L1-L7`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/vercel.json#L1-L7) |
| **8** | **Responsive Glassmorphic UI Dashboard** | Swiss-style responsive HTML5/CSS3 single-page dashboard with SVG metrics visualization and live feedback. | • Markup & CSS: [`templates/index.html:L1-L843`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/templates/index.html#L1-L843) |
| **9** | **HTML5 Webcam Frame Capture** | `navigator.mediaDevices.getUserMedia` video stream capture to hidden canvas element and Blob conversion. | • Video Element: [`templates/index.html:L768`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/templates/index.html#L768)<br>• JS Camera Stream Handler: [`templates/index.html:L899-L962`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/templates/index.html#L899-L962) |

---

## Part 3: Deployment Options Summary

1. **Local Desktop / Laptop**:
   `python app.py` (Runs on `http://localhost:5000`)
2. **Raspberry Pi OS**:
   `./deploy_raspberry_pi.sh` then `python app.py`
3. **Docker Container**:
   `docker build -t aesthetic-intelligence-engine .` && `docker run -p 5000:5000 aesthetic-intelligence-engine`
4. **Vercel Serverless**:
   `vercel --prod`
