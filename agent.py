import json
import logging
import warnings
import re
import asyncio
import requests
from agents import function_tool
from typing import Optional
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents import set_tracing_disabled
import uuid
from datetime import datetime

# Configuration du logging
logging.getLogger("httpx").setLevel(logging.WARNING)
set_tracing_disabled(True)
warnings.filterwarnings("ignore", category=DeprecationWarning)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AtracioAgent")

# Configuration de l'API ERP
ERP_API_BASE_URL = "http://localhost:5000"

def make_api_request(endpoint: str, method: str = "GET", data: dict = None):
    """Fonction utilitaire pour faire des requêtes à l'API ERP"""
    try:
        url = f"{ERP_API_BASE_URL}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        else:
            return {"success": False, "error": f"Unsupported method: {method}"}
        
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            return {"success": False, "error": f"API Error: {response.status_code} - {response.text}"}
    
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Cannot connect to ERP server. Make sure it's running on http://localhost:5000"}
    except Exception as e:
        return {"success": False, "error": f"Request failed: {str(e)}"}

@function_tool
def check_stock_level(sku: str) -> str:
    sku = sku.strip().replace('"', '').replace("'", "")
    if sku.startswith("sku="):
        sku = sku[4:]
    
    result = make_api_request(f"/stock/{sku}")
    
    if result.get("success"):
        item = result["data"]
        return f"{sku}: {item['available_qty']} units available, {item['reserved_qty']} units reserved at {item['location']}."
    else:
        return f"Error: {result.get('error', 'Unknown error')}"

@function_tool
def create_purchase_order(input_text: str):
    input_text = input_text.strip().replace('"', '').replace("'", "")
    sku_match = re.search(r'(SKU\d+)', input_text, re.IGNORECASE)
    quantity_match = re.search(r'\b(?!\d+$)(\d+)\b', input_text)
    
    if not (sku_match and quantity_match):
        return "Please provide both a valid SKU and a quantity (e.g., 'Create a purchase order for SKU123 50')."
    
    sku = sku_match.group(1).upper()
    quantity = int(quantity_match.group(1))
    
    # Création du bon de commande via l'API
    order_data = {
        "sku": sku,
        "quantity": quantity
    }
    
    result = make_api_request("/purchase-orders", method="POST", data=order_data)
    
    if result.get("success"):
        po_data = result["data"]
        return (
            f"Purchase order {po_data['id']} has been successfully created.\n"
            f"SKU: {po_data['sku']}, Quantity: {po_data['quantity']} units, "
            f"Status: {po_data['status']}, Total Amount: ${po_data['total_amount']:.2f}."
        )
    else:
        return f"Error creating purchase order: {result.get('error', 'Unknown error')}"

@function_tool
def check_order_status(order_id: str) -> str:
    order_id = order_id.strip().replace('"', '').replace("'", "")
    if order_id.startswith("order_id="):
        order_id = order_id[9:]
    
    result = make_api_request(f"/orders/{order_id}")
    
    if result.get("success"):
        order = result["data"]
        return f"Order {order_id} → Status: {order['status']}, Expected delivery: {order['eta']}, Total: ${order['total_amount']:.2f}."
    else:
        return f"Error: {result.get('error', 'Unknown error')}"

@function_tool
def get_all_stock() -> str:
    result = make_api_request("/stock")
    
    if result.get("success"):
        stock_items = result["data"]
        if not stock_items:
            return "No stock items available."
        
        stock_list = []
        for item in stock_items:
            stock_list.append(f"{item['sku']}: {item['available_qty']} available at {item['location']}")
        
        return "Available stock:\n" + "\n".join(stock_list)
    else:
        return f"Error retrieving stock: {result.get('error', 'Unknown error')}"

@function_tool
def get_all_orders() -> str:
    result = make_api_request("/orders")
    
    if result.get("success"):
        orders = result["data"]
        if not orders:
            return "No orders found."
        
        order_list = []
        for order in orders:
            order_list.append(f"{order['id']}: {order['status']} - ETA: {order['eta']}")
        
        return "All orders:\n" + "\n".join(order_list)
    else:
        return f"Error retrieving orders: {result.get('error', 'Unknown error')}"

@function_tool
def get_all_purchase_orders() -> str:
    result = make_api_request("/purchase-orders")
    
    if result.get("success"):
        purchase_orders = result["data"]
        if not purchase_orders:
            return "No purchase orders found."
        
        po_list = []
        for po in purchase_orders:
            po_list.append(f"{po['id']}: {po['sku']} - {po['quantity']} units - {po['status']}")
        
        return "All purchase orders:\n" + "\n".join(po_list)
    else:
        return f"Error retrieving purchase orders: {result.get('error', 'Unknown error')}"

model = OpenAIChatCompletionsModel(
    model="llama3.2",
    openai_client=AsyncOpenAI(
        base_url="http://localhost:11434/v1",
        api_key="nokeyneeded"
    )
)

AGENT_INSTRUCTIONS = """
You are Atracio's ERP assistant. 
You must answer business-related questions using ONLY the provided tools.
When creating a purchase order, ALWAYS call the `create_purchase_order` tool and return ONLY the tool's result to the user in natural language.

TOOLS:
1. check_stock_level(sku: str) - Check stock level for a specific SKU
2. create_purchase_order(input_text: str) - Create a purchase order (provide SKU and quantity in text)
3. check_order_status(order_id: str) - Check the status of a specific order
4. get_all_stock() - Get a list of all available stock items
5. get_all_orders() - Get a list of all orders
6. get_all_purchase_orders() - Get a list of all purchase orders

RULES:
- Always use the tools to answer questions.
- Do NOT invent data, only use the data from the ERP API.
- Be concise and professional.
- When asked about stock, orders, or purchase orders, use the appropriate tool to get real-time data.
"""

agent = Agent(
    name="Atracio Assistant",
    instructions=AGENT_INSTRUCTIONS,
    tools=[check_stock_level, create_purchase_order, check_order_status, 
           get_all_stock, get_all_orders, get_all_purchase_orders],
    model=model
)

async def stream_response(user_input: str):
    try:
        result = Runner.run_streamed(agent, user_input)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and hasattr(event.data, 'delta'):
                content = event.data.delta
                if content.strip() and not content.startswith("{"):
                    print(content, end="", flush=True)
        print()
    except Exception as e:
        logger.error(f" Error: {str(e)}")

async def main():
    print("Atracio Assistant — Type 'exit' to quit")
    print("Connected to ERP API at:", ERP_API_BASE_URL)
    print()
    
    # Test de connexion à l'API 
    health_check = make_api_request("/Atracio")
    if health_check.get("success"):
        print("ERP Server is running perfectly")
    else:
        print("Warning: Cannot connect to ERP Server. Make sure to start it with: python erp_server.py")
    print()

    while True:
        user_input = input(">> ").strip()
        if not user_input:
            continue
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break
        await stream_response(user_input)

if __name__ == "__main__":
    asyncio.run(main())