# Phase 3 Technical Documentation: Edge AI & MLOps Implementation

This document details the system architecture, model optimizations, application pipeline, and MLOps deployment strategy for the **On-Device Aesthetic Intelligence Engine**.

---

## 1. Executive Summary

In Phase 3, we transitioned the Edge AI system from a raw model evaluation script into a production-ready local web application with active telemetry and monitoring. The system uses a dynamic-range quantized TensorFlow Lite model to perform lightweight image aesthetic scoring on the edge, logging every invocation to a local MLflow repository for model audit and latency analysis.

---

## 2. System Architecture

The following diagram illustrates the complete edge inference, real-time image enhancement, and MLOps logging pipeline:

![System Architecture](architecture_diagram.png)

### Components:
- **Client (Browser)**: A glassmorphic dark-theme SPA that supports drag-and-drop file uploads, real-time webcam video stream capturing, image previews, and prediction score visualizations.
- **Flask Backend (`app.py`)**: Runs locally, receives HTTP POST requests (`/predict` and `/enhance`), feeds processed frames to the TFLite interpreter, and returns JSON responses.
- **Preprocessing Pipeline (OpenCV)**: Decodes, resizes, and normalizes input. For the `/enhance` route, it additionally applies CLAHE local contrast tuning and a 2D sharpening kernel to boost image details.
- **TFLite Interpreter**: Loads the quantized `model_dynamic_quant.tflite` model, allocates input/output tensors, and executes forward pass predictions.
- **MLflow tracking server**: Logs parameters and metrics in a SQL-based store (`mlflow.db`) for tracking performance drift, latencies, and output scores.

---

## 3. Model Optimization

To allow efficient runtimes on mobile and edge devices, we compressed the model using **Dynamic Range Quantization** via TensorFlow Lite:

| Metric | Original Float32 Model | Optimized (Dynamic Range Quantized) |
| :--- | :--- | :--- |
| **File Size** | ~10 MB+ | **2.54 MB** (approx. 4x reduction) |
| **Weight Precision** | 32-bit Floating Point | 8-bit Integer (quantized on disk) |
| **Inference Latency** | Higher CPU overhead | **Sub-5ms** average on edge/desktop CPU |
| **Accuracy Loss** | Reference Base | Negligible ($\le 1\%$ deviation) |

During inference, weights are converted dynamically from 8-bit integer to float32 for math calculations, keeping disk footprint small and memory usage minimal.

---

## 4. Input Preprocessing Pipeline

To ensure the model receives predictions consistent with its training data, we process incoming images in real-time using OpenCV:
1. **Decode Raw Stream**: The file stream uploaded by the client is read into a numpy buffer and decoded into BGR format:
   ```python
   img_array = np.frombuffer(file.read(), np.uint8)
   img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
   ```
2. **Resize**: Resize the dimensions to the model's required input size of $128 \times 128$ pixels:
   ```python
   img_resized = cv2.resize(img, (128, 128))
   ```
3. **Normalization & Dimension Expansion**: The pixel intensities are normalized from $[0, 255]$ to $[0, 1.0]$ and expanded to add a batch size dimension:
   ```python
   inp = np.expand_dims(img_resized / 255.0, axis=0).astype(np.float32)
   ```

---

## 5. MLOps Monitoring Setup

Every prediction triggers a log to **MLflow**, registering:
- **Experiment Name**: `aesthetic-intelligence-engine`
- **Params**:
  - `model`: `"dynamic_range_quantized"`
- **Metrics**:
  - `score`: Aesthetic value calculated by the model ($[0.0, 1.0]$).
  - `latency_ms`: Duration of the forward-pass execution (TFLite interpreter launch to completion).

This telemetry loop allows operators to monitor server-side performance and ensure latency does not spike over time.

---

## 6. How to Deploy Locally

### Prerequisites
Install all required libraries:
```bash
pip install flask tensorflow opencv-python mlflow
```

### Steps to Run
1. Start the Flask application:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```
3. Drag-and-drop or select an image to test prediction.
4. To view the MLflow logs dashboard, run the following in a separate terminal:
   ```bash
   mlflow ui --backend-store-uri sqlite:///mlflow.db
   ```
   Then navigate to `http://localhost:5000` (or `http://localhost:5001` depending on port conflicts) to view metric distributions and parameters.
