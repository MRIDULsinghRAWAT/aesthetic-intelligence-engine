from flask import Flask, request, jsonify, render_template, send_file
import tensorflow as tf
import numpy as np
import cv2
import time
import logging

app = Flask(__name__)
logging.basicConfig(filename='inference_logs.txt', level=logging.INFO)

interpreter = tf.lite.Interpreter(model_path="models/model_dynamic_quant.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/mridul.jpg")
def mridul_img():
    return send_file("mridul.jpg")

@app.route("/mridul_avatar.jpg")
def mridul_avatar():
    return send_file("mridul_avatar.jpg")

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["image"]
    img_array = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    img_resized = cv2.resize(img, (128, 128)) / 255.0
    inp = np.expand_dims(img_resized, axis=0).astype(np.float32)

    start = time.time()
    interpreter.set_tensor(input_details[0]['index'], inp)
    interpreter.invoke()
    latency = (time.time() - start) * 1000
    score = float(interpreter.get_tensor(output_details[0]['index'])[0][0])
    label = "Good Aesthetic" if score > 0.5 else "Bad Aesthetic"

    logging.info(f"score={score:.3f}, label={label}, latency={latency:.2f}ms")

    try:
        import mlflow
        mlflow.set_experiment("aesthetic-intelligence-engine")
        with mlflow.start_run():
            mlflow.log_metric("score", score)
            mlflow.log_metric("latency_ms", latency)
            mlflow.log_param("model", "dynamic_range_quantized")
    except Exception as e:
        logging.error(f"MLflow logging failed: {e}")

    return jsonify({
        "score": round(score, 3),
        "label": label,
        "latency_ms": round(latency, 2)
    })

@app.route("/enhance", methods=["POST"])
def enhance():
    import base64
    file = request.files["image"]
    img_array = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    # 1. Apply CLAHE contrast enhancement in YCrCb space
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(ycrcb)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    y_opt = clahe.apply(y)
    ycrcb_opt = cv2.merge((y_opt, cr, cb))
    img_enhanced = cv2.cvtColor(ycrcb_opt, cv2.COLOR_YCrCb2BGR)
    
    # 2. Sharpening filter to boost edge aesthetics
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    img_sharpened = cv2.filter2D(img_enhanced, -1, kernel)
    
    # Preprocess for prediction
    img_resized = cv2.resize(img_sharpened, (128, 128)) / 255.0
    inp = np.expand_dims(img_resized, axis=0).astype(np.float32)
    
    start = time.time()
    interpreter.set_tensor(input_details[0]['index'], inp)
    interpreter.invoke()
    latency = (time.time() - start) * 1000
    score = float(interpreter.get_tensor(output_details[0]['index'])[0][0])
    label = "Good Aesthetic" if score > 0.5 else "Bad Aesthetic"
    
    # Log to MLflow
    try:
        import mlflow
        mlflow.set_experiment("aesthetic-intelligence-engine")
        with mlflow.start_run():
            mlflow.log_metric("enhanced_score", score)
            mlflow.log_metric("enhanced_latency_ms", latency)
            mlflow.log_param("model", "dynamic_range_quantized_enhanced")
    except Exception as e:
        logging.error(f"MLflow logging failed: {e}")
        
    _, buffer = cv2.imencode('.png', img_sharpened)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    
    return jsonify({
        "score": round(score, 3),
        "label": label,
        "latency_ms": round(latency, 2),
        "image_data": f"data:image/png;base64,{img_base64}"
    })

if __name__ == "__main__":
    print("Server starting at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, use_reloader=False)