from pizza_multi_agent.system_prompts.main_assistant_prompt import MainAssistantPrompt
from pizza_multi_agent.llm.groq_llm import GroqLLM
from pizza_multi_agent.defined_tools.delegate_to_process_order_tool import to_process_order

tools = [to_process_order]

# currently there is only one sub-agent, but this can easily be extended in the future
MainAssistant = MainAssistantPrompt | GroqLLM.bind_tools(tools)

def build_main_assistant(llm = GroqLLM):
    return MainAssistantPrompt | llm.bind_tools(tools)