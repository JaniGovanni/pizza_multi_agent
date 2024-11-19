from langchain_core.messages import AIMessage, HumanMessage
from pizza_multi_agent.build_graph.main_graph import build_main_graph
import asyncio
import uuid
from langgraph.checkpoint.memory import MemorySaver
from pizza_multi_agent.llm.open_ai_llm import OpenAILLM

thread_id = 1
memory = MemorySaver()
# process_order_llm=OpenAILLM
assistant = build_main_graph().compile(checkpointer=memory)
config = {
    "configurable": {  # The key needs to be here
        "thread_id": thread_id,  # These are the configurable values
        "user_id": "test"
    }
}

conversation = [
    AIMessage(content="Hello! You are speaking with Mario & Luigi Pizza. How can I help you today?"),
    
    HumanMessage(content="Hi, I'd like to order a pizza"),
    
    AIMessage(content="I'd be happy to help you with your order. Could you please tell me your full name first?"),
    
    HumanMessage(content="My name is John Smith"),
    
    # Main assistant delegates to process_order assistant
    AIMessage(content="Thank you, John Smith. I'll help you place your order. What kind of pizza would you like?"),
    
    HumanMessage(content="I'd like a large Margherita pizza with extra cheese"),
    
    AIMessage(content="Great choice! Would you like any sides or drinks with your order?"),
    
    HumanMessage(content="Yes, I'll take some garlic bread and a large Beer"),
    
    AIMessage(content="Perfect! Now I'll need your delivery address and phone number, please."),
    
    HumanMessage(content="My address is 123 Main Street, Apt 4B, Springfield, 12345. Phone is +1-555-123-4567"),
    
    AIMessage(content="Thank you! Let me confirm your order:\n\n"
              "Name: John Smith\n"
              "Phone: +1-555-123-4567\n"
              "Address: 123 Main Street, Apt 4B, Springfield, 12345\n"
              "Order:\n"
              "- 1 Large Margherita Pizza with Extra Cheese\n"
              "- 1 Garlic Bread\n"
              "- 1 Large Beer\n"
              "Special instructions: None\n\n"
              "Is this correct?"),
    
    HumanMessage(content="Yes, that's correct"),
]

state = assistant.invoke({"messages": conversation}, config)
print(state)