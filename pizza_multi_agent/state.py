from typing import Annotated, Literal, Optional

from typing_extensions import TypedDict

from langgraph.graph.message import AnyMessage, add_messages


def update_dialog_stack(left: list[str], right: Optional[str]) -> list[str]:
    """Push or pop the state."""
    if right is None:
        return left
    # leads to state [main_assistant]
    if right == "pop":
        return left[:-1]
    # leads to state [main_assistant, process_order] for example
    return left + [right]


# could be easily extended to include more agents

sub_agents = ["process_order"]

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    user_info: str
    dialog_state: Annotated[
        list[
            Literal[
                "main_assistant",  # supervisor, leads to different subagents
                "process_order",  # gets all informations about the users order and process it
            ]
        ],
        update_dialog_stack,
    ]