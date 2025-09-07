from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import uuid
from datetime import datetime
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ERPServer")

app = Flask(__name__)
CORS(app)  # Permet les requêtes cross-origin depuis n8n

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

# Middleware pour logger toutes les requêtes
@app.before_request
def log_request():
    logger.info(f"Received {request.method} request to {request.path}")
    if request.is_json:
        logger.info(f"Request data: {request.get_json()}")

# Gestionnaire d'erreur global
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "message": f"The requested endpoint {request.path} does not exist"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error",
        "message": "An internal error occurred"
    }), 500

# Endpoints pour le stock
@app.route('/stock', methods=['GET'])
def get_stock():
    try:
        data = load_data()
        return jsonify({
            "success": True,
            "data": data.get("stock", []),
            "count": len(data.get("stock", [])),
            "timestamp": datetime.now().isoformat() + "Z"
        })
    except Exception as e:
        logger.error(f"Error in get_stock: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/stock/<sku>', methods=['GET'])
def get_stock_item(sku):
    try:
        data = load_data()
        stock_items = data.get("stock", [])
        
        for item in stock_items:
            if item.get("sku") == sku:
                return jsonify({
                    "success": True,
                    "data": item,
                    "timestamp": datetime.now().isoformat() + "Z"
                })
        
        return jsonify({
            "success": False,
            "error": f"SKU {sku} not found"
        }), 404
    except Exception as e:
        logger.error(f"Error in get_stock_item: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/stock/<sku>', methods=['PUT'])
def update_stock(sku):
    try:
        data = load_data()
        stock_items = data.get("stock", [])
        
        for item in stock_items:
            if item.get("sku") == sku:
                request_data = request.get_json() or {}
                
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
                        "message": f"Stock updated for SKU {sku}",
                        "timestamp": datetime.now().isoformat() + "Z"
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
    except Exception as e:
        logger.error(f"Error in update_stock: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Endpoints pour les commandes
@app.route('/orders', methods=['GET'])
def get_orders():
    try:
        data = load_data()
        return jsonify({
            "success": True,
            "data": data.get("orders", []),
            "count": len(data.get("orders", [])),
            "timestamp": datetime.now().isoformat() + "Z"
        })
    except Exception as e:
        logger.error(f"Error in get_orders: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    try:
        data = load_data()
        orders = data.get("orders", [])
        
        for order in orders:
            if order.get("id") == order_id:
                return jsonify({
                    "success": True,
                    "data": order,
                    "timestamp": datetime.now().isoformat() + "Z"
                })
        
        return jsonify({
            "success": False,
            "error": f"Order {order_id} not found"
        }), 404
    except Exception as e:
        logger.error(f"Error in get_order: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/orders/<order_id>', methods=['PUT'])
def update_order(order_id):
    try:
        data = load_data()
        orders = data.get("orders", [])
        
        for order in orders:
            if order.get("id") == order_id:
                request_data = request.get_json() or {}
                
                if "status" in request_data:
                    order["status"] = request_data["status"]
                if "eta" in request_data:
                    order["eta"] = request_data["eta"]
                
                order["updated_at"] = datetime.now().isoformat() + "Z"
                
                if save_data(data):
                    return jsonify({
                        "success": True,
                        "data": order,
                        "message": f"Order {order_id} updated",
                        "timestamp": datetime.now().isoformat() + "Z"
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
    except Exception as e:
        logger.error(f"Error in update_order: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Endpoints pour les bons de commande - CORRIGÉ L'URL
@app.route('/purchase-orders', methods=['GET'])
def get_purchase_orders():
    try:
        data = load_data()
        return jsonify({
            "success": True,
            "data": data.get("purchase_orders", []),
            "count": len(data.get("purchase_orders", [])),
            "timestamp": datetime.now().isoformat() + "Z"
        })
    except Exception as e:
        logger.error(f"Error in get_purchase_orders: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# AJOUT: Endpoint manquant pour purchase_orders
@app.route('/purchase_orders', methods=['GET'])
def get_purchase_orders_alt():
    """Alternative endpoint pour compatibility avec n8n"""
    return get_purchase_orders()

@app.route('/purchase-orders/<po_id>', methods=['GET'])
def get_purchase_order(po_id):
    try:
        data = load_data()
        purchase_orders = data.get("purchase_orders", [])
        
        for po in purchase_orders:
            if po.get("id") == po_id:
                return jsonify({
                    "success": True,
                    "data": po,
                    "timestamp": datetime.now().isoformat() + "Z"
                })
        
        return jsonify({
            "success": False,
            "error": f"Purchase order {po_id} not found"
        }), 404
    except Exception as e:
        logger.error(f"Error in get_purchase_order: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# AJOUT: Endpoint alternatif
@app.route('/purchase_orders/<po_id>', methods=['GET'])
def get_purchase_order_alt(po_id):
    """Alternative endpoint pour compatibility avec n8n"""
    return get_purchase_order(po_id)

@app.route('/purchase-orders', methods=['POST'])
def create_purchase_order():
    try:
        data = load_data()
        request_data = request.get_json() or {}
        
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
        sku_exists = any(item.get("sku") == sku for item in stock_items)
        
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
                "message": f"Purchase order {po_id} created successfully",
                "timestamp": datetime.now().isoformat() + "Z"
            }), 201
        else:
            return jsonify({
                "success": False,
                "error": "Failed to save data"
            }), 500
    except Exception as e:
        logger.error(f"Error in create_purchase_order: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/purchase-orders/<po_id>', methods=['PUT'])
def update_purchase_order(po_id):
    try:
        data = load_data()
        purchase_orders = data.get("purchase_orders", [])
        
        for po in purchase_orders:
            if po.get("id") == po_id:
                request_data = request.get_json() or {}
                
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
                        "message": f"Purchase order {po_id} updated",
                        "timestamp": datetime.now().isoformat() + "Z"
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
    except Exception as e:
        logger.error(f"Error in update_purchase_order: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Route racine
@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "success": True,
        "message": "Atracio ERP API",
        "version": "1.0",
        "endpoints": {
            "health_verification": "/health",
            "stock": "/stock",
            "orders": "/orders", 
            "purchase_orders": "/purchase-orders"
        },
        "timestamp": datetime.now().isoformat() + "Z"
    })

# Endpoint de verification - CORRIGÉ POUR N8N
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "success": True,
        "status": "Done",
        "message": "Atracio ERP API",
        "version": "1.0",
        "timestamp": datetime.now().isoformat() + "Z"
    })

# AJOUT: Endpoint alternatif pour health check
@app.route('/health_verification', methods=['GET'])
def health_verification():
    """Alternative endpoint name pour compatibility avec n8n"""
    return health_check()

if __name__ == '__main__':
    logger.info("Starting ERP Server...")
    app.run(debug=True, host='0.0.0.0', port=5000)