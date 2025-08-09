import streamlit as st
import pandas as pd
import base64
import gspread
from gspread_dataframe import get_as_dataframe

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Bitácora del Asombro",
    page_icon="🖼️",
    layout="wide"
)

# --- FUNCIÓN PARA CARGAR LA IMAGEN DE FONDO ---
@st.cache_data
def get_img_as_base64(file):
    try:
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        st.warning(f"Advertencia: No se encontró la imagen de fondo '{file}'. La página funcionará sin ella.")
        return None

# --- FUNCIÓN PARA EXTRAER EL ID DE GOOGLE DRIVE ---
def get_drive_id(url):
    if isinstance(url, str) and '=' in url:
        return url.split('=')[1]
    return ""

# --- CARGA DE LA IMAGEN DE FONDO Y CSS ---
img_base64 = get_img_as_base64("portada_gabinete.jpg")
if img_base64:
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
        border: 2px solid #777; border-radius: 10px; padding: 15px;
        background-color: rgba(30, 30, 30, 0.9);
        box-shadow: 0px 0px 15px 5px rgba(255, 255, 255, 0.1);
        margin-bottom: 20px; height: 100%;
    }}
    .gallery-title {{
        font-size: 1.4em; font-weight: bold; color: #FFD700;
        font-family: 'Georgia', serif;
    }}
    .gallery-author {{ font-style: italic; color: #CCCCCC; margin-bottom: 10px; }}
    .gallery-img {{ width: 100%; border-radius: 5px; margin-bottom: 15px; }}
    </style>
    """
    st.markdown(page_bg_img_css, unsafe_allow_html=True)

# --- TÍTULO DE LA EXPOSICIÓN ---
st.title("Galería de Gabinetes")
st.markdown("<h3 style='text-align: center; color: #E0E0E0;'>Archivo de regalos simbólicos</h3><br>", unsafe_allow_html=True)

# --- FUNCIÓN PARA CONECTAR Y LEER GOOGLE SHEETS DE FORMA SEGURA ---
@st.cache_data(ttl=60)
def load_data():
    try:
        creds_dict = st.secrets["connections"]["gcs"]
        sa = gspread.service_account_from_dict(creds_dict)
        spreadsheet = sa.open_by_url("https://docs.google.com/spreadsheets/d/1mLZEeMS0mxOXcPjy83-AtoHyXJ1M1pKDoICjM8iy20s/edit")
        worksheet = spreadsheet.worksheet("Respuestas de formulario 1")
        df = get_as_dataframe(worksheet)
        df.dropna(subset=["Titulo"], inplace=True) # Elimina filas si el título está vacío
        return df
    except Exception as e:
        st.error(f"No se pudo conectar o leer la hoja de cálculo: {e}")
        return pd.DataFrame()

# --- CARGAR Y MOSTRAR LOS DATOS ---
df = load_data()

if not df.empty:
    # --- NOMBRES DE COLUMNAS SIMPLIFICADOS (VERIFICA QUE COINCIDAN CON TU HOJA) ---
    COL_NOMBRE = "Nombre"
    COL_TITULO = "Titulo"
    COL_IMAGEN_GABINETE = "ImagenGabinete"
    COL_DESCRIPCION = "Descripcion"
    COL_SOL_VERDAD = "SolVerdad"

    # --- RENDERIZAR LA GALERÍA ---
    num_columnas = 3
    cols = st.columns(num_columnas)

    for index, row in df.iterrows():
        with cols[index % num_columnas]:
            gabinete_img_id = get_drive_id(row.get(COL_IMAGEN_GABINETE, ""))

            st.markdown(f"""
            <div class="gallery-card">
                <p class="gallery-title">{row.get(COL_TITULO, "Sin Título")}</p>
                <p class="gallery-author">Presentado por: {row.get(COL_NOMBRE, "Anónimo")}</p>
                <img class="gallery-img" src="https://drive.google.com/uc?id={gabinete_img_id}" alt="{row.get(COL_TITULO, '')}">
                <details>
                    <summary>Ver más detalles</summary>
                    <p><strong>Artefacto Central:</strong> {row.get(COL_DESCRIPCION, 'No disponible')}</p>
                    <p><strong>El 'Sol' de la Verdad:</strong> {row.get(COL_SOL_VERDAD, 'No disponible')}</p>
                </details>
            </div>
            """, unsafe_allow_html=True)
else:
    st.warning("No se encontraron datos en la hoja de cálculo o hubo un error al cargar.")
