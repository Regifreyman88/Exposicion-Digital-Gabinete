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

# --- FUNCIÓN PARA EXTRAER EL ID DE GOOGLE DRIVE ---
def get_drive_id(url):
    if isinstance(url, str) and '=' in url:
        return url.split('=')[1]
    return ""

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
    .cover-image {{
        width: 100%;
        border-radius: 10px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
    }}
    </style>
    """
    st.markdown(page_bg_img_css, unsafe_allow_html=True)
except FileNotFoundError:
    st.error(f"Error: No se encontró el archivo de la portada ('{img_path}').")
    st.stop()

# --- TÍTULO DE LA EXPOSICIÓN ---
st.title("Mi Gabinete")
st.markdown("<h3 style='text-align: center; color: #E0E0E0; font-family: Courier New, monospace;'>Archivo de regalos simbólicos ofrecidos al Asombro en tránsito</h3><br>", unsafe_allow_html=True)

# --- CARGAR LOS DATOS DESDE GOOGLE SHEETS ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQA-RtFzjQk1Fa8rFpMDrF2NKYVwyliJhhXd6vduGnbmIoggbL7KOyJkaxIKh5AUcJM9sxzBExOgnHX/pub?gid=562854143&single=true&output=csv"

try:
    df = pd.read_csv(SHEET_URL)

    # --- NOMBRES DE COLUMNA SIMPLIFICADOS ---
    # Asegúrate de que estos nombres coincidan con los que pusiste en tu Google Sheet
    COL_NOMBRE = "Nombre"
    COL_CARRERA = "Carrera"
    COL_IMAGEN_MUSEO = "ImagenMuseo"
    COL_SOL_VERDAD = "SolVerdad"
    COL_TITULO = "Titulo"
    COL_AUDIO = "Audio"
    COL_SALAS = "Salas"
    COL_DESCRIPCION = "Descripcion"
    COL_PITCH = "Pitch"
    COL_IMAGEN_GABINETE = "ImagenGabinete"

    # --- RENDERIZAR LA GALERÍA DE PORTADAS ---
    num_columnas = 3
    cols = st.columns(num_columnas)

    for index, row in df.iterrows():
        col = cols[index % num_columnas]
        
        # Extraer IDs de Drive
        gabinete_img_id = get_drive_id(row[COL_IMAGEN_GABINETE])
        museo_img_id = get_drive_id(row[COL_IMAGEN_MUSEO])
        audio_id = get_drive_id(row[COL_AUDIO])

        # Crear un expansor para cada gabinete
        with col:
            st.image(f"https://drive.google.com/uc?id={gabinete_img_id}", use_column_width=True, caption=row[COL_TITULO])
            with st.expander("Ver detalles de la colección"):
                
                # --- Contenido Detallado Dentro del Expansor ---
                st.subheader(row[COL_TITULO])
                st.caption(f"Presentado por: {row[COL_NOMBRE]} ({row[COL_CARRERA]})")

                # Reproductor de Audio
                if audio_id:
                    st.audio(f"https://drive.google.com/uc?id={audio_id}", format='audio/wav')

                # Pestañas para organizar el texto
                tab1, tab2, tab3 = st.tabs(["El Artefacto", "La Revelación", "Las Salas"])

                with tab1:
                    st.write("**Descripción del Artefacto Central:**")
                    st.write(row[COL_DESCRIPCION])
                    if museo_img_id:
                        st.image(f"https://drive.google.com/uc?id={museo_img_id}", use_column_width=True, caption="Objeto del Museo")
                
                with tab2:
                    st.write("**El 'Sol' de la Verdad:**")
                    st.write(row[COL_SOL_VERDAD])
                    st.write("---")
                    st.write("**El Pitch:**")
                    st.write(row[COL_PITCH])
                
                with tab3:
                    st.write("**Las Salas del Gabinete:**")
                    st.write(row[COL_SALAS])


except Exception as e:
    st.error(f"Error al cargar o procesar los datos: {e}")
    st.warning("Verifica que el enlace de tu Google Sheet esté publicado como CSV y que los nombres de las columnas en el archivo coincidan con los del código.")
