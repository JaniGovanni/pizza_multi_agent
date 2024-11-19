from pizza_multi_agent.system_prompts.process_order_prompt import build_process_order_system_prompt
from pizza_multi_agent.llm.groq_llm import GroqLLM
from pizza_multi_agent.defined_tools.back_to_main_assistant_tool import back_to_main_assistant
from pizza_multi_agent.defined_tools.process_order_tool import process_order
from app.menue import pizzeria_menu

# TODO: make a class out of this

ProcessOrderPrompt = build_process_order_system_prompt(pizzeria_menu)
ProcessOrderTools = [back_to_main_assistant, process_order]

ProcessOrderAssistant = ProcessOrderPrompt | GroqLLM.bind_tools(ProcessOrderTools)

def build_process_order_assistant(llm = GroqLLM):
    return ProcessOrderPrompt | llm.bind_tools(ProcessOrderTools)