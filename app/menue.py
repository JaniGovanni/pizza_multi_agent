import json

# This is the menu of the pizzeria. It is a dictionary that contains the pizzas, the toppings, the sides and the drinks.

pizzeria_menu = {
    "pizzas": [
        {
            "name": "Margherita",
            "ingredients": ["tomato sauce", "mozzarella", "basil"],
            "sizes": {
                "Small": 8.99,
                "Medium": 10.99,
                "Large": 12.99
            }
        },
        {
            "name": "Pepperoni",
            "ingredients": ["tomato sauce", "mozzarella", "pepperoni"],
            "sizes": {
                "Small": 10.99,
                "Medium": 12.99,
                "Large": 14.99
            }
        },
        {
            "name": "Vegetarian",
            "ingredients": ["tomato sauce", "mozzarella", "bell peppers", "mushrooms", "onions"],
            "sizes": {
                "Small": 9.99,
                "Medium": 11.99,
                "Large": 13.99
            }
        },
        {
            "name": "BBQ Chicken",
            "ingredients": ["bbq sauce", "mozzarella", "chicken", "red onions", "cilantro"],
            "sizes": {
                "Small": 12.99,
                "Medium": 14.99,
                "Large": 16.99
            }
        },
        {
            "name": "Four Cheese",
            "ingredients": ["tomato sauce", "mozzarella", "parmesan", "gorgonzola", "goat cheese"],
            "sizes": {
                "Small": 13.99,
                "Medium": 15.99,
                "Large": 17.99
            }
        },
        {
            "name": "Spicy Italian",
            "ingredients": ["tomato sauce", "mozzarella", "spicy salami", "red chili peppers", "oregano"],
            "sizes": {
                "Small": 12.49,
                "Medium": 14.49,
                "Large": 16.49
            }
        }
    ],
    "toppings": [
        {
            "name": "Extra Cheese",
            "price": 1.50
        },
        {
            "name": "Mushrooms",
            "price": 1.00
        },
        {
            "name": "Pepperoni",
            "price": 1.50
        },
        {
            "name": "Olives",
            "price": 1.00
        },
        {
            "name": "Onions",
            "price": 0.75
        },
        {
            "name": "Bacon",
            "price": 1.75
        },
        {
            "name": "Green Peppers",
            "price": 1.00
        },
        {
            "name": "Pineapple",
            "price": 1.25
        }
    ],
    "sides": [
        {
            "name": "Garlic Bread",
            "price": 4.99
        },
        {
            "name": "Caesar Salad",
            "price": 6.99
        },
        {
            "name": "Mozzarella Sticks",
            "price": 5.99
        },
        {
            "name": "French Fries",
            "price": 3.99
        },
        {
            "name": "Onion Rings",
            "price": 4.49
        }
    ],
    "drinks": [
        {
            "name": "Soda",
            "sizes": {"small": 1.99, "medium": 2.49, "large": 2.99}
        },
        {
            "name": "Beer",
            "sizes": {"bottle": 4.99, "pint": 5.99}
        },
        {
            "name": "Water",
            "sizes": {"bottle": 1.49, "large": 2.49}
        },
        {
            "name": "Wine",
            "sizes": {"glass": 6.99, "bottle": 19.99}
        },
        {
            "name": "Juice",
            "sizes": {"small": 2.49, "large": 3.49}
        }
    ]
}

menu_json = json.dumps(pizzeria_menu, indent=4)
print(menu_json)