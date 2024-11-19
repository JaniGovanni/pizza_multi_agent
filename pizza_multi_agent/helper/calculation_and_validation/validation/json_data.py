from typing import Dict

def validate_json_data(json_data: Dict) -> None:
    if "order_items" not in json_data:
        raise ValueError("ERROR: Invalid JSON data format: missing required 'order_items' key")