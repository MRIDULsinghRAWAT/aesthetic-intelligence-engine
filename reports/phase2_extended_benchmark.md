# Phase 2 Extended Benchmark

## Memory Usage
- Dynamic Range: 2.55 MB
- Float16: 14.22 MB
- Full INT8: 2.74 MB

## Energy Efficiency (CPU Time Proxy)
- Dynamic Range: 12.28 ms/inference
- Float16: 7.65 ms/inference
- Full INT8: 7.59 ms/inference

## Real-Time Performance (Dynamic Range Model)
- Avg Latency: 13.97 ms/frame
- Throughput: 71.6 FPS
- Verdict: Real-time capable

## Edge Application
A lightweight Flask-based inference API (inference/app.py) simulates edge
application integration with a /predict endpoint for aesthetic scoring,
deployable to Raspberry Pi or any edge server.

## Note on Pruning
Weight pruning via tensorflow-model-optimization was attempted but is
incompatible with Keras 3 (TF 2.20 default) — a known library limitation.
Compression was achieved instead via multiple quantization strategies
(Dynamic Range, Float16, Full INT8).
