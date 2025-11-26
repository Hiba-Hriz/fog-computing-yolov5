# fog-computing-yolov5
Système distribué de détection d'objets avec fog computing
Flux de Données
📸 Capture : Le Nœud 1 capture une image depuis la webcam

🔍 Détection : Envoi au Nœud 2 pour analyse YOLOv5

💾 Stockage : Les résultats sont sauvegardés sur le Nœud 3

📡 Consultation : API REST pour accéder à l'historique

🚀 Installation Rapide
Prérequis
Python 3.8 ou supérieur

Webcam fonctionnelle

Connexion réseau entre les machines

Installation des Dépendances
# Cloner le repository
git clone https://github.com/Hiba-Hriz/fog-computing-yolov5.git

cd fog-computing-yolov5

# Installer les dépendances
pip install -r requirements.txt
📦 Dépendances Principales
flask>=2.0.0          # Serveurs web API
torch>=1.7.0          # Machine Learning
torchvision>=0.8.0    # Vision par ordinateur
opencv-python>=4.5.0  # Traitement d'images
requests>=2.25.0      # Communication HTTP
numpy>=1.19.0         Calculs scientifiques
🛠️ Utilisation
🎯 Démarrage du Système
1. Démarrer le Nœud 3 (Résultats)
cd node3_results
python fog_node3_results.py
2. Démarrer le Nœud 2 (Détection YOLOv5)
cd node2_detection
python fog_node2_detection.py
3. Démarrer le Nœud 1 (Capture)
cd node1_camera
python fog_node1_camera.py
