import streamlit as st
import pandas as pd
import gspread
from google.oauth2 import service_account
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN Y TÍTULO ---
st.set_page_config(layout="wide")
st.title("🖼️ Exposición Digital de Gabinetes de Asombro")
st.image("portada_gabinete.jpg")

# --- CREDENCIALES ---
creds_dict = {
    "type": st.secrets["gcp_type"], "project_id": st.secrets["gcp_project_id"],
    "private_key_id": st.secrets["gcp_private_key_id"], "private_key": st.secrets["gcp_private_key"],
    "client_email": st.secrets["gcp_client_email"], "client_id": st.secrets["gcp_client_id"],
    "auth_uri": st.secrets["gcp_auth_uri"], "token_uri": st.secrets["gcp_token_uri"],
    "auth_provider_x509_cert_url": st.secrets["gcp_auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["gcp_client_x509_cert_url"],
}

@st.cache_resource(ttl=600)
def connect_to_google_sheets():
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"Error de autenticación: {e}")
        return None

@st.cache_data(ttl=600)
def load_data(_client):
    try:
        sheet = _client.open("Mi gabinete personal (Respuestas)").sheet1
        return pd.DataFrame(sheet.get_all_records())
    except Exception as e:
        st.error(f"Ocurrió un error al cargar los datos de la hoja: {e}")
        return pd.DataFrame()

st.markdown("### Explora los gabinetes y descubrimientos de la clase.")
client = connect_to_google_sheets()

if client:
    df = load_data(client)
    if not df.empty:
        # --- NOMBRES EXACTOS DE LAS COLUMNAS ---
        col_carrera = "Carrera"
        col_artefacto = "El artefacto central: Describe el único objeto, real o imaginado, que está en el corazón de tu Gabinete."
        col_pitch = "El Pitch (La Revelación Controlada)\nEscribe aquí tu pitch (máximo 3 minutos de lectura). Responde: ¿Por qué este Gabinete merece existir y qué debería sentir alguien al visitarlo?"
        col_imagen = "Mi Gabinete"
        col_timestamp = "Marca temporal"
        col_objeto_museo = "Objeto elegido del museo"
        col_metafora = "Cuál es la metáfora central (El Nombre Secreto): Elige una metáfora que defina el alma de tu Gabinete."
        col_salas = "Las 'Salas' principales: define de 3 a 5 'salas' o 'exhibiciones' dentro de tu Gabinete."
        col_sol_caverna = "Basado en la metáfora de la caverna, ¿cuál es el 'sol' de la verdad que tu artefacto te ayudó a imaginar?"
        col_cancion = "Canción de Sunno"

        # --- ZONA DE INTERACTIVIDAD EN LA BARRA LATERAL ---
        st.sidebar.header("Filtros de la Exposición")
        
        autores = ["Todos"] + list(df[col_carrera].unique())
        autor_seleccionado = st.sidebar.selectbox("Ver el gabinete de:", autores)
        
        search_term = st.sidebar.text_input("Buscar por palabra clave en el Pitch:")
        
        if st.sidebar.button("Generar Nube de Ideas Colectiva"):
            all_text = " ".join(df[col_pitch].astype(str)) + " ".join(df[col_metafora].astype(str))
            if all_text.strip():
                wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="viridis").generate(all_text)
                fig, ax = plt.subplots()
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis("off")
                st.pyplot(fig)
            else:
                st.sidebar.warning("No hay suficiente texto para generar la nube.")

        # --- LÓGICA DE FILTRADO ---
        df_filtrado = df
        if autor_seleccionado != "Todos":
            df_filtrado = df_filtrado[df_filtrado[col_carrera] == autor_seleccionado]
        if search_term:
            df_filtrado = df_filtrado[df_filtrado[col_pitch].str.contains(search_term, case=False, na=False)]

        # --- CONSTRUCCIÓN DE LA GALERÍA ---
        if df_filtrado.empty:
            st.warning("No se encontraron resultados para tu búsqueda.")
        else:
            df_filtrado = df_filtrado.iloc[::-1]
            for index, row in df_filtrado.iterrows():
                st.divider()
                col1, col2 = st.columns([2, 3])
                with col1:
                    st.image(row[col_imagen], use_container_width=True, caption=f"Objeto de Museo: {row[col_objeto_museo]}")
                with col2:
                    st.subheader(f"Gabinete de: {row[col_carrera]}")
                    st.caption(f"Publicado el: {row[col_timestamp]}")
                    with st.expander("Ver Análisis Completo"):
                        st.markdown(f"**Artefacto Central:** {row[col_artefacto]}")
                        st.markdown(f"**Metáfora Central (El Nombre Secreto):** {row[col_metafora]}")
                        st.markdown(f"**Las 'Salas' Principales:** {row[col_salas]}")
                        st.markdown(f"**El 'Sol' de la Verdad (Metáfora de la Caverna):** {row[col_sol_caverna]}")
                        st.markdown(f"**Banda Sonora (Canción de Suno):** {row[col_cancion]}")
                    st.markdown(f"#### El Pitch:")
                    st.info(f"*{row[col_pitch]}*")
    else:
        st.info("Aún no hay respuestas en el formulario. ¡La galería aparecerá aquí cuando los alumnos empiecen a participar!")
