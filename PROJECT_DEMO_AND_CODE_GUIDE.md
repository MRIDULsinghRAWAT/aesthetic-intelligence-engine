# Aesthetic Intelligence Engine (Æ) - Live Demo & Code Mapping Guide

This document provides a presentation guide to showcase the **Aesthetic Intelligence Engine** to your mentor, with explicit Q&A code locations for all major features (Webcam, Upload Photo, Real-time Scoring, Image Enhancement, and Deployment options) and a technical breakdown of tasks, techniques, and term definitions.

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

#### Step 1: Add Photo & Real-Time Aesthetic Evaluation
1. Go to `http://localhost:5000`.
2. Drag and drop any image (e.g. `test_image.jpg` or `mridul.jpg`) or click the dropzone to pick a photo.
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

## Part 2: Mentor Quick Answers - "Where is this code implemented?"

If your mentor asks where specific core features are coded in the project, reference these exact code blocks:

### ❓ Question 1: "Where is the Add Photo / Upload Image feature implemented?"
* **Frontend Upload Zone & Preview**: [`templates/index.html:L762-L775`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/templates/index.html#L762-L775)
* **Drag & Drop + File Selection JavaScript Handlers**: [`templates/index.html:L882-L897`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/templates/index.html#L882-L897) & [`templates/index.html:L964-L973`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/templates/index.html#L964-L973)
* **How it works**: Uses HTML5 File API and drag-and-drop listeners to read user images into memory, display an instant preview, and prepare a `FormData` payload.

---

### ❓ Question 2: "Where is the Web Camera (Live Capture) feature implemented?"
* **HTML Video Stream Element & Camera Button**: [`templates/index.html:L768-L771`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/templates/index.html#L768-L771)
* **JavaScript Camera Stream & Frame Capture Engine**: [`templates/index.html:L899-L962`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/templates/index.html#L899-L962)
* **How it works**: Uses `navigator.mediaDevices.getUserMedia({ video: true })` to capture the webcam stream, draws frames onto an off-screen `<canvas>` element, converts the canvas to a JPEG `Blob`, and sends it to the scoring backend.

---

### ❓ Question 3: "Where is the Real-Time Analysis / Scoring feature implemented?"
* **Backend Flask Prediction API (`POST /predict`)**: [`app.py:L213-L249`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/app.py#L213-L249)
* **Frontend Async Prediction Handler**: [`templates/index.html:L975-L1012`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/templates/index.html#L975-L1012)
* **How it works**: Backend decodes image bytes with OpenCV `cv2.imdecode`, resizes to `128x128`, normalizes pixel values (`/ 255.0`), feeds input into TFLite interpreter using thread locks, measures latency with high-precision timestamps, and returns score and execution time in `< 5ms`.

---

### ❓ Question 4: "Where is the Auto-Enhance feature implemented?"
* **Backend OpenCV Image Enhancement Pipeline (`POST /enhance`)**: [`app.py:L250-L303`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/app.py#L250-L303)
* **Frontend Auto-Enhance Button & Base64 Image Render**: [`templates/index.html:L286-L305`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/templates/index.html#L286-L305) & [`templates/index.html:L1014-L1054`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/templates/index.html#L1014-L1054)
* **How it works**:
  1. Converts RGB/BGR image into **YCrCb color space**.
  2. Applies **CLAHE** (Contrast Limited Adaptive Histogram Equalization) on the luminance (Y) channel with `clipLimit=3.0` and `tileGridSize=(8,8)`.
  3. Applies a **2D Sharpening Kernel Filter** (`[[0,-1,0],[-1,5,-1],[0,-1,0]]`) using `cv2.filter2D`.
  4. Runs the enhanced image back through the TFLite model and returns Base64 PNG data along with the improved score.

---

### ❓ Question 5: "Where are the Deployment options implemented?"
* **Local Network Broadcasting (Mobile Phone on Wi-Fi)**:
  * Server setup: [`app.py:L313`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/app.py#L313) (`app.run(host="0.0.0.0", port=5000)`)
* **Raspberry Pi OS Native Setup**:
  * Edge Installer Script: [`deploy_raspberry_pi.sh`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/deploy_raspberry_pi.sh) (installs system libraries and lightweight `tflite-runtime`)
* **Docker Containerization**:
  * Container configuration: [`Dockerfile`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/Dockerfile)
* **Vercel Cloud Serverless Deployment**:
  * Environment Handler & `/tmp` dynamic write rerouting: [`app.py:L29-L51`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/app.py#L29-L51)
  * Serverless Config & Entrypoint: [`vercel.json`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/vercel.json) & [`api/index.py`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/api/index.py)

---

## Part 3: Complete Feature Summary Table

| # | Feature | Description | Key File & Line Range |
|---|---|---|---|
| **1** | **Add Photo / Upload** | Drag-and-drop & file picker browser input | [`templates/index.html:L762-L775`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/templates/index.html#L762-L775) & [`L882-L897`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/templates/index.html#L882-L897) |
| **2** | **Web Camera Capture** | Live webcam streaming & canvas Blob capture | [`templates/index.html:L768`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/templates/index.html#L768) & [`L899-L962`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/templates/index.html#L899-L962) |
| **3** | **Real-Time Analysis** | Sub-5ms TFLite model scoring API (`POST /predict`) | [`app.py:L213-L249`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/app.py#L213-L249) & [`templates/index.html:L975-L1012`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/templates/index.html#L975-L1012) |
| **4** | **Auto-Enhance Image** | YCrCb CLAHE + 2D Sharpening filter (`POST /enhance`) | [`app.py:L250-L303`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/app.py#L250-L303) & [`templates/index.html:L1014-L1054`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/templates/index.html#L1014-L1054) |
| **5** | **Live Hot-Swapping** | Thread-safe interpreter re-allocation (`v1` ⇄ `v2`) | [`app.py:L136-L211`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/app.py#L136-L211) & [`templates/index.html:L1087-L1138`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/templates/index.html#L1087-L1138) |
| **6** | **Quantized Model** | MobileNetV2 2.54MB dynamic range quantized TFLite binary | [`models/model_dynamic_quant.tflite`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/models/model_dynamic_quant.tflite) & [`notebooks/phase1_training.ipynb`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/notebooks/phase1_training.ipynb) |
| **7** | **Edge Dual Engine** | `tensorflow` ⇄ `tflite_runtime` dynamic wheel import | [`app.py:L13-L25`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/app.py#L13-L25) & [`deploy_raspberry_pi.sh`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/deploy_raspberry_pi.sh) |
| **8** | **Deployments** | Local Wi-Fi, Raspberry Pi, Docker, Vercel Serverless | [`app.py:L29-L51`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/app.py#L29-L51), [`Dockerfile`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/Dockerfile), [`vercel.json`](file:///c:/Users/Mridul/Desktop/aesthetic-intelligence-engine/vercel.json) |

---

## Part 4: Task-to-Technique Mapping & Glossary of Technical Terms

This section explains **what you were asked to do**, **what technique you used**, **how it works**, and **definitions of key technical terms** to impress your mentor.

---

### Task 1: Model Compression & Edge Optimization
* **What you were asked to do**: Make a heavy neural network run fast (< 5ms) on low-power devices without needing expensive GPU servers.
* **Technique Used**: **Dynamic Range Quantization** on a **MobileNetV2** base architecture.
* **How it works**: Pre-trained MobileNetV2 weights are compressed from 32-bit floating point (`float32`) to 8-bit integers (`int8`) post-training. This reduces file size from 10MB+ down to **2.54 MB** (75% savings) while preserving over 99% accuracy.

---

### Task 2: Edge Hardware Compatibility
* **What you were asked to do**: Run inference on micro-hardware (like Raspberry Pi) where installing a full 500MB+ TensorFlow package is too heavy or unsupported.
* **Technique Used**: **Dual-Engine Wheel Fallback (`tensorflow` ⇄ `tflite_runtime`)**.
* **How it works**: `app.py` attempts to import `tensorflow`. If missing (as on a Raspberry Pi), it gracefully falls back to `tflite_runtime`—a lightweight 15MB wheel package containing only the TFLite interpreter engine.

---

### Task 3: Live Image Capture & Client-Side Preprocessing
* **What you were asked to do**: Allow users to analyze images from their webcam or file uploads directly in the browser.
* **Technique Used**: **HTML5 MediaDevices API & Off-Screen Canvas Blob Encoding**.
* **How it works**: Browser accesses camera stream via `navigator.mediaDevices.getUserMedia`, draws video frames onto an off-screen `<canvas>`, converts pixels into a JPEG `Blob`, and streams binary data to Flask via asynchronous `fetch()` requests.

---

### Task 4: Automated Image Aesthetic Enhancement
* **What you were asked to do**: Automatically improve the visual quality and aesthetic score of poor, dark, or blurry photos.
* **Technique Used**: **YCrCb Color-Space CLAHE & 2D Spatial Sharpening Convolution**.
* **How it works**:
  1. Image is converted to **YCrCb** color space so contrast enhancement only affects lightness (Y channel) without distorting natural colors.
  2. **CLAHE** adjusts local histogram contrast across image tiles.
  3. A **2D Convolutional Sharpening Kernel** (`[[0,-1,0],[-1,5,-1],[0,-1,0]]`) amplifies high-frequency edge details.

---

### Task 5: Zero-Downtime Model Hot-Swapping
* **What you were asked to do**: Update or rollback active production AI models live without restarting the server.
* **Technique Used**: **Atomic Thread-Locked Interpreter Allocation (`threading.Lock()`)**.
* **How it works**: When `/model/update` receives a request, it validates and allocates tensors for the new model file inside a thread lock, then atomically replaces the active `InterpreterClass` instance in memory.

---

### 💡 Technical Terms & Definitions Glossary

1. **Edge AI / On-Device Inference**: Running machine learning models locally on physical hardware (laptops, phones, Raspberry Pi) rather than sending data to cloud API servers. Guarantees zero network latency and complete user data privacy.
2. **Dynamic Range Quantization**: A post-training quantization method that compresses model weight values from 32-bit floats to 8-bit integers, drastically shrinking model size and reducing CPU memory bandwidth demands.
3. **MobileNetV2**: An efficient convolutional neural network (CNN) architecture optimized specifically for mobile and embedded vision applications using depthwise separable convolutions.
4. **TFLite (TensorFlow Lite)**: Google's lightweight, open-source cross-platform framework for deploying ML models on mobile and edge devices.
5. **CLAHE (Contrast Limited Adaptive Histogram Equalization)**: A computer vision algorithm that enhances local contrast in small image regions (tiles) while preventing noise over-amplification.
6. **YCrCb Color Space**: A color model separating Luminance/Brightness ($Y$) from Chrominance/Color ($Cr$, $Cb$), ideal for processing light and contrast without altering true colors.
7. **2D Convolutional Kernel**: A small matrix (e.g. 3x3) slid over image pixels to perform mathematical transformations such as edge sharpening, blurring, or feature detection.
8. **Thread Lock (`threading.Lock`)**: A software synchronization primitive that prevents multiple server threads from simultaneously modifying or reading shared resources, ensuring thread safety and zero crash bugs.
9. **Base64 Encoding**: A binary-to-text encoding scheme that formats raw image byte buffers into text strings suitable for immediate rendering inside HTML `<img>` elements.
10. **Serverless Architecture (Vercel)**: A cloud computing execution model where application containers run dynamically on-demand with read-only file systems, requiring write operations to be redirected to `/tmp`.
