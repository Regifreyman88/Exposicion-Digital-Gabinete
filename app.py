import streamlit as st
import pandas as pd
import base64  # Necesario para poner tu imagen de fondo

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Bitácora del Asombro",
    page_icon=" Mysteries",  # Un emoji que encaja con el tema
    layout="wide"
)

# --- FUNCIÓN PARA CARGAR LA IMAGEN DE FONDO ---
# Esta función convierte tu imagen en un formato que CSS puede usar
@st.cache_data  # Esto hace que la imagen se cargue solo una vez
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- CARGA DE LA IMAGEN DE PORTADA ---
# ASEGÚRATE DE QUE EL ARCHIVO 'portada_bitacora_con_imagen.png'
# ESTÉ EN LA MISMA CARPETA QUE ESTE SCRIPT.
try:
    img = get_img_as_base64("portada_bitacora_con_imagen.png")
    # --- INYECTAR CSS CON TU TEMA ---
    # Aquí está la magia del diseño. Usamos los colores y la sensación de tu portada.
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("data:image/png;base64,{img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    [data-testid="stHeader"] {{
        background-color: rgba(0,0,0,0);
    }}

    /* Estilo para el contenedor de cada "regalo" */
    .gift-container {{
        border: 2px solid #5a7a9a; /* Un borde con el color azul de la portada */
        border-radius: 10px;
        padding: 15px;
        background-color: rgba(12, 22, 37, 0.85); /* Fondo azul oscuro semi-transparente */
        box-shadow: 0px 0px 15px 5px rgba(118, 202, 255, 0.3); /* Un brillo azul cian como el del interior del gabinete */
        transition: 0.3s;
        margin-bottom: 20px; /* Espacio entre los elementos de la galería */
        height: 100%; /* Asegura que todos los contenedores en una fila tengan la misma altura */
