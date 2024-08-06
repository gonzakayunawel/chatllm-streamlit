import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from groq import Groq
import os

# Load API keys from another file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Application title
st.title(":robot_face: My ChatGPT :sunglasses:")

# Model selection
with st.sidebar:
    st.title("ChatGPT Model Selection")
    selected_model = st.radio(
        "Select the model to use",
        ("gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo", "gpt-4-turbo", "llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768")
    )

    client = OpenAI(api_key=GROQ_API_KEY)
    st.session_state["openai_model"] = selected_model

    st.write(f"You are now using the model: {st.session_state["openai_model"]}.")

if selected_model in ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo", "gpt-4-turbo"]:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    client = Groq(api_key=GROQ_API_KEY)

# Initialize session state if necessary
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello, I'm ChatGPT custom, how can I help you?"}
    ]

# File uploader
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # To convert to a string:
    string_data = bytes_data.decode('utf-8')
    # Now you can use string_data or bytes_data as needed

# Display existing messages
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# User input field
if user_input := st.chat_input():
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Error handling for the response
    try:
        response = client.chat.completions.create(
            model=st.session_state["openai_model"],  # Model can be changed
            messages=st.session_state["messages"],
        )
        response_content = response.choices[0].message.content
        st.session_state["messages"].append(
            {"role": "assistant", "content": response_content}
        )
        st.chat_message("assistant").write(response_content)
    except Exception as e:
        st.error(f"An error occurred while communicating with the API: {e}")

# Button to reset the context
if st.button("New Chat"):
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello, I'm ChatGPT, how can I help you?"}
    ]
