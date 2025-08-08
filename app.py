import streamlit as st
import pandas as pd
import gspread
from google.oauth2 import service_account

st.set_page_config(layout="wide")
st.title("🖼️ Exposición Digital de Gabinetes")

def connect_to_google_sheets():
    try:
        creds_dict = {
            "type": st.secrets["gcp_type"], "project_id": st.secrets["gop_project_id"],
            "private_key_id": st.secrets["gcp_private_key_id"], "private_key": st.secrets["gcp_private_key"],
            "client_email": st.secrets["gcp_client_email"], "client_id": st.secrets["gcp_client_id"],
            "auth_uri": st.secrets["gcp_auth_uri"], "token_uri": st.secrets["gcp_token_uri"],
            "auth_provider_x509_cert_url": st.secrets["gcp_auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["gcp_client_x509_cert_url"],
        }
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"Error de autenticación: {e}")
        return None

def load_data(client):
    try:
        sheet = client.open("Mi gabinete personal (Respuestas)").sheet1
        return pd.DataFrame(sheet.get_all_records())
    except Exception as e:
        st.error(f"Ocurrió un error al cargar los datos de la hoja: {e}")
        return pd.DataFrame()

st.markdown("Explora los análisis y descubrimientos realizados por todos los participantes del curso.")
client = connect_to_google_sheets()

if client:
    df = load_data(client)
    if not df.empty:
        df = df.iloc[::-1]
        for index, row in df.iterrows():
            st.divider()
            col_carrera = "Carrera"
            col_artefacto = "El artefacto central: Describe el único objeto, real o imaginado, que está en el corazón de tu Gabinete."
            col_pitch = "El Pitch (La Revelación Controlada)\nEscribe aquí tu pitch (máximo 3 minutos de lectura). Responde: ¿Por qué este Gabinete merece existir y qué debería sentir alguien al visitarlo?"
            col_imagen = "Mi Gabinete"
            col_timestamp = "Marca temporal"
            col1, col2 = st.columns([1, 2])
            with col1:
                if col_imagen in row and row[col_imagen]: st.image(row[col_imagen], use_container_width=True)
            with col2:
                if col_carrera in row: st.subheader(f"Gabinete de: {row[col_carrera]}")
                if col_artefacto in row: st.markdown(f"**Artefacto Central:** {row[col_artefacto]}")
                if col_pitch in row: st.markdown(f"**El Pitch:** *\"{row[col_pitch]}\"*")
                if col_timestamp in row: st.caption(f"Publicado el: {row[col_timestamp]}")
    else:
        st.info("Aún no hay respuestas en el formulario o no se pudieron cargar. ¡La galería aparecerá aquí cuando los alumnos empiecen a participar!")
