from typing import Dict

def process_drink_order(drink_input: str, menu: Dict) -> Dict:
    drink_input = drink_input.lower()
    
    for menu_drink in menu["drinks"]:
        drink_name = menu_drink["name"]
        
        if drink_name.lower() in drink_input:
            matched_size = next((menu_size for menu_size in menu_drink["sizes"].keys()
                               if menu_size.lower() in drink_input or 
                               any(size_word in drink_input for size_word in menu_size.lower().split())), None)
            
            if matched_size:
                return {
                    "item": drink_input,
                    "price": menu_drink["sizes"][matched_size]
                }
                
            available_sizes = list(menu_drink["sizes"].keys())
            raise ValueError(f"ERROR: Invalid size for drink '{drink_input}'. Available sizes: {', '.join(available_sizes)}")
            
    raise ValueError(f"ERROR: Drink '{drink_input}' not found in menu")