# fog-computing-yolov5
Système distribué de détection d'objets avec fog computing

## Flux de Données

- 📸 **Capture** : Le Nœud 1 capture une image depuis la webcam
- 🔍 **Détection** : Envoi au Nœud 2 pour analyse YOLOv5
- 💾 **Stockage** : Les résultats sont sauvegardés sur le Nœud 3
- 📡 **Consultation** : API REST pour accéder à l'historique

## Prérequis

- Python 3.8 ou supérieur
- Webcam fonctionnelle
- Connexion réseau entre les machines

## Installation des Dépendances

```bash
pip install flask torch torchvision opencv-python numpy requests
```
Installer YOLOv5(Pour le Nœud 2)

⚠️ Important : Cette étape doit être effectuée sur le PC qui hébergera le Nœud 2

```bash
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
```
Placer le fichier fog_node2_detection.py dans le dossier yolov5

Configuration Réseau
Modifiez les adresses IP dans node1_camera/fog_node1_camera.py :
```bash
DETECTION_NODE_URL = "http://IP_DU_NOEUD_2:5001/detect"
RESULT_NODE_URL = "http://IP_DU_NOEUD_3:5002/receive_results"
```
Utilisation
Démarrage du Système

1-Démarrer le Nœud 3 (Résultats)
```bash
cd node3_results
python fog_node3_results.py
```
2-Démarrer le Nœud 2 (Détection YOLOv5)
```bash
cd node2_detection
python fog_node2_detection.py
```
3-Démarrer le Nœud 1 (Capture)
```bash
cd node1_camera
python fog_node1_camera.py
```
