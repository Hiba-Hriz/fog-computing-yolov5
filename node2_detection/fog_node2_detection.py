# fog_node2_detection.py
from flask import Flask, request, jsonify
import cv2
import numpy as np
import torch
import time
import socket
from models.experimental import attempt_load
from utils.general import non_max_suppression, scale_boxes
from utils.torch_utils import select_device

app = Flask(_name_)

print("Loading YOLOv5 model...")
device = select_device('cpu')
model = attempt_load('yolov5s.pt', device=device)
model.eval()

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return socket.gethostbyname(socket.gethostname())

local_ip = get_local_ip()
print(f"✅ Nœud 2 - Détection prêt! http://{local_ip}:5001")

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "role": "detection_node", "ip": local_ip})

@app.route('/detect', methods=['POST'])
def detect():
    start_time = time.time()

    if 'image' not in request.files:
        return jsonify({"error": "No image", "status": "error"}), 400

    try:
        file = request.files['image']
        nparr = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({"error": "Invalid image", "status": "error"}), 400

        original_shape = img.shape

        # Preprocess
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_resized = cv2.resize(img_rgb, (640, 640))
        
        img_tensor = torch.from_numpy(img_resized).to(device).float()
        img_tensor = img_tensor.permute(2, 0, 1).unsqueeze(0) / 255.0

        # Inference
        with torch.no_grad():
            pred = model(img_tensor)[0]
            pred = non_max_suppression(pred, conf_thres=0.4, iou_thres=0.5)

        # Parse results
        results = []
        names = model.names
        for det in pred:
            if len(det):
                det[:, :4] = scale_boxes(img_tensor.shape[2:], det[:, :4], original_shape).round()
                for *xyxy, conf, cls in det:
                    results.append({
                        "class": names[int(cls)],
                        "confidence": float(conf),
                        "bbox": [int(v) for v in xyxy]
                    })

        return jsonify({
            "objects": results,
            "count": len(results),
            "latency_ms": round((time.time() - start_time) * 1000, 2),
            "status": "success",
            "detection_node": local_ip,
            "timestamp": time.time()
        })

    except Exception as e:
        return jsonify({"error": f"Processing failed: {str(e)}", "status": "error"}), 500

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5001, debug=False)