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
    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("data:image/jpeg;base64,{img_base64}");
        background-size: cover; background-position: center;
        background-repeat: no-repeat; background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- TÍTULO ---
st.title("Galería de Gabinetes")
st.markdown("<h3 style='text-align: center; color: #E0E0E0;'>Archivo de regalos simbólicos</h3><br>", unsafe_allow_html=True)

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
    # --- NOMBRES DE COLUMNA SIMPLIFICADOS ---
    COL_NOMBRE = "Nombre"
    COL_TITULO = "Titulo"
    COL_IMAGEN_GABINETE = "ImagenGabinete"
    
    # Filtrar filas donde el título y la imagen principal no están vacíos
    df_filtered = df[(df[COL_TITULO] != "") & (df[COL_IMAGEN_GABINETE] != "")].copy()

    if df_filtered.empty:
        st.warning("No se encontraron gabinetes con un 'Titulo' y una 'ImagenGabinete' definidos en la hoja de cálculo.")
    else:
        st.markdown("---")
        num_columnas = 3
        cols = st.columns(num_columnas)
        
        for index, row in df_filtered.iterrows():
            with cols[index % num_columnas]:
                gabinete_img_id = get_drive_id(row.get(COL_IMAGEN_GABINETE, ""))
                titulo = row.get(COL_TITULO, "Sin Título")
                nombre = row.get(COL_NOMBRE, "Anónimo")
                
                st.subheader(titulo)
                st.caption(f"Presentado por: {nombre}")
                if gabinete_img_id:
                    st.image(f"https://drive.google.com/uc?id={gabinete_img_id}", use_column_width=True)
                
                with st.expander("Ver más detalles"):
                    st.write(f"**Descripción:** {row.get('Descripcion', 'No disponible')}")
                    st.write(f"**Salas:** {row.get('Salas', 'No disponible')}")
                    st.write(f"**Pitch:** {row.get('Pitch', 'No disponible')}")
else:
    st.warning("No se encontraron datos en la hoja de cálculo o hubo un error al cargar.")
