import tensorflow as tf
import numpy as np
import cv2
import time

# Load TFLite model
def load_model(model_path):
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter

# Run inference on single image
def predict(interpreter, image_path, img_size=(128, 128)):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Load and preprocess image
    img = cv2.imread(image_path)
    img = cv2.resize(img, img_size) / 255.0
    img = np.expand_dims(img, axis=0).astype(np.float32)

    # Inference
    start = time.time()
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    latency = (time.time() - start) * 1000

    score = interpreter.get_tensor(output_details[0]['index'])[0][0]
    label = "Good" if score > 0.5 else "Bad"

    return {
        "score": float(score),
        "label": label,
        "latency_ms": round(latency, 2)
    }

if __name__ == "__main__":
    import sys

    model_path = "models/aesthetic_model_quantized.tflite"
    image_path = sys.argv[1] if len(sys.argv) > 1 else "test.jpg"

    print(f"Loading model: {model_path}")
    interpreter = load_model(model_path)

    print(f"Running inference on: {image_path}")
    result = predict(interpreter, image_path)

    print(f"\nResult:")
    print(f"  Label:   {result['label']}")
    print(f"  Score:   {result['score']:.3f}")
    print(f"  Latency: {result['latency_ms']} ms")
