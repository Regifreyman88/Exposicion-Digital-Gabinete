import streamlit as st
import pandas as pd
import base64
import gspread
from gspread_dataframe import get_as_dataframe

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Galería de Gabinetes", page_icon="🖼️", layout="wide")

# --- FUNCIÓN PARA CARGAR LA IMAGEN DE FONDO ---
@st.cache_data
def get_img_as_base64(file):
    try:
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        st.warning(f"Advertencia: No se encontró la imagen de fondo '{file}'.")
        return None

# --- FUNCIÓN PARA EXTRAER EL ID DE GOOGLE DRIVE ---
def get_drive_id(url):
    if isinstance(url, str) and '=' in url:
        return url.split('=')[1]
    return ""

# --- APLICAR ESTILOS Y FONDO ---
img_base64 = get_img_as_base64("portada_gabinete.jpg")
st.markdown(f"""
<style>
    /* --- FONDO --- */
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("data:image/jpeg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    /* --- TARJETA DE LA GALERÍA --- */
    .gallery-card {{
        background-color: rgba(20, 30, 40, 0.92);
        border: 2px solid #5a7a9a;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        height: 100%;
        box-shadow: 0px 0px 20px 5px rgba(118, 202, 255, 0.2);
        transition: transform 0.3s ease-in-out;
    }}
    .gallery-card:hover {{
        transform: scale(1.03);
    }}
    /* --- TÍTULOS Y TEXTOS DENTRO DE LA TARJETA --- */
    .gallery-card h3 {{
        color: #76CAFF;
        font-family: 'Georgia', serif;
        text-align: center;
        margin-bottom: 1rem;
    }}
    .gallery-card .caption {{
        text-align: center;
        font-style: italic;
        color: #CCCCCC;
    }}
    .gallery-card img {{
        border-radius: 5px;
    }}
    /* --- ESTILO DEL BOTÓN EXPANDIBLE --- */
    .stExpander {{
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}
    .stExpander header {{
        color: #FFD700 !important;
    }}
</style>
""",
