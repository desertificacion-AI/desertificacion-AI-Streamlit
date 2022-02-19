import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Aplicación megachula',
    page_icon=':cactus:',
    layout='centered'
)

# Título
# ======

image = Image.open('desertIAragón.png')
st.image(image, width=800)

st.title('Desertificación en Aragón')
st.subheader('AI Saturdays - I Edición Zaragoza - CURSO BÁSICO DE IA')
st.markdown('''#### Descripción del problema''')
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
st.markdown('''#### Objetivo de la aplicación''')
st.markdown('''
El objetivo de la aplicación en una primera instancia pasa por, dada una imagen de la zona recogida de satelite poder \
comparar la evolucion en el tiempo con respecto a la desertificación *y en una segunda instancia poder \
desarrollar un modelo que regrese la probabilidad de desertizacion en un area dada*.
''')

# Librerías
# =========

st.markdown('---')
with st.expander('Librerías'):
    st.markdown("""
        * PIL
        * streamlit
        * ...
    """)

# Imagen
# ======

st.markdown('---')
st.subheader('Imagen geoespacial')

# Imagen de prueba
img_name = 'LC08_L1TP_199031_20220117_20220123_02_T1_ndvi_M_[-5.3173828125,39.72831341029745,3.8232421875000004,42.879989517714826].tiff'
img = Image.open(img_name)
st.image(img, width=800)

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

# import numpy as np
# data = np.zeros( (512,512,3), dtype=np.uint8)
# data[256,256] = [255,0,0]
#
# from matplotlib import pyplot as plt
# fig, ax = plt.subplots()
# ax.imshow(data, interpolation='nearest')
# st.pyplot(fig)

# Banda lateral
# =============

st.sidebar.header('Selección del pixel de estudio')

import skimage.io as skio
img1 = skio.imread(img_name, plugin='tifffile')
# st.sidebar.image(img1, width=200)
st.sidebar.write(img1.shape)
x0 = 1
x1 = img1.shape[0]
y0 = 1
y1 = img1.shape[1]
# st.sidebar.write(x0, x1, y0, y1)

coord_x = st.sidebar.slider('Coordenada x', x0, x1)
coord_y = st.sidebar.slider('Coordenada y', y0, y1)

a0 = 1
a1 = min(x1, y1)
ancho = st.sidebar.slider('Ancho de la cuadrícula', a0, a1)

st.sidebar.markdown('El pixel se encuentra en el centro de la cuadrícula')

f0 = coord_x - int(0.5 * ancho)
if f0 < y0:
    f0 = y0

f1 = coord_x + int(0.5 * ancho)
if f1 > y1:
    f1 = y1

if f1 <= f0:
    f1 = f0 + 1

c0 = coord_y - int(0.5 * ancho)
if c0 < x0:
    c0 = x0

c1 = coord_y + int(0.5 * ancho)
if c1 > x1:
    c1 = x1

if c1 <= c0:
    c1 = c0 + 1

st.sidebar.write(f0, f1, c0, c1)

cuadrícula = img1[f0:f1, c0:c1]
st.sidebar.image(cuadrícula, width=200)






