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
    .entry-container {{
        border: 2px solid #777;
        border-radius: 10px;
        padding: 25px;
        background-color: rgba(30, 30, 30, 0.9);
        margin-bottom: 30px;
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
    df.columns = df.columns.str.strip()

    # --- NOMBRES DE COLUMNA ---
    required_columns = ["Nombre", "Carrera", "Titulo", "ImagenGabinete", "Descripcion", "ImagenMuseo", "SolVerdad", "Audio", "Salas", "Pitch"]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        st.error(f"Error Crítico: Faltan las siguientes columnas en tu Google Sheet: {missing_columns}")
        st.info(f"Por favor, renombra los encabezados en tu Google Sheet. Columnas encontradas: {list(df.columns)}")
        st.stop()
    
    df_filtered = df[(df["Titulo"] != "") & (df["ImagenGabinete"] != "")].copy()

    if df_filtered.empty:
        st.warning("No se encontraron gabinetes con un 'Titulo' y una 'ImagenGabinete' definidos.")
    else:
        st.markdown("---")
        
        # --- RENDERIZAR CADA GABINETE COMO UNA FICHA COMPLETA ---
        for index, row in df_filtered.iterrows():
            with st.container():
                st.markdown('<div class="entry-container">', unsafe_allow_html=True)
                
                # Encabezado
                st.header(row.get("Titulo", "Sin Título"))
                st.caption(f"Evidencia presentada por: {row.get('Nombre', 'Anónimo')} ({row.get('Carrera', 'N/A')})")
                st.markdown("---")
                
                # Columnas para imagen principal y artefacto
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Mi Gabinete")
                    gabinete_img_id = get_drive_id(row.get("ImagenGabinete", ""))
                    if gabinete_img_id:
                        st.image(f"https://drive.google.com/uc?id={gabinete_img_id}", use_column_width=True)
                
                with col2:
                    st.subheader("El Artefacto Central")
                    st.write(row.get("Descripcion", "No disponible"))
                    
                    st.subheader("Objeto del Museo")
                    museo_img_id = get_drive_id(row.get("ImagenMuseo", ""))
                    if museo_img_id:
                        st.image(f"https://drive.google.com/uc?id={museo_img_id}", use_column_width=True)

                # Audio (si existe)
                st.subheader("Paisaje Sonoro")
                audio_id = get_drive_id(row.get("Audio", ""))
                if audio_id:
                    st.audio(f"https://drive.google.com/uc?id={audio_id}")
                else:
                    st.text("No se proporcionó audio.")
                
                st.markdown("---")
                
                # Pestañas para el resto de la información
                tab1, tab2, tab3 = st.tabs(["💡 La Revelación", "🏛️ Las Salas", "📢 El Pitch"])

                with tab1:
                    st.subheader("El 'Sol' de la Verdad")
                    st.write(row.get("SolVerdad", "No disponible"))

                with tab2:
                    st.subheader("Las Salas del Gabinete")
                    st.write(row.get("Salas", "No disponible"))
                    
                with tab3:
                    st.subheader("El Pitch")
                    st.write(row.get("Pitch", "No disponible"))
                
                st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("No se encontraron datos en la hoja de cálculo o hubo un error al cargar.")
