import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Aplicación megachula',
    page_icon='⚡',
    layout='centered'
)

# Título
# ======

st.title('Mis pruebas con streamlit')
st.subheader('AI Saturdays - I Edición Zaragoza - CURSO BÁSICO DE IA')
st.markdown("""
#### Pruebas con `streamlit` para el proyecto **Desertificación Aragón**
""")

# Banda lateral
# =============

st.sidebar.header('Banda lateral')

uploaded_img = st.sidebar.file_uploader('Arrastra aquí la imagen')

# Imagen
# ======

st.markdown('---')
st.subheader('Leyendo la imagen directamente desde el archivo')

code = """
image_name = 'LC08_L1TP_199031_20220117_20220123_02_T1_ndvi_M_[-5.3173828125,39.72831341029745,3.8232421875000004,42.879989517714826].tiff'
image = Image.open(image_name)
st.image(image, width=800)
"""
st.code(code, language='python')

image_name = 'LC08_L1TP_199031_20220117_20220123_02_T1_ndvi_M_[-5.3173828125,39.72831341029745,3.8232421875000004,42.879989517714826].tiff'
image = Image.open(image_name)
st.image(image, width=800)

st.markdown('---')
st.subheader('Arrastrando la imagen en la banda lateral')

code = """
uploaded_img = st.sidebar.file_uploader('Arrastra aquí la imagen')
try:
    image_name = uploaded_img
    image = Image.open(image_name)
    st.image(image, width=800)
except:
    pass
"""
st.code(code, language='python')

try:
    image_name = uploaded_img
    image = Image.open(image_name)
    st.image(image, width=800)
except:
    pass

# Créditos
with st.expander('Créditos'):
    st.markdown("""
        * Pedro Biel
        * Yinet Castiblanco
        * Eva de Miguel
        
        * **Código fuente:** [GitHub](https://github.com/desertificacion-AI/desertificacion-AI).
    """)
