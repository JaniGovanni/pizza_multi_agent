from pizza_multi_agent.state import State, sub_agents
from langchain_core.messages import ToolMessage
from langgraph.graph import END
from langgraph.prebuilt import tools_condition

def BackToMain(state: State) -> dict:
    """Pop the dialog stack and return to the main_assistant.

    This lets the full graph explicitly track the dialog flow and delegate control
    to specific sub-graphs.
    """
    messages = []
    if state["messages"][-1].tool_calls:
        # Note: Doesn't currently handle the edge case where the llm performs parallel tool calls
        messages.append(
            ToolMessage(
                content="Resuming dialog with the main_assistant. Please reflect on the past conversation and assist the user further as needed.",
                tool_call_id=state["messages"][-1].tool_calls[0]["id"],
            )
        )
    return {
        "dialog_state": "pop",
        "messages": messages,
    }

def route_primary_assistant(
    state: State,
):
    routes = sub_agents
    route = tools_condition(state)
    if route == END:
        return END
    tool_calls = state["messages"][-1].tool_calls
    if tool_calls:
        tool_name = tool_calls[0]["name"]
        # Check if the tool name matches "to_" + any route
        for route_name in routes:
            if tool_name.lower() == f"to_{route_name}":
                return f"enter_{route_name}"
    raise ValueError("Invalid route")


def route_to_workflow(state: State):
    """If we are in a delegated state, route directly to the appropriate assistant."""
    dialog_state = state.get("dialog_state")
    if not dialog_state:
        return "main_assistant"
    return dialog_state[-1]