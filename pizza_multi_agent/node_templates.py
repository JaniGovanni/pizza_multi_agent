from langchain_core.messages import ToolMessage
from typing import Callable
from langchain_core.messages import ToolMessage
from pizza_multi_agent.state import State

# is a wrapper for regular python functions, to be used as
# langchain components
# https://python.langchain.com/api_reference/core/runnables/langchain_core.runnables.base.RunnableLambda.html#langchain_core.runnables.base.RunnableLambda
from langchain_core.runnables import RunnableLambda

from langgraph.prebuilt import ToolNode


def create_tool_node_with_fallback(tools: list) -> dict:

    def handle_tool_error(state: State) -> dict:
        error = state.get("error")
        tool_calls = state["messages"][-1].tool_calls
        return {
            "messages": [
                ToolMessage(
                    content=f"Error: {repr(error)}\n please fix your mistakes.",
                    tool_call_id=tc["id"],
                )
                for tc in tool_calls
            ]
        }
    
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )


def create_entry_node(assistant_name: str, new_dialog_state: str) -> Callable:
    def entry_node(state: State) -> dict:
        tool_call_id = state["messages"][-1].tool_calls[0]["id"]
        return {
            "messages": [
                ToolMessage(
                    content=f"The assistant is now the {assistant_name} assistant. Reflect on the above conversation between the main_assistant and the user."
                    f" The user's intent is unsatisfied. Do whatever is needed to assist the user. Remember, you are {assistant_name} assistant,"
                    " If the user changes their mind or needs help for other tasks, call the back_to_main_assistant function to let the main_assistant take control."
                    " Do not mention who you are - just act as the proxy for the assistant.",
                    tool_call_id=tool_call_id,
                )
            ],
            "dialog_state": new_dialog_state,
        }
    return entry_node
