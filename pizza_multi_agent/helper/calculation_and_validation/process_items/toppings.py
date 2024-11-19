from typing import Dict

def process_toppings(toppings: list, menu: Dict) -> list:
    topping_details = []
    for topping in toppings:
        topping_item = next((t for t in menu["toppings"] if t["name"] == topping), None)
        if not topping_item:
            raise ValueError(f"ERROR: Topping '{topping}' not found in menu")
        topping_details.append({"name": topping, "price": topping_item["price"]})
    return topping_details