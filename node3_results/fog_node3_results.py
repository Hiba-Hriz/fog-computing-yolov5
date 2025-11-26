# fog_node3_results.py
from flask import Flask, request, jsonify
import json
import time
import socket
from datetime import datetime
import os

app = Flask(_name_)

# Stockage des résultats
results_history = []

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
print(f"✅ Nœud 3 - Réception résultats prêt! http://{local_ip}:5002")

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy", 
        "role": "results_node", 
        "ip": local_ip,
        "results_count": len(results_history)
    })

@app.route('/receive_results', methods=['POST'])
def receive_results():
    """Reçoit les résultats de détection du nœud 2"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data received", "status": "error"}), 400
        
        # Ajouter un timestamp et sauvegarder
        data['received_at'] = datetime.now().isoformat()
        data['results_node'] = local_ip
        
        results_history.append(data)
        
        # Limiter l'historique à 100 entrées
        if len(results_history) > 100:
            results_history.pop(0)
        
        print(f"📥 Résultats reçus: {data['count']} objets détectés")
        print(f"   Classes: {[obj['class'] for obj in data['objects']]}")
        print(f"   Latence: {data['latency_ms']} ms")
        
        return jsonify({
            "status": "success", 
            "message": f"Results received: {data['count']} objects",
            "results_count": len(results_history)
        })
        
    except Exception as e:
        return jsonify({"error": f"Error processing results: {str(e)}", "status": "error"}), 500

@app.route('/get_results', methods=['GET'])
def get_results():
    """Retourne l'historique des résultats"""
    return jsonify({
        "history": results_history,
        "total_results": len(results_history)
    })

@app.route('/latest_result', methods=['GET'])
def latest_result():
    """Retourne le dernier résultat"""
    if results_history:
        return jsonify(results_history[-1])
    else:
        return jsonify({"message": "No results available"})

@app.route('/clear_results', methods=['POST'])
def clear_results():
    """Efface l'historique des résultats"""
    results_history.clear()
    return jsonify({"message": "Results history cleared"})

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5002, debug=False)