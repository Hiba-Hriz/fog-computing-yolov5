import cv2
import requests
import numpy as np
import time
import socket

# Configuration ip
DETECTION_NODE_URL = "http://10.26.13.188:5001/detect"  # Nœud 2 
RESULT_NODE_URL = "http://10.26.14.17:5002/receive_results"  # Nœud 3

def test_connection():
    """Test complet de la connexion"""
    print("🔍 TEST DE CONNEXION")
    print("=" * 40)
    
    # Test ping
    try:
        import subprocess
        result = subprocess.run(["ping", "-n", "2", "10.26.13.188"], 
                              capture_output=True, text=True, timeout=5)
        if "TTL=" in result.stdout:
            print("✅ Ping vers 10.26.13.188: OK")
        else:
            print("❌ Ping échoué")
    except:
        print("❌ Test ping échoué")
    
    # Test port
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(("10.26.13.188", 5001))
        sock.close()
        if result == 0:
            print("✅ Port 5001: OUVERT")
        else:
            print("❌ Port 5001: FERMÉ")
    except Exception as e:
        print(f"❌ Test port: {e}")
    
    # Test service HTTP
    try:
        response = requests.get("http://10.26.13.188:5001/health", timeout=5)
        if response.status_code == 200:
            print("✅ Service HTTP: ACTIF")
            print(f"   Réponse: {response.json()}")
        else:
            print(f"⚠️  Service HTTP: {response.status_code}")
    except requests.exceptions.ConnectTimeout:
        print("❌ Service HTTP: TIMEOUT")
    except requests.exceptions.ConnectionError:
        print("❌ Service HTTP: CONNEXION REFUSÉE")
    except Exception as e:
        print(f"❌ Service HTTP: {e}")

def send_to_detection_node(image_data, filename="capture.jpg"):
    """Envoie l'image au nœud de détection"""
    try:
        print(f"   📤 Envoi à {DETECTION_NODE_URL}...")
        response = requests.post(
            DETECTION_NODE_URL,
            files={"image": (filename, image_data, "image/jpeg")},
            timeout=15
        )
        
        if response.status_code == 200:
            print("   ✅ Réponse reçue du nœud 2")
            return response.json()
        else:
            print(f"   ❌ Erreur HTTP {response.status_code}")
            return None
            
    except requests.exceptions.ConnectTimeout:
        print("   ❌ Timeout - Le nœud 2 ne répond pas")
        print("   💡 Vérifiez que 'python fog_node2_detection.py' est lancé sur 10.26.13.188")
        return None
    except requests.exceptions.ConnectionError:
        print("   ❌ Connexion refusée")
        print("   💡 Vérifiez le firewall et que le service écoute sur le bon port")
        return None
    except Exception as e:
        print(f"   ❌ Erreur inattendue: {e}")
        return None

def main():
    print("=" * 60)
    print("📷 NŒUD 1 - SYSTÈME DE CAPTURE")
    print("=" * 60)
    print(f"📍 Nœud 2: 10.26.13.188:5001")
    print(f"📍 Nœud 3: 10.26.14.17:5002")
    
    # Test de connexion
    test_connection()
    
    print("\n" + "=" * 40)
    input("Appuyez sur Entrée pour continuer...")
    
    # Initialisation caméra
    print("\n📹 Initialisation caméra...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Impossible d'ouvrir la caméra")
        return
    
    print("✅ Caméra prête")
    print("\n🎯 INSTRUCTIONS:")
    print("• C = Capturer et envoyer")
    print("• Q = Quitter")
    print("-" * 30)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Affichage
        display_frame = frame.copy()
        cv2.putText(display_frame, "C=Capture, Q=Quit", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        cv2.imshow("Node 1 - Camera", display_frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            print("\n📸 CAPTURE...")
            
            # Sauvegarde debug
            cv2.imwrite("last_capture.jpg", frame)
            print("   💾 Image sauvegardée: last_capture.jpg")
            
            # Encodage
            _, img_encoded = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
            image_data = img_encoded.tobytes()
            
            # Envoi au nœud 2
            detection_results = send_to_detection_node(image_data)
            
            if detection_results and detection_results.get("status") == "success":
                print(f"   ✅ DETECTION: {detection_results['count']} objets")
                
                # Afficher les objets
                for obj in detection_results['objects']:
                    print(f"      • {obj['class']} ({obj['confidence']:.2f})")
                
                # Envoi au nœud 3
                print("   📤 Envoi au nœud 3...")
                try:
                    response = requests.post(RESULT_NODE_URL, json=detection_results, timeout=10)
                    if response.status_code == 200:
                        print("      ✅ Résultats envoyés au nœud 3")
                    else:
                        print(f"      ❌ Erreur nœud 3: {response.status_code}")
                except Exception as e:
                    print(f"      ❌ Erreur nœud 3: {e}")
                    
            else:
                print("   ❌ Échec de la détection")
            
            print("-" * 40)
            
        elif key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("✅ Programme terminé")

if __name__ == "__main__":
    main()
