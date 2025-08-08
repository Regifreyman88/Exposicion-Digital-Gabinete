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

# --- CREDENCIALES INCRUSTADAS EN EL CÓDIGO ---
creds_dict = {
  "type": "service_account",
  "project_id": "mi-galeria-digital",
  "private_key_id": "aaddc8c3d6442d54c6e263cd7d2293e078b6ce05",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCr5WjUA75I8Zos\n07C1XPllo4cLfYA0KQ0zXRgEoEWfrhP0+QYM896zBj9JBqGaCguF6pIZ+g6HobDC\njos2fzBhnC3aJoyIPT1AHDCI+rtvDNL45PwnrsfbfNckifOyWPwoNNlrb5ZNFL7g\nN+1ZFBF7DpwPG6ArzfOOu13jfs8jj3oebPdpJe3XsSTLdAYMzfWOuGo1o9V4e3s3\n+iwOPYVOr10LRoto4GfAkqGdbGpafWYcc/mGkL4BuK6HZIb4D6Bg8gAf4ADlHyzN\nzb9AulVTFzYovfYeerYwpJTvsjYHoklMdf12ZLlkkVSSk0+Hc+ZSI8JVjVJq7GDy\nUTmjxz2LAgMBAAECggEAD6FytiSzqYpeofOLPqf6UvsFt/kXg/wKTpYJLb0tLOdK\nupySUkcyrvDD
