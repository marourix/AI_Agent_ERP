from flask import Flask, jsonify, request
import json
import uuid
from datetime import datetime
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ERPServer")

app = Flask(__name__)

# Chargement des données de fichier JSON
def load_data():
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("data.json file not found.")
        return {"stock": [], "orders": [], "purchase_orders": []}
    except json.JSONDecodeError:
        logger.error("JSON format error in data.json")
        return {"stock": [], "orders": [], "purchase_orders": []}

def save_data(data):
    try:
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        return False

# Endpoints pour le stock
@app.route('/stock', methods=['GET'])
def get_stock():
    data = load_data()
    return jsonify({
        "success": True,
        "data": data.get("stock", []),
        "count": len(data.get("stock", []))
    })

@app.route('/stock/<sku>', methods=['GET'])
def get_stock_item(sku):
    data = load_data()
    stock_items = data.get("stock", [])
    
    for item in stock_items:
        if item["sku"] == sku:
            return jsonify({
                "success": True,
                "data": item
            })
    
    return jsonify({
        "success": False,
        "error": f"SKU {sku} not found"
    }), 404

@app.route('/stock/<sku>', methods=['PUT'])
def update_stock(sku):
    data = load_data()
    stock_items = data.get("stock", [])
    
    for item in stock_items:
        if item["sku"] == sku:
            request_data = request.get_json()
            
            if "available_qty" in request_data:
                item["available_qty"] = request_data["available_qty"]
            if "reserved_qty" in request_data:
                item["reserved_qty"] = request_data["reserved_qty"]
            if "location" in request_data:
                item["location"] = request_data["location"]
            
            item["updated_at"] = datetime.now().isoformat() + "Z"
            
            if save_data(data):
                return jsonify({
                    "success": True,
                    "data": item,
                    "message": f"Stock updated for SKU {sku}"
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Failed to save data"
                }), 500
    
    return jsonify({
        "success": False,
        "error": f"SKU {sku} not found"
    }), 404

# Endpoints pour les commandes d'achat
@app.route('/orders', methods=['GET'])
def get_orders():
    data = load_data()
    return jsonify({
        "success": True,
        "data": data.get("orders", []),
        "count": len(data.get("orders", []))
    })

@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    data = load_data()
    orders = data.get("orders", [])
    
    for order in orders:
        if order["id"] == order_id:
            return jsonify({
                "success": True,
                "data": order
            })
    
    return jsonify({
        "success": False,
        "error": f"Order {order_id} not found"
    }), 404

@app.route('/orders/<order_id>', methods=['PUT'])
def update_order(order_id):
    data = load_data()
    orders = data.get("orders", [])
    
    for order in orders:
        if order["id"] == order_id:
            request_data = request.get_json()
            
            if "status" in request_data:
                order["status"] = request_data["status"]
            if "eta" in request_data:
                order["eta"] = request_data["eta"]
            
            order["updated_at"] = datetime.now().isoformat() + "Z"
            
            if save_data(data):
                return jsonify({
                    "success": True,
                    "data": order,
                    "message": f"Order {order_id} updated"
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Failed to save data"
                }), 500
    
    return jsonify({
        "success": False,
        "error": f"Order {order_id} not found"
    }), 404

# Endpoints pour les bons de commande 
@app.route('/purchase-orders', methods=['GET'])
def get_purchase_orders():
    data = load_data()
    return jsonify({
        "success": True,
        "data": data.get("purchase_orders", []),
        "count": len(data.get("purchase_orders", []))
    })

@app.route('/purchase-orders/<po_id>', methods=['GET'])
def get_purchase_order(po_id):
    data = load_data()
    purchase_orders = data.get("purchase_orders", [])
    
    for po in purchase_orders:
        if po["id"] == po_id:
            return jsonify({
                "success": True,
                "data": po
            })
    
    return jsonify({
        "success": False,
        "error": f"Purchase order {po_id} not found"
    }), 404

@app.route('/purchase-orders', methods=['POST'])
def create_purchase_order():
    data = load_data()
    request_data = request.get_json()
    
    # Validation des données requises
    if not request_data or "sku" not in request_data or "quantity" not in request_data:
        return jsonify({
            "success": False,
            "error": "SKU and quantity are required"
        }), 400
    
    sku = request_data["sku"]
    quantity = request_data["quantity"]
    
    # Vérification que le SKU existe
    stock_items = data.get("stock", [])
    sku_exists = any(item["sku"] == sku for item in stock_items)
    
    if not sku_exists:
        return jsonify({
            "success": False,
            "error": f"SKU {sku} does not exist in stock"
        }), 400
    
    # Génération de l'ID du bon de commande
    po_id = f"PO{uuid.uuid4().hex[:6].upper()}"
    
    # Création du bon de commande
    new_po = {
        "id": po_id,
        "sku": sku,
        "quantity": quantity,
        "status": "Pending",
        "supplier_id": request_data.get("supplier_id", "SUPP001"),
        "unit_price": request_data.get("unit_price", 25.00),
        "total_amount": quantity * request_data.get("unit_price", 25.00),
        "created_at": datetime.now().isoformat() + "Z",
        "updated_at": datetime.now().isoformat() + "Z"
    }
    
    # Ajout à la liste des bons de commande
    if "purchase_orders" not in data:
        data["purchase_orders"] = []
    
    data["purchase_orders"].append(new_po)
    
    if save_data(data):
        return jsonify({
            "success": True,
            "data": new_po,
            "message": f"Purchase order {po_id} created successfully"
        }), 201
    else:
        return jsonify({
            "success": False,
            "error": "Failed to save data"
        }), 500

@app.route('/purchase-orders/<po_id>', methods=['PUT'])
def update_purchase_order(po_id):
    data = load_data()
    purchase_orders = data.get("purchase_orders", [])
    
    for po in purchase_orders:
        if po["id"] == po_id:
            request_data = request.get_json()
            
            if "status" in request_data:
                po["status"] = request_data["status"]
            if "quantity" in request_data:
                po["quantity"] = request_data["quantity"]
                po["total_amount"] = po["quantity"] * po["unit_price"]
            
            po["updated_at"] = datetime.now().isoformat() + "Z"
            
            if save_data(data):
                return jsonify({
                    "success": True,
                    "data": po,
                    "message": f"Purchase order {po_id} updated"
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Failed to save data"
                }), 500
    
    return jsonify({
        "success": False,
        "error": f"Purchase order {po_id} not found"
    }), 404

# Route racine
@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "success": True,
        "message": "Atracio ERP API",
        "version": "1.0",
        "endpoints": {
            "health_verification": "/Atracio",
            "stock": "/stock",
            "orders": "/orders", 
            "purchase_orders": "/purchase-orders"
        },
        "timestamp": datetime.now().isoformat() + "Z"
    })

# Endpoint de verification
@app.route('/Atracio', methods=['GET'])
def health_check():
    return jsonify({
        "success": True,
        "status": "Done",
        "timestamp": datetime.now().isoformat() + "Z"
    })

if __name__ == '__main__':
    logger.info("Starting ERP Server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
