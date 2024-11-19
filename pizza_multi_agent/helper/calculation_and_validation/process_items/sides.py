from typing import Dict

def process_side_order(side: str, menu: Dict) -> Dict:
    side_item = next((s for s in menu["sides"] if s["name"] == side), None)
    if not side_item:
        raise ValueError(f"ERROR: Side item '{side}' not found in menu")
    return {
        "item": side,
        "price": side_item["price"]
    }