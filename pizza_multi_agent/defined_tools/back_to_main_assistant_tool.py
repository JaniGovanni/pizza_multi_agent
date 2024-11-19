from pydantic import BaseModel


class back_to_main_assistant(BaseModel):
    """
    A tool to escalate control of the dialog to the main_assistant. Use this tool when the customer's wants to cancel the order.

    """
