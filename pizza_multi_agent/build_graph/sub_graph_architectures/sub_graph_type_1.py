from langgraph.graph import StateGraph
from langgraph.graph import END
from typing import Callable, List
from langchain_core.tools import Tool
from pizza_multi_agent.node_templates import create_entry_node, create_tool_node_with_fallback
from pizza_multi_agent.assistant_template import AssistantTemplate
from pizza_multi_agent.defined_tools.back_to_main_assistant_tool import back_to_main_assistant
from pizza_multi_agent.build_graph.sub_graph_architectures.routing_functions.route_tool_or_back_or_end import RouteToolOrBackOrEnd


def build_sub_graph_type_1(graph: StateGraph,
                           sub_graph_name: str,
                           agent_runnable: Callable,
                           agent_tools: List[Tool]) -> StateGraph:
    entry_node_name = "enter_" + sub_graph_name
    # create entry node for sub_graph
    graph.add_node(entry_node_name, 
                   create_entry_node(sub_graph_name, sub_graph_name))
    # create sub_agent node
    graph.add_node(sub_graph_name, AssistantTemplate(agent_runnable))

    # create tool nodes for sub_agent
    graph.add_node(sub_graph_name + "_tools", 
                   create_tool_node_with_fallback([tool for tool in agent_tools if tool != back_to_main_assistant.__name__]))
    graph.add_conditional_edges(sub_graph_name, 
                                RouteToolOrBackOrEnd,
                                {END: END, 
                                 "tools": sub_graph_name + "_tools", 
                                 "leave_skill": "leave_skill"})
    # tools back to subagent
    graph.add_edge(sub_graph_name + "_tools", sub_graph_name)
    # entry node to sub_agent
    graph.add_edge(entry_node_name, sub_graph_name)
    return graph
    
    
    



    