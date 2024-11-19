from pydantic import BaseModel


class to_process_order(BaseModel):
    """
    A tool, to delegate the work to the process_order_assistant. Use this tool when the customer wants to order something.

    Args:
        name: The name of the customer.
    """

    customer_name: str

    class Config:
        json_schema_extra = {
            "example": {
                "customer_name": "John Wick",
            },
        }