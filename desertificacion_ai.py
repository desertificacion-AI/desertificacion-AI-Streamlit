import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Aplicación megachula',
    page_icon=':cactus:',
    layout='centered'
)

# Título
# ======

st.title('Desertificación en Aragón')
st.subheader('AI Saturdays - I Edición Zaragoza - CURSO BÁSICO DE IA')
st.markdown('''### Descripción del problema''')
st.markdown('''
La desertificación se produce por la degradación de la tierra que se da en zonas secas: áridas, semiáridas y \
subhúmedas secas. La actividad humana y las variaciones climáticas están entre las causas de esta degradación del \
suelo, que impacta en los ecosistemas y en los recursos y modos de vida de los habitantes de las zonas afectadas. \
Estas zonas secas son aquellas con un índice de aridez (IA=P/ETP) inferior a 0,65.
España es uno de los territorios que sufre esta problemática.

En Aragón el 75% del territorio está en riesgo de desertización. El cambio climático y la subida de las temperaturas \
amenazan las tierras semiáridas que predominan en el Valle del Ebro, las zonas secas antes mencionadas son justamente \
las que se dan en el valle del Ebro, desde la ciudad de Huesca hacia el sur.

Para poder identificar estas zonas se propone un proceso que gestione el reconocimiento por imágenes de la \
desertificación en Aragón con el objetivo de aplicar políticas más eficientes referentes a la reforestación de las \
zonas afectadas, y nuevos tratamientos de cultivos.
''')
st.markdown('''### Descripción del problema''')
st.markdown('''
El objetivo de la aplicación en una primera instancia pasa por, dada una imagen de la zona recogida de satelite poder \
comparar la evolucion en el tiempo con respecto a la desertificación *y en una segunda instancia poder \
desarrollar un modelo que regrese la probabilidad de desertizacion en un area dada*.
''')

# Banda lateral
# =============

st.sidebar.header('Banda lateral')
st.sidebar.text('Aquí se pueden poner algunos widgets')

# Imagen
# ======

st.markdown('---')
st.subheader('Imagen geoespacial')

# Imagen de prueba
image_name = 'LC08_L1TP_199031_20220117_20220123_02_T1_ndvi_M_[-5.3173828125,39.72831341029745,3.8232421875000004,42.879989517714826].tiff'
image = Image.open(image_name)
st.image(image, width=800)

# Librerías
# =========

with st.expander('Librerías'):
    st.markdown("""
        PIL
        streamlit
        ...
    """)

# Créditos
# ========

with st.expander('Créditos'):
    st.markdown("""
        13/02/2022
        
        * Pedro Biel
        * Yinet Castiblanco
        * Eva de Miguel
        
        * **Código fuente:** [GitHub](https://github.com/desertificacion-AI/desertificacion-AI).
    """)
