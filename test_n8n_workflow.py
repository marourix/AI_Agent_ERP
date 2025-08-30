#!/usr/bin/env python3
"""
Script de test pour le workflow n8n Atracio ERP
Teste toutes les actions disponibles via le webhook
"""

import requests
import json
import time
from typing import Dict, Any

class AtracioN8NTest:
    def __init__(self, n8n_base_url: str = "http://localhost:5678"):
        self.n8n_base_url = n8n_base_url
        self.webhook_url = f"{n8n_base_url}/webhook/atracio-webhook"
        
    def test_webhook(self, action: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Teste une action spécifique via le webhook"""
        try:
            payload = {"action": action, **data}
            print(f"🔍 Testing action: {action}")
            print(f"📤 Payload: {json.dumps(payload, indent=2)}")
            
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            print(f"📥 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Response: {json.dumps(result, indent=2)}")
                return result
            else:
                print(f"❌ Error Response: {response.text}")
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to n8n at {self.n8n_base_url}")
            print("Make sure n8n is running and accessible")
            return {"success": False, "error": "Connection failed"}
        except requests.exceptions.Timeout:
            print("❌ Request timeout")
            return {"success": False, "error": "Timeout"}
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return {"success": False, "error": str(e)}
        finally:
            print("-" * 50)
    
    def test_all_actions(self):
        """Teste toutes les actions disponibles"""
        print("🚀 Starting Atracio N8N Workflow Tests")
        print("=" * 50)
        
        # Test 1: Vérifier le stock d'un SKU spécifique
        self.test_webhook("check_stock", {"sku": "SKU123"})
        time.sleep(1)
        
        # Test 2: Créer un bon de commande
        self.test_webhook("create_purchase_order", {
            "sku": "SKU456",
            "quantity": 25
        })
        time.sleep(1)
        
        # Test 3: Vérifier le statut d'une commande
        self.test_webhook("check_order_status", {"order_id": "ORD001"})
        time.sleep(1)
        
        # Test 4: Obtenir tous les stocks
        self.test_webhook("get_all_stock", {})
        time.sleep(1)
        
        # Test 5: Obtenir toutes les commandes
        self.test_webhook("get_all_orders", {})
        time.sleep(1)
        
        # Test 6: Obtenir tous les bons de commande
        self.test_webhook("get_all_purchase_orders", {})
        time.sleep(1)
        
        # Test 7: Test avec des données invalides
        print("🧪 Testing error handling...")
        self.test_webhook("check_stock", {})  # SKU manquant
        time.sleep(1)
        
        self.test_webhook("create_purchase_order", {
            "sku": "SKU999",
            "quantity": -5  # Quantité négative
        })
        time.sleep(1)
        
        # Test 8: Action invalide
        self.test_webhook("invalid_action", {"test": "data"})
        
        print("\n🎯 All tests completed!")
    
    def test_specific_scenarios(self):
        """Teste des scénarios spécifiques"""
        print("\n🎭 Testing specific scenarios...")
        print("=" * 50)
        
        # Test de création de plusieurs bons de commande
        for i in range(3):
            self.test_webhook("create_purchase_order", {
                "sku": "SKU123",
                "quantity": 10 + i * 5
            })
            time.sleep(1)
        
        # Test de vérification de stock avec différents SKUs
        skus = ["SKU123", "SKU456", "SKU789"]
        for sku in skus:
            self.test_webhook("check_stock", {"sku": sku})
            time.sleep(1)
    
    def health_check(self):
        """Vérifie la santé du système"""
        print("🏥 Health Check")
        print("=" * 50)
        
        # Vérifier n8n
        try:
            n8n_response = requests.get(f"{self.n8n_base_url}/healthz", timeout=5)
            print(f"✅ n8n: {'OK' if n8n_response.status_code == 200 else 'ERROR'}")
        except:
            print("❌ n8n: Not accessible")
        
        # Vérifier l'API ERP
        try:
            erp_response = requests.get("http://localhost:5000/Atracio", timeout=5)
            print(f"✅ ERP API: {'OK' if erp_response.status_code == 200 else 'ERROR'}")
        except:
            print("❌ ERP API: Not accessible")
        
        print("-" * 50)

def main():
    """Fonction principale"""
    print("Atracio ERP Agent - N8N Workflow Test Suite")
    print("=" * 60)
    
    # Configuration
    n8n_url = input("Enter n8n base URL (default: http://localhost:5678): ").strip()
    if not n8n_url:
        n8n_url = "http://localhost:5678"
    
    # Créer l'instance de test
    tester = AtracioN8NTest(n8n_url)
    
    # Menu de test
    while True:
        print("\n Test Menu:")
        print("1. Health Check")
        print("2. Test All Actions")
        print("3. Test Specific Scenarios")
        print("4. Test Single Action")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            tester.health_check()
        elif choice == "2":
            tester.test_all_actions()
        elif choice == "3":
            tester.test_specific_scenarios()
        elif choice == "4":
            print("\n🔧 Single Action Test")
            action = input("Enter action (e.g., check_stock): ").strip()
            if action:
                if action == "check_stock":
                    sku = input("Enter SKU: ").strip()
                    tester.test_webhook(action, {"sku": sku})
                elif action == "create_purchase_order":
                    sku = input("Enter SKU: ").strip()
                    quantity = input("Enter quantity: ").strip()
                    try:
                        quantity = int(quantity)
                        tester.test_webhook(action, {"sku": sku, "quantity": quantity})
                    except ValueError:
                        print(" Quantity must be a number")
                elif action == "check_order_status":
                    order_id = input("Enter Order ID: ").strip()
                    tester.test_webhook(action, {"order_id": order_id})
                elif action in ["get_all_stock", "get_all_orders", "get_all_purchase_orders"]:
                    tester.test_webhook(action, {})
                else:
                    print("Unknown action")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print(" Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    main()

