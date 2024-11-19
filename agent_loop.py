from langchain_core.messages import AIMessage, HumanMessage
from pizza_multi_agent.build_graph.main_graph import build_main_graph
import asyncio
import uuid
from langchain_core.messages import AIMessage, HumanMessage  
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from pizza_multi_agent.llm.open_ai_llm import OpenAILLM


async def run_conversation():
    # thread_id is used to access checkpoints
    #thread_id = str(uuid.uuid4())
    thread_id = 1

    # MemorySaver is not persitent, use PostgressSaver for that
    memory = MemorySaver()
    #memory = SqliteSaver.from_conn_string("pizza_chat_history.db")
    assistant = build_main_graph(process_order_llm=OpenAILLM).compile(checkpointer=memory)
    start_message = "Hello! You are speaking with Mario & Luigi Pizza. How can I help you today?"
    messages = [AIMessage(content=start_message)]
    print(f"Pizza Order Assistant: {start_message}")
    config = {
    "configurable": {
        # The passenger_id is used in our flight tools to
        # fetch the user's flight information
        "user_id": "test",
        # Checkpoints are accessed by thread_id
        "thread_id": thread_id,
    }}
    
    while True:
        # Get user input
        user_input = input("You: ")
            
        if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Pizza Order Assistant: Thank you for your time! Goodbye!")
                break
        messages.append(HumanMessage(content=user_input))
        async for event in assistant.astream_events({"messages": messages}, 
                                                    config, 
                                                    version="v1"):
            kind = event["event"]
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    # Empty content in the context of OpenAI means
                    # that the model is asking for a tool to be invoked.
                    # So we only print non-empty content
                    print(content, end="")
        print("")

if __name__ == "__main__":
    asyncio.run(run_conversation())