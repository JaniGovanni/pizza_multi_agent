
# Third party imports
import streamlit as st
from pizza_multi_agent.llm.open_ai_llm import OpenAILLM

# Local imports
from app.menue import pizzeria_menu
from app.oders_view import show_orders_page
from pizza_multi_agent.build_graph.main_graph import build_main_graph
from langchain_core.messages import HumanMessage, AIMessage
import asyncio
import uuid
from langgraph.checkpoint.memory import MemorySaver

st.set_page_config(page_title="Pizza Challenge", layout="wide")

async def main_page():
    
    # Set the title of the Streamlit app
    st.title("Jupus Pizza Challenge")


    # Check if the messages list is in the session state; if not, initialize it with a welcome message
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! You are speaking with Mario & Luigi Pizza. How can I help you today?",
            }
        ]
    if "pizza_agent" not in st.session_state:
        st.session_state.pizza_agent = build_main_graph(process_order_llm=OpenAILLM).compile(checkpointer=MemorySaver())
    if "config" not in st.session_state:
        thread_id = str(uuid.uuid4())
        st.session_state.config = {"configurable": {
            "thread_id": thread_id,
        }}

    # Display each message in the chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Capture user input from the chat input box 
    if prompt := st.chat_input("What do you wanna order?"):
        # Append the user's message to the session state messages
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display the user's message in the chat interface (not relevant for the challenge)
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Generate a response from the assistant using the OpenAI model
        with st.chat_message("assistant"):
            stream = st.session_state.pizza_agent.astream_events({"messages": [
                    HumanMessage(content=msg["content"]) if msg["role"] == "user" 
                    else AIMessage(content=msg["content"]) 
                    for msg in st.session_state.messages]}, 
                    config=st.session_state.config,
                    version="v1"
                )
            message_placeholder = st.empty()
            full_response = ""
            
            async for event in stream:
                if event["event"] == "on_chat_model_stream":
                    content = event["data"]["chunk"].content
                    if content:
                        full_response += content
                        message_placeholder.markdown(full_response + "▌")
            
            # Final update without the cursor
            message_placeholder.markdown(full_response)
            response = full_response
        # Append the assistant's response to the session state messages
        st.session_state.messages.append({"role": "assistant", "content": response})

# Add navigation in the sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Order Pizza", "View Orders"])

# Display menu in the sidebar
st.sidebar.header("Our Menu")

# Display pizzas
st.sidebar.subheader("Pizzas")
if isinstance(pizzeria_menu["pizzas"], list):
    for pizza in pizzeria_menu["pizzas"]:
        st.sidebar.text(f"- {pizza['name']}")
else:
    st.sidebar.write("No pizzas available at the moment.")

st.sidebar.write("---")

# Display toppings
st.sidebar.subheader("Extra Toppings")
if isinstance(pizzeria_menu["toppings"], list):
    for topping in pizzeria_menu["toppings"]:
        st.sidebar.text(f"- {topping['name']}")
else:
    st.sidebar.write("No toppings available at the moment.")

st.sidebar.write("---")

# Display sides
st.sidebar.subheader("Sides")
if isinstance(pizzeria_menu["sides"], list):
    for side in pizzeria_menu["sides"]:
        st.sidebar.text(f"- {side['name']}")
else:
    st.sidebar.write("No sides available at the moment.")
    
st.sidebar.write("---")

# Display drinks
st.sidebar.subheader("Drinks")
if isinstance(pizzeria_menu["drinks"], list):
    for drink in pizzeria_menu["drinks"]:
        st.sidebar.text(f"- {drink['name']}")
else:
    st.sidebar.write("No drinks available at the moment.")

    st.sidebar.write(f"- {drink['name']}")



if page == "Order Pizza":
    asyncio.run(main_page())
elif page == "View Orders":
    show_orders_page()