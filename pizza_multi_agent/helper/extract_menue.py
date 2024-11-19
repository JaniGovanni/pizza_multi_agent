def ExtractMenue(menu: dict) -> tuple[str, str, str, str]:
    """
    Build formatted menu strings for pizzas, toppings, sides, and drinks.
    
    Args:
        menu (dict): The complete menu dictionary
        
    Returns:
        tuple: (available_pizzas, available_toppings, available_sides, available_drinks)
    """
    pizza_details = []
    for pizza in menu["pizzas"]:
        sizes_info = [f"{size}: ${price}" for size, price in pizza["sizes"].items()]
        ingredients_info = ", ".join(pizza["ingredients"])
        pizza_details.append(f"{pizza['name']} ({', '.join(sizes_info)})\n  Ingredients: {ingredients_info}")
    available_pizzas = "\n- ".join(pizza_details)
    
    # Build toppings string
    available_toppings = ", ".join([f"{topping['name']} (${topping['price']})" for topping in menu["toppings"]])
    
    # Build sides string
    sides_details = [f"{side['name']} (${side['price']})" for side in menu["sides"]]
    available_sides = "\n- ".join(sides_details)
    
    # Build drinks string
    drinks_details = []
    for drink in menu["drinks"]:
        sizes_info = [f"{size}: ${price}" for size, price in drink["sizes"].items()]
        drinks_details.append(f"{drink['name']} ({', '.join(sizes_info)})")
    available_drinks = "\n- ".join(drinks_details)
    
    return available_pizzas, available_toppings, available_sides, available_drinks