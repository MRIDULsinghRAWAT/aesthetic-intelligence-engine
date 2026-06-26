# Phase 2 Extended Benchmark

## Memory Usage
- Dynamic Range: 9.77 MB
- Float16: 16.52 MB
- Full INT8: 4.13 MB

## Energy Efficiency (CPU Time Proxy)
- Dynamic Range: 12.10 ms/inference
- Float16: 7.71 ms/inference
- Full INT8: 7.45 ms/inference

## Real-Time Performance (Dynamic Range Model)
- Avg Latency: 23.41 ms/frame
- Throughput: 42.7 FPS
- Verdict: Real-time capable

## Edge Application
A lightweight Flask-based inference API (inference/app.py) simulates edge
application integration with a /predict endpoint for aesthetic scoring.

## Note on Pruning
Weight pruning via tensorflow-model-optimization was attempted but is
incompatible with Keras 3 (TF 2.20 default) — a known library limitation.
Compression was achieved instead via multiple quantization strategies.
