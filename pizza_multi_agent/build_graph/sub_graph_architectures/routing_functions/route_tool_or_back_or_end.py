from langgraph.graph import END
from langgraph.prebuilt import tools_condition
from pizza_multi_agent.state import State
from pizza_multi_agent.defined_tools.back_to_main_assistant_tool import back_to_main_assistant

def RouteToolOrBackOrEnd(state:State):
    route = tools_condition(state)
    if route == END:
        return END
    tool_calls = state["messages"][-1].tool_calls
    did_cancel = any(tc["name"] == back_to_main_assistant.__name__ for tc in tool_calls)

    if did_cancel:
        return "leave_skill"
    # NOTE: this only returns a string "tools", so there is no information about the specific tool that was called
    else:
        return route