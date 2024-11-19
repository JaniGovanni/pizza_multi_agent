from typing import Dict
from pizza_multi_agent.helper.calculation_and_validation.process_items.toppings import process_toppings

def process_pizza_order(pizza: Dict, menu: Dict) -> Dict:
    # Validate pizza order structure
    if not isinstance(pizza, dict) or "pizza_name" not in pizza or "size" not in pizza:
        raise ValueError("ERROR: Invalid pizza order format: must contain 'pizza_name' and 'size'")
        
    pizza_name = pizza["pizza_name"]
    size_input = pizza["size"].lower()
    toppings = pizza.get("toppings", [])
    
    # Find pizza in menu
    pizza_item = next((p for p in menu["pizzas"] if p["name"] == pizza_name), None)
    if not pizza_item:
        raise ValueError(f"ERROR: Pizza '{pizza_name}' not found in menu")
        
    # Validate size
    matched_size = next((menu_size for menu_size in pizza_item["sizes"].keys() 
                       if menu_size.lower() in size_input or size_input in menu_size.lower()), None)
    if not matched_size:
        raise ValueError(f"ERROR: Size '{pizza['size']}' not available for pizza '{pizza_name}'")
        
    base_price = pizza_item["sizes"][matched_size]
    
    # Calculate toppings
    toppings_details = process_toppings(toppings, menu)
    toppings_price = sum(topping["price"] for topping in toppings_details)
    
    pizza_total = round(base_price + toppings_price, 2)
    
    return {
        "item": f"{matched_size} {pizza_name}",
        "base_price": base_price,
        "toppings": toppings_details,
        "total": pizza_total
    }