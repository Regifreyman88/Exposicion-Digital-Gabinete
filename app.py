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
# El f-string que causaba el error ahora está corregido y completo.
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
        background-color: rgba(20, 30, 40, 0.9);
        border: 2px solid #5a7a9a;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        height: 100%;
        box-shadow: 0px 0px 20px 5px rgba(118, 202, 255, 0.2);
    }}
    .gallery-card h3 {{ /* Título del Gabinete */
        color: #76CAFF;
        font-family: 'Georgia', serif;
        text-align: center;
    }}
    .gallery-card .caption {{ /* Autor */
        text-align: center;
        font-style: italic;
        color: #CCCCCC;
    }}
    .gallery-card img {{ /* Imagen Principal */
        border-radius: 5px;
    }}
    .stExpander {{ /* Contenedor de detalles */
        background-color: transparent !important;
    }}
</style>
""", unsafe_allow_html=True)

# --- TÍTULO ---
st.title("Galería de Gabinetes")
st.markdown("<h3 style='text-align: center;'>Archivo de regalos simbólicos</h3><br>", unsafe_allow_html=True)

# --- FUNCIÓN PARA CONECTAR Y LEER GOOGLE SHEETS ---
@st.cache_data(ttl=60)
def load_data():
    try:
        creds = dict(st.secrets)
        sa = gspread.service_account_from_dict(creds)
        spreadsheet = sa.open_by_url("https://docs.google.com/spreadsheets/d/1mLZEeMS0mxOXcPjy83-AtoHyXJ1M1pKDoICjM8iy20s/edit")
        worksheet = spreadsheet.worksheet("Respuestas de formulario 1")
        df = get_as_dataframe(worksheet, keep_default_na=False)
        return df
    except Exception as e:
        st.error(f"No se pudo conectar o leer la hoja de cálculo: {e}")
        return pd.DataFrame()

# --- CARGAR Y MOSTRAR DATOS ---
df = load_data()

if not df.empty:
    df.columns = df.columns.str.strip()
    required_columns = ["Nombre", "Carrera", "Titulo", "ImagenGabinete"]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        st.error
