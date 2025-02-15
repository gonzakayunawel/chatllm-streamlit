import streamlit as st

from openai import OpenAI
from groq import Groq
from mistralai import Mistral
import anthropic
from load_text import extract_data


# Llama a la clave API de otro archivo

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
MISTRAL_API_KEY = st.secrets["MISTRAL_API_KEY"]
ANTHROPIC_API_KEY = st.secrets["ANTHROPIC_API_KEY"]


# Título de la aplicación
st.title(":robot_face: My Local ChatGPT :sunglasses:")


# ----- Subir archivos de texto para procesarlos ------


uploaded_file = st.file_uploader(
    "Sube un archivo en pdf, docx o txt.",
    accept_multiple_files=False,
    type=["pdf", "docx", "txt"],
    )

# Comprobar si se han subido archivos
if uploaded_file is not None:
    st.success(f"""
        Nombre : {uploaded_file.name} //
        Tamaño: {uploaded_file.size} bytes //
        Tipo  : {uploaded_file.type}
        """)
    # Extraer texto
    with uploaded_file as data:
        st.session_state["document"] = extract_data(data)

        doc_prompt = f"""
        Responde las preguntas del usuario en base al siguiente texto, si no puedes responder, responde con "No encuentro la respuesta".
        TEXTO: {st.session_state["document"]}
        """

        st.session_state["messages"].append({"role": "assistant", "content": doc_prompt})
else:
    st.warning("No se ha subido ningún archivo aún.")

# ----- system prompt ------

init_content = """
Hola, soy un Asistente de GenIA que permite acceder a múltiples m
odelos de lenguaje para apoyarte, ¿En qué puedo ayudarte hoy?
"""


# Using "with" notation
with st.sidebar:
    st.title("ChatGPT Model Selection")
    selected_model = st.selectbox(
        "Selecciona el modelo a utilizar",
        (
            "gpt-4o-mini",
            "gpt-4o",
            "gpt-3.5-turbo",
            "gpt-4-turbo",
            "llama3-8b-8192",
            "llama3-70b-8192",
            "mixtral-8x7b-32768",
            "mistral-large-latest",
            "claude-3-5-sonnet-20240620",
        ),
    )

    # st.session_state["llm_model"] = selected_model

    st.write(f"Ahora estás usando el modelo: {selected_model}.")

    # Botón para reiniciar el contexto
    if st.button("Nuevo Chat"):
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": init_content,
            }
        ]


# Inicializa el estado de la sesión si es necesario
if "messages" not in st.session_state:
    if selected_model != "claude-3-5-sonnet-20240620":
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

        if selected_model in ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo", "gpt-4-turbo"]:
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=selected_model,
                messages=st.session_state["messages"],
            )
        elif selected_model == "mistral-large-latest":
            client = Mistral(api_key=MISTRAL_API_KEY)
            response = client.chat.complete(
                model="mistral-large-latest",
                messages=st.session_state["messages"],
            )

        elif selected_model == "claude-3-5-sonnet-20240620":
            client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
            response = client.messages.create(
                model=selected_model,
                max_tokens=3000,
                temperature=0,
                system=init_content,
                messages=[{"role": "user", "content": [{"type": "text", "text": str(st.session_state["messages"])}]}],
            )
        else:
            client = Groq(api_key=GROQ_API_KEY)
            response = client.chat.completions.create(
                model=selected_model,  # Se puede cambiar el modelo
                messages=st.session_state["messages"],
            )

        if selected_model == "claude-3-5-sonnet-20240620":
            for msg in response.content:
                response_content = msg.text
        else:
            response_content = response.choices[0].message.content
        st.session_state["messages"].append(
            {"role": "assistant", "content": response_content}
        )
        st.chat_message("assistant").write(response_content)
    except Exception as e:
        st.error(f"Ocurrió un error al comunicarse con la API: {e}")
