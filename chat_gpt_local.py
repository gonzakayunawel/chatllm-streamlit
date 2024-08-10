import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from groq import Groq
import os
import magic

def file_type_inference(file_path):
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file_path)
    return file_type


# Llama a la clave API de otro archivo
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Título de la aplicación
st.title(":robot_face: My Local ChatGPT :sunglasses:")

uploaded_files = st.file_uploader(
    "Choose a file", accept_multiple_files=True
)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    st.write(bytes_data)
    file_type = file_type_inference(bytes_data)
    st.write(file_type)


init_content = "Hola, soy Local ChatGPT, un asistente que puede usar múltiples modelos de lenguaje para apoyarte, ¿En qué puedo ayudarte?"

# Using "with" notation
with st.sidebar:
    st.title("ChatGPT Model Selection")
    selected_model = st.radio(
        "Selecciona el modelo a utilizar",
        (
            "gpt-4o-mini",
            "gpt-4o",
            "gpt-3.5-turbo",
            "gpt-4-turbo",
            "llama3-8b-8192",
            "llama3-70b-8192",
            "mixtral-8x7b-32768",
        ),
    )

    client = OpenAI(api_key=GROQ_API_KEY)
    st.session_state["openai_model"] = selected_model

    st.write(f"Ahora estás usando el modelo: {st.session_state["openai_model"]}.")

    # Botón para reiniciar el contexto
    if st.button("Nuevo Chat"):
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": init_content,
            }
        ]

if selected_model in ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo", "gpt-4-turbo"]:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    client = Groq(api_key=GROQ_API_KEY)

# Inicializa el estado de la sesión si es necesario
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": init_content,
        }
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
            model=st.session_state["openai_model"],  # Se puede cambiar el modelo
            messages=st.session_state["messages"],
        )
        response_content = response.choices[0].message.content
        st.session_state["messages"].append(
            {"role": "assistant", "content": response_content}
        )
        st.chat_message("assistant").write(response_content)
    except Exception as e:
        st.error(f"Ocurrió un error al comunicarse con la API: {e}")
