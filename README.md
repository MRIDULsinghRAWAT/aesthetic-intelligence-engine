# Aesthetic Intelligence Engine

Edge AI system for on-device aesthetic scoring using MobileNetV2 and TFLite. Built as part of the Ultimez Technology internship program.

## Project Overview

This project builds an AI system capable of running computer-vision models directly on edge devices, focused on binary aesthetic classification (Good/Bad image quality) with minimal latency and model size, suitable for mobile deployment.

---

## Phase 1 - Edge AI Foundation & Model Selection

### Objective
Build a basic AI pipeline capable of performing inference on-device using lightweight models.

### Model
- **Architecture:** MobileNetV2 (pretrained on ImageNet, frozen base)
- **Task:** Binary aesthetic classification (Good/Bad image)
- **Input Size:** 128x128x3
- **Parameters:** 2,422,081
- **Training:** 2000 image subset, 10 epochs (Colab RAM constraint)

### Results
| Model | Size | Latency | Val Accuracy |
|---|---|---|---|
| Original (.h5) | 11.54 MB | N/A | 71.0% |
| TFLite | 9.52 MB | 11.25 ms | 71.0% |
| TFLite Quantized | 2.67 MB | 11.88 ms | 71.0% |

---

## Phase 2 - Model Optimization & On-Device Inference

### Objective
Optimize the AI model for efficient on-device inference using the full dataset, while maintaining performance and accuracy.

### Improvements Over Phase 1
- Trained on the **full 12,000 image dataset** using a `tf.data` pipeline (instead of a 2000 image RAM-loaded subset), improving generalization.
- Applied **three quantization strategies** for deployment flexibility: Dynamic Range, Float16, and Full INT8.
- Benchmarked inference latency across all variants on simulated edge conditions.
- Generated visual demo predictions on real validation images.

### Note on Pruning
Weight pruning via `tensorflow-model-optimization` was attempted but is currently incompatible with Keras 3 (TensorFlow 2.20 default), a known library limitation. Model compression was instead achieved through multiple quantization strategies, which provided comparable size reduction (up to 4.3x).

### Results (Full 12k Dataset)
| Model | Size | Latency | Val Accuracy |
|---|---|---|---|
| Original (.h5) | 11.54 MB | N/A | 72.5% |
| Dynamic Range Quantized | 2.67 MB | 11.58 ms | ~72% |
| Float16 Quantized | 4.79 MB | 7.77 ms | ~72.5% |
| Full INT8 Quantized | 2.87 MB | 9.59 ms | ~70-71% |

**Best trade-off:** Dynamic Range Quantization (smallest size with minimal accuracy loss). **Fastest:** Float16 (best for GPU-accelerated edge devices).

### Demo
On-device inference was demonstrated on 6 real validation images, correctly classifying aesthetically pleasing images (sunflowers, drinks, skyline) as "Good" and a blurred/dark image as "Bad". See `reports/demo_predictions.png` and demo video.

### Demo Video
[Watch Phase 2 On-Device Inference Demo](reports/phase2_demo_inference.mp4)

### Extended Phase 2 Benchmarks
Detailed memory usage, energy efficiency, real-time FPS, and edge application 
integration results: [phase2_extended_benchmark.md](reports/phase2_extended_benchmark.md)

A lightweight Flask-based inference API (`inference/app.py`) was also built to 
demonstrate edge application integration, exposing a `/predict` endpoint for 
image-based aesthetic scoring.



---

## Dataset
- **Name:** BIQ2021 (Image Quality Assessment)
- **Source:** Kaggle
- **Size:** 12,000 images
- **Labels:** MOS (Mean Opinion Score), range 0.0 to 1.0
- **Label Split:** MOS > 0.5 = Good (1), MOS <= 0.5 = Bad (0) → 6,824 Good / 5,176 Bad

## Tech Stack
- Python, TensorFlow 2.x
- TFLite (Edge AI Framework)
- OpenCV (Image Processing)
- tensorflow-model-optimization (attempted)
- Google Colab (Training Environment)

## Project Structure

    aesthetic-intelligence-engine/
    ├── notebooks/    # Training notebooks (Phase 1 + Phase 2)
    ├── models/       # Saved .h5 and .tflite models (all quantization variants)
    ├── reports/      # Performance comparison reports and demo predictions
    ├── inference/    # Inference scripts
    ├── docs/         # Model and dataset documentation
    └── data/         # Dataset (stored on Google Drive, not committed)

## How to Run Inference

    python inference/run_inference.py path/to/image.jpg

Loads the quantized TFLite model and outputs an aesthetic score, label (Good/Bad), and inference latency.

## Future Work (Phase 3)
- Build a practical edge AI application with real-time camera input
- MLOps pipeline for model versioning and monitoring
- Deployment to Android or Raspberry Pi
