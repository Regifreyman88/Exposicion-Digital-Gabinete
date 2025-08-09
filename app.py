import streamlit as st
import pandas as pd
import base64
from streamlit_gsheets import GSheetsConnection

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

# --- TÍTULO DE LA EXPOSICIÓN ---
st.title("Galería de Gabinetes")
st.markdown("<h3 style='text-align: center; color: #333;'>Archivo de regalos simbólicos</h3><br>", unsafe_allow_html=True)

try:
    # --- CONEXIÓN DIRECTA A GOOGLE SHEETS USANDO LOS SECRETOS ---
    conn = st.connection("gcs", type=GSheetsConnection)
    df = conn.read(ttl="1m")

    # --- PASO DE DIAGNÓSTICO: MOSTRAR LOS NOMBRES DE COLUMNA REALES ---
    st.warning("Paso de Diagnóstico: Revisa los nombres de columna de abajo.")
    st.write("NOMBRES DE COLUMNA REALES LEÍDOS DESDE EL ARCHIVO:", df.columns)
    # --- FIN DEL PASO DE DIAGNÓSTICO ---

    if df.empty:
        st.error("Error Crítico: No se leyeron datos de Google Sheets. Verifica los permisos y los secretos.")
        st.stop()
        
    # --- NOMBRES DE COLUMNA SIMPLIFICADOS ---
    COL_NOMBRE = "Nombre"
    COL_TITULO = "Titulo"
    COL_IMAGEN_GABINETE = "ImagenGabinete" # Este es el que causa el error
    COL_DESCRIPCION = "Descripcion"
    COL_SOL_VERDAD = "SolVerdad"

    # --- RENDERIZAR LA GALERÍA ---
    st.markdown("---")
    num_columnas = 3
    cols = st.columns(num_columnas)

    for index, row in df.iterrows():
        col = cols[index % num_columnas]
        with col:
            gabinete_img_id = get_drive_id(row[COL_IMAGEN_GABINETE])

            st.subheader(row[COL_TITULO])
            st.caption(f"Presentado por: {row[COL_NOMBRE]}")
            if gabinete_img_id:
                st.image(f"https://drive.google.com/uc?id={gabinete_img_id}", use_column_width=True)
            
            with st.expander("Ver más detalles"):
                st.write(f"**Artefacto Central:** {row.get(COL_DESCRIPCION, 'No disponible')}")
                st.write(f"**El 'Sol' de la Verdad:** {row.get(COL_SOL_VERDAD, 'No disponible')}")

except Exception as e:
    st.error(f"Error al cargar o procesar los datos: {e}")
    st.warning("Verifica la configuración de la conexión en los Secretos de Streamlit y que la hoja de cálculo esté compartida con el email de servicio.")
