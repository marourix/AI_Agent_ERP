# ERP AI Agent

An intelligent agent for ERP (Enterprise Resource Planning) management that simulates a real business environment implemented by the OPENAI agent SDK  with a Flask API backend.

##  Features

- **AI Agent**: Conversational assistant for ERP management
- **Mock ERP Backend**: Flask server simulating a real ERP system
- **REST API**: Endpoints to manage stock, orders and purchase orders
- **Structured database**: JSON format organized like a real database

##  Prerequisites

- Python 3.8+
- Ollama with llama3.2 model
- Python dependencies (see requirements.txt)

##  Installation

1. **Clone the project**
```bash
git clone https://github.com/marourix/AI_Agent_ERP.git
cd AI_Agent_ERP
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Start Ollama with llama3.2**
```bash
ollama run llama3.2
```

##  Usage
### Manual startup

1. **Start the ERP server**
```bash
python erp_server.py
```

2. **In another terminal, start the agent**
```bash
python agent.py
```

##  Architecture

### File structure
```
AI_Agent/
├── agent.py              # Main AI agent
├── erp_server.py         # Flask server (mock ERP backend)
├── data.json             # Structured JSON database
├── requirements.txt      # Python dependencies
└── README.md            # Documentation
```

### API Endpoints

The Flask server exposes the following endpoints:

#### Stock
- `GET /stock` - Complete stock list
- `GET /stock/{sku}` - Details of a specific SKU
- `PUT /stock/{sku}` - Update stock

#### Orders
- `GET /orders` - List of orders
- `GET /orders/{id}` - Details of an order
- `PUT /orders/{id}` - Update an order

#### Purchase Orders
- `GET /purchase-orders` - List of purchase orders
- `GET /purchase-orders/{id}` - Details of a purchase order
- `POST /purchase-orders` - Create a purchase order
- `PUT /purchase-orders/{id}` - Update a purchase order

#### Health
- `GET /health` - Verify if the server is working or not

## Agent Features

The agent can perform the following actions:

1. **Check stock**: `check_stock_level(sku)`
2. **Create a purchase order**: `create_purchase_order(input_text)`
3. **Check order status**: `check_order_status(order_id)`
4. **List all stock**: `get_all_stock()`
5. **List all orders**: `get_all_orders()`
6. **List all purchase orders**: `get_all_purchase_orders()`

## Data Structure

### Database Format
Data is now organized in object arrays (database format):

```json
{
    "stock": [
        {
            "id": 1,
            "sku": "SKU123",
            "available_qty": 150,
            "reserved_qty": 20,
            "location": "Warehouse A",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
    ],
    "orders": [
        {
            "id": "ORD001",
            "customer_id": "CUST001",
            "status": "Shipped",
            "eta": "2025-08-01",
            "total_amount": 1250.00,
            "created_at": "2025-07-15T10:30:00Z",
            "updated_at": "2025-07-20T14:45:00Z"
        }
    ],
    "purchase_orders": [
        {
            "id": "POE115A9",
            "sku": "SKU456",
            "quantity": 50,
            "status": "Pending",
            "supplier_id": "SUPP001",
            "unit_price": 25.00,
            "total_amount": 1250.00,
            "created_at": "2025-08-10T20:26:13Z",
            "updated_at": "2025-08-10T20:26:13Z"
        }
    ]
}
```

##  Usage Examples

### Interacting with the agent
```
>> Check stock for SKU123
SKU123: 150 units available, 20 units reserved at Warehouse A.

>> Create a purchase order for SKU456 100 units
Purchase order POABC123 has been successfully created.
SKU: SKU456, Quantity: 100 units, Status: Pending, Total Amount: $2500.00.

>> Check status of order ORD001
Order ORD001 → Status: Shipped, Expected delivery: 2025-08-01, Total: $1250.00.

>> List all stock
Available stock:
SKU123: 150 available at Warehouse A
SKU456: 75 available at Warehouse B
SKU789: 200 available at Warehouse A
And so on...
```

## Configuration

### Environment variables
- `ERP_API_BASE_URL`: ERP server URL (default: http://localhost:5000)

### AI Model
- Model used: llama3.2 via Ollama
- URL: http://localhost:11434/v1

## Troubleshooting

### Common issues

1. **ERP server not accessible**
   - Check that the Flask server is started
   - Check that port 5000 is not used by another service

2. **Ollama not accessible**
   - Check that Ollama is installed and running
   - Check that the llama3.2 model is downloaded

3. **Dependency errors**
   - Reinstall dependencies: `pip install -r requirements.txt`


## Objectives Achieved

 **Flask mock backend**: Complete ERP server with REST endpoints  
 **Database format**: JSON structure organized in object arrays  
 **Modular architecture**: Clear separation between agent and backend  
 **REST API**: Standard endpoints for all operations  
 **Error handling**: Validation and robust error management

 ![localhost/purchase_orders](images/Capture%20d'écran%202025-08-16%20230534.png)
 ![localhost/stock](images/Capture%20d'écran%202025-08-16%20230607.png)
