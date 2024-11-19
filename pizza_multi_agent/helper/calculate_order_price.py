from typing import Dict
from pizza_multi_agent.helper.calculation_and_validation.validation.json_data import validate_json_data
from pizza_multi_agent.helper.calculation_and_validation.process_items.pizza import process_pizza_order
from pizza_multi_agent.helper.calculation_and_validation.process_items.sides import process_side_order
from pizza_multi_agent.helper.calculation_and_validation.process_items.drinks import process_drink_order
from pizza_multi_agent.helper.save_order import SaveOrder

def CalculateOrderPrice(json_data: Dict, menu: Dict) -> Dict | str:
    try:
        validate_json_data(json_data)
        
        # Process pizzas
        total = 0
        for pizza in json_data.get("order_items", []):
            pizza_result = process_pizza_order(pizza, menu)
            total += pizza_result["total"]
        
        # Process sides
        for side in json_data.get("side", []):
            side_result = process_side_order(side, menu)
            total += side_result["price"]
        
        # Process drinks
        for drink in json_data.get("drink", []):
            drink_result = process_drink_order(drink, menu)
            total += drink_result["price"]
        
        # Update the total price in the original JSON
        json_data["total_price"] = round(total, 2)
        return json_data
        
    except ValueError as e:
        return str(e)