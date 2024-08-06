import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Llama a la clave API de otro archivo
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# Título de la aplicación
st.title(":robot_face: Mi ChatGPT :sunglasses:")

# Inicializa el estado de la sesión si es necesario
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hola, soy ChatGPT, ¿En qué puedo ayudarte?"}
    ]

# Mostrar mensajes existentes
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# Campo de entrada del usuario
if user_input := st.chat_input():
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Manejo de errores en la respuesta
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Se puede cambiar el modelo
            messages=st.session_state["messages"],
        )
        response_content = response.choices[0].message.content
        st.session_state["messages"].append(
            {"role": "assistant", "content": response_content}
        )
        st.chat_message("assistant").write(response_content)
    except Exception as e:
        st.error(f"Ocurrió un error al comunicarse con la API: {e}")

# Botón para reiniciar el contexto
if st.button("Nuevo Chat"):
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hola, soy ChatGPT, ¿En qué puedo ayudarte?"}
    ]