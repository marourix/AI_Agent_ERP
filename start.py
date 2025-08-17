import subprocess
import time
import sys
import os
import signal
import threading
from pathlib import Path

def check_dependencies():
    try:
        import flask
        import requests
        import agents
        print("Toutes les dépendances sont installées")
        return True
    except ImportError as e:
        print(f"Dépendance manquante: {e}")
        print("Installez les dépendances avec: pip install -r requirements.txt")
        return False

def start_erp_server():
    """Démarrer le serveur ERP Flask"""
    print(" Démarrage du serveur ERP...")
    try:
        # Démarrer le serveur Flask en backend
        process = subprocess.Popen(
            [sys.executable, "erp_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Attendre que le serveur démarre
        time.sleep(3)
        
        # Vérifier si le serveur fonctionne
        try:
            import requests
            response = requests.get("http://localhost:5000/Atracio", timeout=5)
            if response.status_code == 200:
                print("Serveur ERP démarré avec succès sur http://localhost:5000")
                return process
            else:
                print("Le serveur ERP n'a pas démarré correctement")
                process.terminate()
                return None
        except Exception as e:
            print(f"Erreur lors du test du serveur ERP: {e}")
            process.terminate()
            return None
            
    except Exception as e:
        print(f"Erreur lors du démarrage du serveur ERP: {e}")
        return None

def start_agent():
    print("Démarrage de l'agent Atracio...")
    try:
        subprocess.run([sys.executable, "agent.py"], check=True)
    except KeyboardInterrupt:
        print("\n Arrêt de l'agent...")
    except Exception as e:
        print(f" Erreur lors du démarrage de l'agent: {e}")

def main():
    print("=" * 50)
    print(" ATracio ERP Agent - Démarrage automatique")
    print("=" * 50)
    
    # Vérifier les dépendances
    if not check_dependencies():
        sys.exit(1)
    
    # Vérifier que les fichiers nécessaires existent
    required_files = ["erp_server.py", "agent.py", "data.json"]
    for file in required_files:
        if not Path(file).exists():
            print(f" Fichier manquant: {file}")
            sys.exit(1)
    
    print(" Tous les fichiers nécessaires sont présents")
    
    # Démarrer le serveur backend d'ERP
    erp_process = start_erp_server()
    if not erp_process:
        print(" Impossible de démarrer le serveur ERP")
        sys.exit(1)
    
    try:
        # Démarrer l'agent Atracio
        start_agent()
    finally:
        # Nettoyer le processus du serveur ERP
        print(" Arrêt du serveur ERP...")
        erp_process.terminate()
        try:
            erp_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            erp_process.kill()
        print(" Serveur ERP arrêté")

if __name__ == "__main__":
    main()
