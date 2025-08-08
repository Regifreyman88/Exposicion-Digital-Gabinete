import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Gabinete de Curiosidades",
    page_icon="🖼️",
    layout="wide" # Usa el ancho completo de la página
)

st.title("Gabinete de Curiosidades Digital 🏛️")
st.write("Una colección de maravillas visuales y conceptuales.")

# --- TU LISTA DE OBRAS (Imágenes y textos) ---
# Sustituye esto con tus propias imágenes y textos
obras = [
    {"img": "https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?q=80&w=2574&auto=format&fit=crop", "titulo": "Florero Abstracto", "autor": "Artista Ficticio 1", "desc": "Una exploración del color y la forma en la naturaleza muerta."},
    {"img": "https://images.unsplash.com/photo-1536924940846-227afb31e2a5?q=80&w=2666&auto=format&fit=crop", "titulo": "Nebulosa Cósmica", "autor": "Artista Ficticio 2", "desc": "El universo capturado en un lienzo digital, mostrando la belleza del caos."},
    {"img": "https://images.unsplash.com/photo-1519125323398-675f0ddb6308?q=80&w=2670&auto=format&fit=crop", "titulo": "Paisaje Onírico", "autor": "Artista Ficticio 3", "desc": "Un paisaje que difumina la línea entre la realidad y los sueños."},
    {"img": "https://images.unsplash.com/photo-1552083974-186346191183?q=80&w=2670&auto=format&fit=crop", "titulo": "El Ojo del Bosque", "autor": "Artista Ficticio 4", "desc": "La naturaleza nos observa a través de esta composición serena y misteriosa."},
    {"img": "https://images.unsplash.com/photo-1578301978018-3005759f48f7?q=80&w=2572&auto=format&fit=crop", "titulo": "Escultura de Luz", "autor": "Artista Ficticio 5", "desc": "Formas geométricas que cobran vida a través de la interacción con la luz."},
    {"img": "https://images.unsplash.com/photo-1506806732259-39c2d0268443?q=80&w=2574&auto=format&fit=crop", "titulo": "Retrato Fragmentado", "autor": "Artista Ficticio 6", "desc": "Una deconstrucción de la identidad a través de fragmentos visuales."}
]

# --- INYECTAR CSS PARA EL ESTILO ---
# Este es el truco para hacerla "vistosa"
st.markdown("""
<style>
    /* Contenedor de cada imagen para darle un marco y sombra */
    .img-container {
        border-radius: 10px;
        padding: 10px;
        background-color: #f0f2f6; /* Un fondo sutil */
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
        transition: 0.3s;
    }
    .img-container:hover {
        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.3);
        transform: scale(1.03); /* Efecto de zoom al pasar el ratón */
    }
    /* Estilo para las imágenes dentro del contenedor */
    .img-container img {
        width: 100%;
        border-radius: 5px;
    }
    /* Estilo para los títulos de las obras */
    .work-title {
        font-size: 1.2em;
        font-weight: bold;
        color: #333;
        margin-top: 10px;
    }
    /* Estilo para el autor */
    .work-author {
        font-style: italic;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)


# --- CREAR LA GALERÍA CON COLUMNAS ---
# Definimos cuántas columnas queremos
num_columnas = 3
cols = st.columns(num_columnas)

# Iteramos sobre las obras y las asignamos a una columna
for i, obra in enumerate(obras):
    col = cols[i % num_columnas]
    with col:
        # Usamos st.markdown para poder aplicar nuestras clases de CSS
        st.markdown(f"""
        <div class="img-container">
            <img src="{obra['img']}" alt="{obra['titulo']}">
            <p class="work-title">{obra['titulo']}</p>
            <p class="work-author">{obra['autor']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # --- INTERACTIVIDAD: EL EXPANSOR ---
        # Un botón para ver más detalles sin saturar la pantalla
        with st.expander("Ver más detalles..."):
            st.write(obra['desc'])

st.markdown("---")
st.write("Creado con mucho esfuerzo y un poco de ayuda.")
