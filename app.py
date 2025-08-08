Claro, ese error de sintaxis significa que el bloque try no tiene su correspondiente except para manejar los errores. Esto suele suceder por un problema al copiar y pegar el código.

Aquí está el código completo con la estructura try...except corregida.

Código Corregido
Por favor, reemplaza todo el código de tu archivo con esta versión.

Python

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
        box-shadow: 0px 0px 20px 8px rgba(118, 202, 255, 0.5);
        transform: scale(1.02);
    }}
    .gift-title, .gift-author, .gift-desc {{
        font-family: 'Courier New', Courier, monospace;
        color: #E0E0E0;
    }}
    .gift-title {{
        font-size: 1.5em;
        font-weight: bold;
        color: #76CAFF;
    }}
    .gift-author {{
        font-style: italic;
        color: #A0A0A0;
        margin-bottom: 10px;
    }}
    .gift-img {{
        width: 100%;
        border-radius: 5px;
        margin-bottom: 15px;
    }}
    </style>
    """
    st.markdown(page_bg_img_css, unsafe_allow_html=True)

except FileNotFoundError:
    st.error(f"Error: No se encontró el archivo de la portada ('{img_path}'). Asegúrate de que el nombre en el código sea idéntico al del archivo subido y que esté en la misma carpeta.")
    st.stop()

# --- TÍTULO DE LA EXPOSICIÓN ---
st.title("Mi Gabinete")
st.markdown("<h3 style='text-align: center; color: #E0E0E0; font-family: Courier New, monospace;'>Archivo de regalos simbólicos ofrecidos al Asombro en tránsito</h3><br>", unsafe_allow_html=True)

# --- CARGAR LOS DATOS DESDE GOOGLE SHEETS ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQA-RtFzjQk1Fa8rFpMDrF2NKYVwyliJhhXd6vduGnbmIoggbL7KOyJkaxIKh5AUcJM9sxzBExOgnHX/pub?gid=562854143&single=true&output=csv"

try:
    df = pd.read_csv(SHEET_URL)

    # --- NOMBRES DE LAS COLUMNAS DE TU GOOGLE SHEET ---
    COL_CARRERA = "Carrera"
    COL_TITULO = "Cuál es la metáfora central (El Nombre Secreto): Elige una metáfora que defina el alma de tu Gabinete."
    COL_DESC = "El artefacto central: Describe el único objeto, real o imaginado, que está en el corazón de tu Gabinete."
    COL_IMG_URL = "Mi Gabinete"

    # --- RENDERIZAR LA GALERÍA ---
    num_columnas = 3
    cols = st.columns(num_columnas)

    for index, row in df.iterrows():
        with cols[index % num_columnas]:
            img_id = ""
            if isinstance(row[COL_IMG_URL], str) and '=' in row[COL_IMG_URL]:
                img_id = row[COL_IMG_URL].split('=')[1]

            autor = row.get(COL_CARRERA, "Anónimo")

            st.markdown(f"""
            <div class="gift-container">
                <p class="gift-title">{row[COL_TITULO]}</p>
                <p class="gift-author">Presentado por: {autor}</p>
                <img class="gift-img" src="https://drive.google.com/uc?id={img_id}" alt="{row[COL_TITULO]}">
                <p class="gift-desc">{row[COL_DESC]}</p>
            </div>
            """, unsafe_allow_html=True)

except KeyError as e:
    st.error(f"Error de Columna: No se encontró la columna {e}. Por favor, verifica que el nombre de la columna en el código sea EXACTAMENTE igual al de tu Google Sheet.")
except Exception as e:
    st.error(f"Error al cargar o procesar los datos de la bitácora: {e}")
    st.warning("Verifica que el enlace del Google Sheet sea correcto y esté publicado como CSV.")






