import streamlit as st
import pandas as pd
import base64

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Bitácora del Asombro",
    page_icon="🖼️",
    layout="wide"
)

# --- FUNCIÓN PARA CARGAR LA IMAGEN DE FONDO ---
@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- FUNCIÓN PARA EXTRAER EL ID DE GOOGLE DRIVE ---
def get_drive_id(url):
    if isinstance(url, str) and '=' in url:
        return url.split('=')[1]
    return ""

# --- CARGA DE LA IMAGEN DE FONDO Y CSS ---
try:
    img_path = "portada_gabinete.jpg"
    img_base64 = get_img_as_base64(img_path)
    page_bg_img_css = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("data:image/jpeg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .gallery-card {{
        border: 2px solid #777;
        border-radius: 10px;
        padding: 15px;
        background-color: rgba(30, 30, 30, 0.9);
        box-shadow: 0px 0px 15px 5px rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        height: 100%;
    }}
    .gallery-title {{
        font-size: 1.4em;
        font-weight: bold;
        color: #FFD700; /* Color dorado para el título */
        font-family: 'Georgia', serif;
    }}
    .gallery-author {{
        font-style: italic;
        color: #CCCCCC;
        margin-bottom: 10px;
    }}
    .gallery-img {{
        width: 100%;
        border-radius: 5px;
        margin-bottom: 15px;
    }}
    .decorative-img {{
        width: 50px;
        height: 50px;
        border-radius: 50%;
        object-fit: cover;
        float: right;
        border: 2px solid #FFD700;
    }}
    </style>
    """
    st.markdown(page_bg_img_css, unsafe_allow_html=True)
except FileNotFoundError:
    st.error(f"Error: No se encontró el archivo de la portada ('{img_path}').")
    st.stop()

# --- TÍTULO DE LA EXPOSICIÓN ---
st.title("Galería de Gabinetes")
st.markdown("<h3 style='text-align: center; color: #E0E0E0; font-family: Courier New, monospace;'>Archivo de regalos simbólicos ofrecidos al Asombro en tránsito</h3><br>", unsafe_allow_html=True)

# --- CARGAR LOS DATOS ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQA-RtFzjQk1Fa8rFpMDrF2NKYVwyliJhhXd6vduGnbmIoggbL7KOyJkaxIKh5AUcJM9sxzBExOgnHX/pub?gid=562854143&single=true&output=csv"

try:
