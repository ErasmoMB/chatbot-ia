import streamlit as st
import speech_recognition as sr
import pyttsx3
from google import genai
import threading

# Inicializar el cliente de Gemini
client = genai.Client(api_key="YOUR_API_KEY")

# Inicializar el motor de texto a voz
engine = pyttsx3.init()

# Configuración de la página
st.set_page_config(page_title="Chatbot de Voz", page_icon="🤖")

# Título de la aplicación
st.title("🤖 Chatbot de Voz")

# Variable para controlar el estado del micrófono
microphone_active = True

# Función para capturar y convertir voz a texto
def capture_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while microphone_active:
            st.write("🎤 Escuchando...")  # Mensaje en la interfaz
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio, language="es-ES")
                st.write(f"📝 Texto: {text}")  # Mostrar texto en la interfaz
                return text
            except sr.UnknownValueError:
                st.write("❌ No se pudo entender el audio")  # Mensaje de error en la interfaz
                speak_text("No entendí lo que dijiste. Por favor, intenta de nuevo.")
            except sr.RequestError:
                st.write("⚠️ Error al conectar con el servicio de reconocimiento de voz")  # Mensaje de error en la interfaz
                return None

# Función para convertir texto a voz
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Función para manejar la conversación
def conversation():
    while microphone_active:
        user_input = capture_voice()
        if user_input:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=user_input
            )
            st.write(f"🤖 Respuesta: {response.text}")  # Mostrar respuesta en la interfaz
            speak_text(response.text)

# Botón para iniciar la conversación
if st.button("🎤 Iniciar Captura de Voz"):
    st.write("🎤 Iniciando captura de voz...")
    threading.Thread(target=conversation).start()

# Botón para silenciar el micrófono
if st.button("🔇 Silenciar Micrófono"):
    microphone_active = False
    st.write("🔇 Micrófono silenciado. Presiona el botón para activar el micrófono.")

# Botón para activar el micrófono
if not microphone_active and st.button("🔊 Activar Micrófono"):
    microphone_active = True
    st.write("🔊 Micrófono activado. Presiona el botón para iniciar la captura de voz.")

# Botón para finalizar la conversación
if st.button("🛑 Finalizar Conversación"):
    microphone_active = False
    st.write("🛑 Conversación finalizada.")