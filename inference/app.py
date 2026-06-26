
from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import cv2

app = Flask(__name__)
interpreter = tf.lite.Interpreter(model_path="models/model_dynamic_quant.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["image"]
    img_array = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (128,128)) / 255.0
    inp = np.expand_dims(img, axis=0).astype(np.float32)
    interpreter.set_tensor(input_details[0]["index"], inp)
    interpreter.invoke()
    score = float(interpreter.get_tensor(output_details[0]["index"])[0][0])
    label = "Good" if score > 0.5 else "Bad"
    return jsonify({"score": score, "label": label})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
