# fog-computing-yolov5
Système distribué de détection d'objets avec fog computing

## Flux de Données

- 📸 **Capture** : Le Nœud 1 capture une image depuis la webcam
- 🔍 **Détection** : Envoi au Nœud 2 pour analyse YOLOv5
- 📡 **Consultation** : API REST pour accéder à l'historique

## Prérequis

- Python 3.8 ou supérieur
- Webcam fonctionnelle
- Connexion réseau entre les machines

## Installation des Dépendances

```bash
pip install flask torch torchvision opencv-python numpy requests
```
## Installer YOLOv5(Pour le Nœud 2)

⚠️ Important : Cette étape doit être effectuée sur le PC qui hébergera le Nœud 2

```bash
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
```
⚡ Étape clé :

Placer le fichier fog_node2_detection.py à l’intérieur du dossier yolov5.

Cela permet au script de trouver correctement les modules et fichiers du projet YOLOv5.

## Configuration Réseau
Modifiez les adresses IP dans node1_camera/fog_node1_camera.py :
```bash
DETECTION_NODE_URL = "http://IP_DU_NOEUD_2:5001/detect"
RESULT_NODE_URL = "http://IP_DU_NOEUD_3:5002/receive_results"
```
## Utilisation

1-Démarrer le Nœud 3 (Résultats)
```bash
python fog_node3_results.py
```
2-Démarrer le Nœud 2 (Détection YOLOv5)
```bash
python fog_node2_detection.py
```
3-Démarrer le Nœud 1 (Capture)
```bash
python fog_node1_camera.py
```
