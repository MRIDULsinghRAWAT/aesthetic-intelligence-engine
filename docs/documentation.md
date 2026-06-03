# Phase 1 Documentation

## Selected Model: MobileNetV2
- Lightweight CNN architecture by Google
- Only 2.4M parameters
- Pre-trained on ImageNet (1000 classes)
- Ideal for edge/mobile deployment

## Why MobileNetV2?
- Small size (~10MB)
- Fast inference (~11ms)
- TFLite compatible
- Good accuracy for binary classification

## Selected Dataset: BIQ2021
- Full name: Blind Image Quality 2021
- Source: Kaggle
- 12,000 real-world images
- Labels: MOS (Mean Opinion Score) 0.0 to 1.0
- Higher MOS = Better aesthetic quality

## Labeling Strategy
- MOS > 0.5 = Good image (label: 1) → 6,824 images
- MOS <= 0.5 = Bad image (label: 0) → 5,176 images

## Training Setup
- Subset: 2000 images (Colab RAM constraint)
- Image size: 128x128
- Epochs: 10
- Optimizer: Adam
- Loss: Binary Crossentropy

## Conversion
- Original → TFLite → TFLite Quantized (INT8)
- Size reduced from 11.54MB to 2.67MB (4x compression)
