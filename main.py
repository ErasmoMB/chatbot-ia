import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Inicializar el cliente de Gemini
api_key = os.getenv("YOUR_API_KEY")  # Cargar la clave de API
client = genai.Client(api_key=api_key)  # Usar la clave de API cargada

# Configuración de la página
st.set_page_config(
    page_title="Chatbot con Gemini",
    page_icon="🗣️",
    layout="centered"
)

# Título y descripción
st.title("🗣️ Chatbot")
st.markdown("""
Este chatbot está diseñado para interactuar con los usuarios utilizando el modelo Gemini.
""")

# Inicializar el historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar el historial de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del usuario
if prompt := st.chat_input("¿Qué te gustaría saber?"):
    # Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Generar la respuesta usando Gemini
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            response_text = response.text  # Asumiendo que el output tiene un atributo text
            
            # Mostrar la respuesta
            message_placeholder.markdown(response_text)
            
            # Agregar la respuesta al historial
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
        except Exception as e:
            error_message = f"Error: {str(e)}"
            message_placeholder.error(error_message)