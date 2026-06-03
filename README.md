# Aesthetic Intelligence Engine

Edge AI system for on-device aesthetic scoring using MobileNetV2 and TFLite.

## Phase 1 - Edge AI Foundation & Model Selection

### Objective
Build a basic AI pipeline capable of performing inference on-device using lightweight models.

### Model
- **Architecture:** MobileNetV2 (pretrained on ImageNet)
- **Task:** Binary aesthetic classification (Good/Bad image)
- **Input Size:** 128x128x3
- **Parameters:** 2,422,081

### Dataset
- **Name:** BIQ2021 (Image Quality Assessment)
- **Source:** Kaggle
- **Size:** 12,000 images
- **Labels:** MOS (Mean Opinion Score) 0.0 → 1.0
- **Split:** MOS > 0.5 = Good (1), MOS ≤ 0.5 = Bad (0)
- **Training subset:** 2000 images (Colab RAM constraint)

### Results
| Model | Size | Latency | Val Accuracy |
|---|---|---|---|
| Original (.h5) | 11.54 MB | N/A | 71.0% |
| TFLite | 9.52 MB | 11.25 ms | 71.0% |
| TFLite Quantized | 2.67 MB | 11.88 ms | 71.0% |

### Tech Stack
- Python, TensorFlow 2.x
- TFLite (Edge AI Framework)
- OpenCV (Image Processing)
- Google Colab (Training Environment)

### Project Structure

    aesthetic-intelligence-engine/
    ├── notebooks/    # Training notebook
    ├── models/       # Saved .h5 and .tflite models
    ├── reports/      # Performance comparison report
    ├── inference/    # Inference scripts
    └── data/         # Dataset (stored on Google Drive)

### Note
Full dataset training (12k images) recommended for production.
2000 image subset used due to Colab free tier RAM constraints.
