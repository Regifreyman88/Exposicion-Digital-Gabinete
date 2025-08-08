      import streamlit as st
import pandas as pd
import base64

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Bitácora del Asombro",
    page_icon=" Mysteries",
    layout="wide"
)

# --- FUNCIÓN PARA CARGAR LA IMAGEN DE FONDO ---
@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- CARGA DE LA IMAGEN Y DEFINICIÓN DEL CSS ---
try:
    # Asegúrate de que tu imagen de portada esté en la misma carpeta que este script
    img_path = "portada_bitacora_con_imagen.png"
    img_base64 = get_img_as_base64(img_path)

    # El f-string que causaba el error ahora está corregido y completo.
    page_bg_img_css = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    [data-testid="stHeader"] {{
        background-color: rgba(0,0,0,0);
    }}
    .gift-container {{
        border: 2px solid #5a7a9a;
        border-radius: 10px;
        padding: 15px;
        background-color: rgba(12, 22, 37, 0.85);
        box-shadow: 0px 0px 15px 5px rgba(118, 202, 255, 0.3);
        transition: 0.3s;
        margin-bottom: 20px;
        height: 100%;
    }}
    .gift-container:hover {{
        box-shadow: 0px 0px 20px 8px rgba(118,
