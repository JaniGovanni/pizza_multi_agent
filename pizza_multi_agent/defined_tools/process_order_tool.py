from langchain_core.tools import tool
from pizza_multi_agent.helper.extract_order import ExtractOrder
from pizza_multi_agent.helper.calculate_order_price import CalculateOrderPrice
from pizza_multi_agent.helper.save_order import SaveOrder
from app.menue import pizzeria_menu

@tool
def process_order(order: str):
    """
    Sends the order to the pizzeria

    Args:
        order: A string containing the verified order details, special instructions, address and phone number
    """
    order_dict = CalculateOrderPrice(ExtractOrder(order), pizzeria_menu)
    SaveOrder(order_dict)

    return order_dict