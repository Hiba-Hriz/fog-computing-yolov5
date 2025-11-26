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

```markdown

Cloner le Repository

```bash
git clone https://github.com/Hiba-Hriz/fog-computing-yolov5.git
cd fog-computing-yolov5

