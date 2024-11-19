import pandas as pd
import streamlit as st
import json
import os

# NOT RELEVANT FOR THE CHALLENGE (this is only the order page ui)

def load_orders(directory):
    orders = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as f:
                order = json.load(f)
                orders.append(order)
    return orders

def flatten_order(order):
    flat_order = {
        "Name": order.get("customer", {}).get("name", "N/A"),
        "Phone": order.get("customer", {}).get("phone", "N/A"),
        "Address": order.get("customer", {}).get("adress", "N/A"),
        "Price": order.get("total_price", "N/A"),
        "Instructions": order.get("special_instructions", "N/A"),
        "Pizzas": [],
        "Pizza Sizes": [],
        "Pizza Toppings": [],
        "Side": [],
        "Drink": []
    }
    
    for item in order.get("order_items", []):
        flat_order["Pizzas"].append(item.get("pizza_name", "N/A"))
        flat_order["Pizza Sizes"].append(item.get("size", "N/A"))
        flat_order["Pizza Toppings"].append(", ".join(item.get("toppings", [])))
    
    for item in order.get("side", []):
        flat_order["Side"].append(item)
    
    for item in order.get("drink", []):
        flat_order["Drink"].append(item)
    
    return flat_order

def show_orders_page():
    st.title("Pizzeria Orders")

    orders_directory = "app/orders"
    orders = load_orders(orders_directory)

    if not orders:
        st.write("No orders found.")
    else:
        # Flatten each order and create a DataFrame
        flattened_orders = [flatten_order(order) for order in orders]
        df = pd.DataFrame(flattened_orders)
        
        # Display the DataFrame
        st.dataframe(df)