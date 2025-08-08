import streamlit as st
import pandas as pd
import gspread
from google.oauth2 import service_account

# --- CONFIGURACIÓN Y TÍTULO ---
st.set_page_config(layout="wide")
st.title("🖼️ Exposición Digital de Gabinetes de Asombro")
st.image("portada_gabinete.jpg")

# --- CREDENCIALES INCRUSTADAS EN EL CÓDIGO ---
# Este diccionario contiene la "llave secreta" de forma segura
creds_dict = {
  "type": "service_account",
  "project_id": "mi-galeria-digital",
  "private_key_id": "aaddc8c3d6442d54c6e263cd7d2293e078b6ce05",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCr5WjUA75I8Zos\n07C1XPllo4cLfYA0KQ0zXRgEoEWfrhP0+QYM896zBj9JBqGaCguF6pIZ+g6HobDC\njos2fzBhnC3aJoyIPT1AHDCI+rtvDNL45PwnrsfbfNckifOyWPwoNNlrb5ZNFL7g\nN+1ZFBF7DpwPG6ArzfOOu13jfs8jj3oebPdpJe3XsSTLdAYMzfWOuGo1o9V4e3s3\n+iwOPYVOr10LRoto4GfAkqGdbGpafWYcc/mGkL4BuK6HZIb4D6Bg8gAf4ADlHyzN\nzb9AulVTFzYovfYeerYwpJTvsjYHoklMdf12ZLlkkVSSk0+Hc+ZSI8JVjVJq7GDy\nUTmjxz2LAgMBAAECggEAD6FytiSzqYpeofOLPqf6UvsFt/kXg/wKTpYJLb0tLOdK\nupySUkcyrvDDJxl1RGk5bFn3eGk756q/mfwVk0UJhIwLwf8otD1tU7u8e22L8ah8\nM/8OdsVL4xzSVhOSl1sZbXEw0WDPjVQfmd/mszzsl1YCwX+aQaFz+OdMvaJgT4lW\n6u20b2ajmWIeqWVrZFwe+xPVgHvae+eVGkW2T6Vy3Ht1AfGkyFw6heWkfsWCGIuC\npc4tV3T7TK38SPK1jIiP9SIk7gQWjvl1BxaIPFfdHJF89D7hK40bWLnI6Eo1eM5c\nCXVrOMwkQP/ceI+ECOM/8jkvND5hyOz8cJdArvb6kQKBgQDXSa6+zJRiqePS0nkz\nQlwvu6MfsxO+qnvUmvjDCU0k13XnYafWKgXCTu1Tqyaj71Y+grMYlJFl5ajaTYbF\n5xetTWP7uVw6JqXPLKOODjbzJd/jdCdovnOB+pXweobn0Lw4zPTqDJAvzrJmub5f\nIOeZhStsfhdGwpVBVECqDV/VDQKBgQDMZxaDMjdRYqb4pB7Jx3VS2Lf2No4g8//H\nhnXqWZOCQx4EZOqu+TgOUBpVWJG+mRPUaAe1t4DuBLHhu2Ji9sJufjNJnOm0dKSq\nyXpov0R1mohGsEypR3kW685dWE+SeUpDXjE7IDL/3vOSVCZj4ezOAwUL+o+lrUL9\nPZ+OQsPm9wKBgAEt5yYmar2rnpLeEknkmCquxXL8ASSvPGRqwOgYmfKUt5Gf6FJ1\nAnkRA53MtzZ4rilDgAWncrBzNJyVhiJ5ZJjPbrfHSSkMYyYiYXb6vvRQBczyKvEY\n8fsJS1743NpSO2W4QbMyhGuuny2O4OsWfA5MO3OpsSjzEew8sOn9jsPVAoGAYtQJ\nH3/9HR2My7VWqYsF3/um3qW8DJTM++S4SIns91OKROeiTN10y/7Q7Kj5NuV+n/l4\nmNTTwsGEXDckt+LFWXUtSQ9UNAsdvvHRfKnV6OLBtyPwvPwwwPNcgOd8+b4pOO9m\n8EZ+QhbDP+Ht+ec3ftgY7ZTFNX7TX+wWpEsFuzsCgYEAouDYQ+wtvC76lfoI8Laz\nUMl50QUy2G0wgoiKb6E95asI94PzMYn9sDT2SYjtoy1oMu5jH+rfY9Jw0FCbmbnf\niWGJbRIK8AHOBi1LcsrmYpelv+qOS0cZRvOhR96Ppa3xkhh0HOOcHN+pLxQwL0t7\n3Gpkz4uoiHZR3OzNIw913n8=\n-----END PRIVATE KEY-----".replace('\\n', '\n'),
    "client_email": "lector-galeria@mi-galeria-digital.iam.gserviceaccount.com",
    "client_id": "101267206338789906387", "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token", "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/lector-galeria%40mi-galeria-digital.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}
# --- FIN DE LAS CREDENCIALES ---

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
        # (El resto del código para mostrar la galería sigue aquí)
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
