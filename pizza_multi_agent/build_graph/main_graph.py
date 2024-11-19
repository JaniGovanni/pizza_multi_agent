from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langgraph.prebuilt import tools_condition
from pizza_multi_agent.state import State, sub_agents
from langgraph.graph import END, StateGraph, START
from pizza_multi_agent.node_templates import create_entry_node
from pizza_multi_agent.assistant_template import AssistantTemplate
from pizza_multi_agent.sub_agents.main_assistant import MainAssistant, build_main_assistant
from pizza_multi_agent.sub_agents.process_order_assistant import ProcessOrderAssistant, ProcessOrderTools, build_process_order_assistant
from pizza_multi_agent.build_graph.main_routing_functions import BackToMain, route_primary_assistant, route_to_workflow
from pizza_multi_agent.build_graph.sub_graph_architectures.sub_graph_type_1 import build_sub_graph_type_1
from pizza_multi_agent.llm.groq_llm import GroqLLM


def build_main_graph(process_order_llm=GroqLLM):
    builder = StateGraph(State)

    builder.add_node("main_assistant", AssistantTemplate(MainAssistant))

    # add a sub_graph
    builder = build_sub_graph_type_1(builder, 
                                    "process_order", 
                                    build_process_order_assistant(process_order_llm), 
                                    ProcessOrderTools)

    # route to sub_graph

    # return from sub_graph to main_assistant
    builder.add_node("leave_skill", BackToMain)
    builder.add_edge("leave_skill", "main_assistant")

    # route to sub_graph
    sub_agents_entry_nodes = [f"enter_{sub_agent}" for sub_agent in sub_agents]
    builder.add_conditional_edges("main_assistant", 
                                route_primary_assistant,
                                sub_agents_entry_nodes + [END])

    # route at entry node
    builder.add_conditional_edges(START,
                                route_to_workflow,
                                sub_agents + ["main_assistant"])
    return builder



