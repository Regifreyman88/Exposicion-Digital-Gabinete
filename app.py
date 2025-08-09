import streamlit as st
import pandas as pd
import gspread
from gspread_dataframe import get_as_dataframe

st.set_page_config(page_title="Diagnóstico de Columnas", layout="wide")

st.title("Diagnóstico de la Conexión")
st.write("Esta página intentará conectarse a tu Google Sheet y mostrar los nombres exactos de las columnas que está leyendo.")

# --- FUNCIÓN PARA CONECTAR Y LEER GOOGLE SHEETS ---
@st.cache_data(ttl=10) # Un cache corto para poder refrescar
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
        return None

# --- CARGAR Y MOSTRAR LOS NOMBRES DE LAS COLUMNAS ---
df = load_data()

if df is not None:
    if not df.empty:
        st.success("¡Conexión exitosa! Se han leído los datos.")
        st.write("A continuación, la lista de los nombres de columna EXACTOS que se encontraron en tu archivo. Por favor, copia esta lista y pégala en nuestra conversación.")
        
        # Imprime la lista de columnas para diagnóstico
        st.code(f"Columnas encontradas: {list(df.columns)}")
        
    else:
        st.error("La conexión fue exitosa, pero la hoja de cálculo parece estar vacía.")
