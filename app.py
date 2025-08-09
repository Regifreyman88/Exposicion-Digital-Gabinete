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
        color: #FFD700;
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
    # Esta sección ahora está correctamente indentada
    df = pd.read_csv(SHEET_URL)
    if df.empty:
        st.error("Error Crítico: El archivo CSV leído desde Google Sheets está vacío.")
        st.stop()

    COL_NOMBRE = "Nombre"
    COL_TITULO = "Titulo"
    COL_IMAGEN_GABINETE = "ImagenGabinete"
    COL_DESCRIPCION = "Descripcion"
    COL_SOL_VERDAD = "SolVerdad"

    decorative_images = [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg/402px-Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Vincent_van_Gogh_-_The_Starry_Night_-_Google_Art_Project.jpg/600px-Vincent_van_Gogh_-_The_Starry_Night_-_Google_Art_Project.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/The_Persistence_of_Memory.jpg/640px-The_Persistence_of_Memory.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/The_Scream.jpg/499px-The_Scream.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Vermeer_-_The_Girl_With_The_Pearl_Earring.jpg/488px-Vermeer_-_The_Girl_With_The_Pearl_Earring.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Sandro_Botticelli_-_La_nascita_di_Venere_-_Google_Art_Project_-_edited.jpg/640px-Sandro_Botticelli_-_La_nascita_di_Venere_-_Google_Art_Project_-_edited.jpg"
    ]

    num_columnas = 3
    cols = st.columns(num_columnas)

    for index, row in df.iterrows():
        col = cols[index % num_columnas]
        with col:
            gabinete_img_id = get_drive_id(row[COL_IMAGEN_GABINETE])
            decorative_img_url = decorative_images[index % len(decorative_images)]

            st.markdown(f"""
            <div class="gallery-card">
                <img src="{decorative_img_url}" class="decorative-img">
                <p class="gallery-title">{row[COL_TITULO]}</p>
                <p class="gallery-author">Presentado por: {row[COL_NOMBRE]}</p>
                <img class="gallery-img" src="https://drive.google.com/uc?id={gabinete_img_id}" alt="{row[COL_TITULO]}">
                <details>
                    <summary>Ver más detalles</summary>
                    <p><strong>Artefacto Central:</strong> {row.get(COL_DESCRIPCION, 'No disponible')}</p>
                    <p><strong>El 'Sol' de la Verdad:</strong> {row.get(COL_SOL_VERDAD, 'No disponible')}</p>
                </details>
            </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error al cargar o procesar los datos: {e}")
    st.warning("Verifica que tu Google Sheet tenga las columnas con los nombres simplificados: 'Nombre', 'Titulo', 'ImagenGabinete', 'Descripcion', 'SolVerdad'.")
