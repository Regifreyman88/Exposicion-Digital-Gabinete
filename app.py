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
if img_base64:
    # CSS para el fondo y las tarjetas de la galería
    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("data:image/jpeg;base64,{img_base64}");
        background-size: cover; background-position: center;
        background-repeat: no-repeat; background-attachment: fixed;
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
    """, unsafe_allow_html=True)

# --- TÍTULO ---
st.title("Galería de Gabinetes")
st.markdown("<h3 style='text-align: center; color: #E0E0E0;'>Archivo de regalos simbólicos</h3><br>", unsafe_allow_html=True)

# --- FUNCIÓN PARA CONECTAR Y LEER GOOGLE SHEETS ---
@st.cache_data(ttl=60)
def load_data():
    try:
        # Usa los secretos directamente. st.secrets es un diccionario.
        creds = dict(st.secrets)
        sa = gspread.service_account_from_dict(creds)
        spreadsheet = sa.open_by_url("https://docs.google.com/spreadsheets/d/1mLZEeMS0mxOXcPjy83-AtoHyXJ1M1pKDoICjM8iy20s/edit")
        worksheet = spreadsheet.worksheet("Respuestas de formulario 1")
        df = get_as_dataframe(worksheet)
        
        # Elimina filas donde el título está vacío para evitar errores
        df.dropna(subset=["Titulo"], inplace=True)
        return df
    except gspread.exceptions.SpreadsheetNotFound:
        st.error("Error: No se encontró la hoja de cálculo. Asegúrate de que el enlace es correcto y que has compartido la hoja con el email de la cuenta de servicio.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"No se pudo conectar o leer la hoja de cálculo: {e}")
        return pd.DataFrame()

# --- CARGAR Y MOSTRAR DATOS ---
df = load_data()

if not df.empty:
    # --- NOMBRES DE COLUMNA SIMPLIFICADOS (VERIFICA QUE COINCIDAN CON TU HOJA) ---
    COL_NOMBRE = "Nombre"
    COL_TITULO = "Titulo"
    COL_IMAGEN_GABINETE = "ImagenGabinete"
    COL_DESCRIPCION = "Descripcion"

    # --- RENDERIZAR LA GALERÍA ---
    st.markdown("---")
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
                </details>
            </div>
            """, unsafe_allow_html=True)
else:
    st.warning("No se encontraron datos en la hoja de cálculo o hubo un error al cargar.")
