import json
import os
from datetime import datetime

def SaveOrder(order_data):
    orders_dir = os.getenv("ORDERS_DIR", "app/orders")
    os.makedirs(orders_dir, exist_ok=True)
    
    # Generate unique filename using timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"order_{timestamp}.json"
    filepath = os.path.join(orders_dir, filename)
    
    # Save the order data as JSON
    with open(filepath, 'w') as f:
        json.dump(order_data, f, indent=4)
    
    return filepath