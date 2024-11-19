import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from typing import Dict, Any
from langchain_core.output_parsers import JsonOutputParser


# TODO: add something to check, if name, address and phone number are in the input_text
def ExtractOrder(input_text: str) -> Dict[str, Any]:
    """
    Extracts order details from the input_text and formats them into JSON.
    
    Args:
        input_text: A string containing the order details, special instructions, address and phone number
        
    Returns:
        Dict containing the structured order information
    """
    llm = ChatGroq(model="llama-3.1-70b-versatile")
    
    extraction_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a specialized order extraction assistant. 
         Your task is to extract order details from a string and format them into a structured JSON format.

        Rules:
        - Extract only factual information mentioned in the input
        - Format must match the specified JSON structure exactly
        - Leave the total_price as 0.00 (it will be calculated separately)
        - Include all mentioned special instructions
        - ONLY output the JSON structure, nothing else!
        
        Output Format:
        {{
          "customer": {{
            "name": "Customer Name",
            "phone": "Customer Phone Number",
            "address": "Customer Address"
          }},
          "order_items": [
            {{
              "pizza_name": "Pizza Name",
              "size": "Size",
              "toppings": ["Topping 1", "Topping 2"]
            }}
          ],
          "side": ["Side 1", "Side 2"],
          "drink": ["Drink 1", "Drink 2"],
          "total_price": 0.00,
          "special_instructions": "Any special instructions"
        }}

        Examples:

        Input:
        Name: Sarah Johnson
        Phone: +1-555-0123
        Address: 789 Oak Lane, Apt 12, Cityville, 54321
        Order:
        - 1 Large Margherita Pizza with Extra Cheese, Mushrooms
        - 1 Garlic Bread
        - 1 Large Soda
        Special instructions: Ring doorbell twice when arriving

        Output:
        {{
          "customer": {{
            "name": "Sarah Johnson",
            "phone": "+1-555-0123",
            "address": "789 Oak Lane, Apt 12, Cityville, 54321"
          }},
          "order_items": [
            {{
              "pizza_name": "Margherita",
              "size": "Large",
              "toppings": ["Extra Cheese", "Mushrooms"]
            }}
          ],
          "side": ["Garlic Bread"],
          "drink": ["Large Soda"],
          "total_price": 0.00,
          "special_instructions": "Ring doorbell twice when arriving"
        }}

        Input:
        Name: Tom Smith
        Phone: +1-444-555-6789
        Address: 123 Pine Street, Springfield, 67890
        Order:
        - 1 Medium Pepperoni Pizza with Olives
        - 1 Small Vegetarian Pizza
        - 1 French Fries
        - 2 Bottle Water
        Special instructions: Leave at door

        Output:
        {{
          "customer": {{
            "name": "Tom Smith",
            "phone": "+1-444-555-6789",
            "address": "123 Pine Street, Springfield, 67890"
          }},
          "order_items": [
            {{
              "pizza_name": "Pepperoni",
              "size": "Medium",
              "toppings": ["Olives"]
            }},
            {{
              "pizza_name": "Vegetarian",
              "size": "Small",
              "toppings": []
            }}
          ],
          "side": ["French Fries"],
          "drink": ["Bottle Water", "Bottle Water"],
          "total_price": 0.00,
          "special_instructions": "Leave at door"
        }}
         """),
        ("human", "{input}"),
    ])
    
    json_parser = JsonOutputParser()
    chain = extraction_prompt | llm | json_parser
    
    # Get parsed result
    order_dict = chain.invoke({"input": input_text})
            
    return order_dict