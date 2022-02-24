from PIL import Image
import numpy as np
import skimage.io as skio
import streamlit as st

st.set_page_config(
    page_title='Aplicación megachula',
    page_icon=':cactus:',
    layout='centered'
)

# Título
# ======

image = Image.open('desertIAragón.png')
st.image(image, width=700)

st.title('Desertificación en Aragón')
st.subheader('AI Saturdays - I Edición Zaragoza - CURSO BÁSICO DE IA')
st.markdown('*Añadir enlace a artículo **Medium***')

# Librerías
# =========

st.markdown('---')
with st.expander('Librerías'):
    st.markdown("""
        * numpy
        * PIL
        * skimage
        * streamlit
    """)

# ¿Mostrar imágenes satelitales?
# ==============================

# Sidebar
# -------

mostrar = st.sidebar.checkbox('¿Mostrar imágenes satelitales?')

# Imágenes
# ======

# Imágenes

img_name_1 = './sources/T31TBG_20210316T105031_B_NDVI.tif'
img_name_2 = './sources/T31TBG_20210405T105021_B_NDVI.tif'
img_name_3 = './sources/T31TBG_20210505T105031_B_NDVI.tif'
img_name_4 = './sources/T31TBG_20210525T105031_B_NDVI.tif'
img_name_5 = './sources/T31TBG_20210614T105031_B_NDVI.tif'
img_name_6 = './sources/T31TBG_20210624T105031_B_NDVI.tif'

img1 = skio.imread(img_name_1, plugin='pil')
img2 = skio.imread(img_name_2, plugin='pil')
img3 = skio.imread(img_name_3, plugin='pil')
img4 = skio.imread(img_name_4, plugin='pil')
img5 = skio.imread(img_name_5, plugin='pil')
img6 = skio.imread(img_name_6, plugin='pil')

if mostrar:
    st.markdown('---')
    st.subheader('Imágenes satelitales')

    col11, col12 = st.columns(2)
    with col11:
        st.write('1 - 20210316 - Tamaño:', img1.shape)
        st.image(img1, width=300, clamp=True)
    with col12:
        st.write('2 - 20210405 - Tamaño:', img1.shape)
        st.image(img2, width=300, clamp=True)

    col21, col22 = st.columns(2)
    with col21:
        st.write('3 - 20210505 - Tamaño:', img1.shape)
        st.image(img3, width=300, clamp=True)
    with col22:
        st.write('4 - 20210525 - Tamaño:', img1.shape)
        st.image(img4, width=300, clamp=True)

    col31, col32 = st.columns(2)
    with col31:
        st.write('5 - 20210614 - Tamaño:', img1.shape)
        st.image(img3, width=300, clamp=True)
    with col32:
        st.write('6 - 20210624 - Tamaño:', img1.shape)
        st.image(img4, width=300, clamp=True)

# Banda lateral
# =============

st.sidebar.markdown('# Cuadrícula de estudio')
st.sidebar.markdown("""
Caudrícula de estudio dentro de la imagen, con un ancho y un alto en píxeles según lo indicado.

La esquina superior izquierda de la cuadrícula se determinará con las coodenadas $x_0$ e $y_0$.
"""
)

# Sidebar
# -------

x0 = 0
x1 = min(img1.shape[1], img2.shape[1], img3.shape[1], img4.shape[1], img5.shape[1], img6.shape[1])
y0 = 0
y1 = min(img1.shape[0], img2.shape[0], img3.shape[0], img4.shape[0], img5.shape[0], img6.shape[0])

coord_x = st.sidebar.slider('Coordenada x.0', x0, x1)
coord_y = st.sidebar.slider('Coordenada y.0', y0, y1)

a0 = 1
# a1 = min(x1, y1)
a1 = 1000
ancho = st.sidebar.slider('Ancho/Alto de la cuadrícula', a0, a1)

if coord_x + ancho > x1:
    coord_x = x1 - ancho
    xn = ancho
else:
    xn = coord_x + ancho

if coord_y + ancho > y1:
    coord_y = y1 - ancho
    yn = ancho
else:
    yn = coord_y + ancho

# TODO se produce un error en los límites

st.sidebar.write('x0', coord_x)
st.sidebar.write('y0', coord_y)
st.sidebar.write('xn', xn)
st.sidebar.write('yn', yn)
st.sidebar.write('ancho', ancho)

# Cuadrículas
# ===========

st.markdown('---')
st.subheader('Cuadriculas de estudio')

x0 = coord_x
y0 = coord_y

st.write('Coordenadas:  x.0 =', x0, ';  y.0 =', y0)
st.write('Tamaño de la cuadrícula:', ancho,'*', ancho, 'px')

cuadrícula1 = img1[x0:xn, y0:yn]
cuadrícula2 = img2[x0:xn, y0:yn]
cuadrícula3 = img3[x0:xn, y0:yn]
cuadrícula4 = img4[x0:xn, y0:yn]
cuadrícula5 = img5[x0:xn, y0:yn]
cuadrícula6 = img6[x0:xn, y0:yn]
cuadriculas = (cuadrícula1, cuadrícula2, cuadrícula3, cuadrícula4, cuadrícula5, cuadrícula6)

def zona_ndvi(ndvi):
    """Zona de representación según el rango."""
    if ndvi < 0:
        return 'Zona sin vegetación'
    elif ndvi > 0.3:
        return 'Zona con vegetación'
    else:
        return 'Zona con algo de vegetación'

i = 0
for cuadricula in cuadriculas:
    i += 1
    st.text(str(i))
    st.image(cuadricula, width=300, clamp=True)

    st.text('Valor NDVI de cada píxel de la cuadrícula')
    np_data = np.asarray(cuadrícula1)
    st.write(np_data)

    st.text('Valor promedio NDVI del conjunto de píxeles de la cuadrícula')
    np_data_mean = np_data.mean()
    st.write(np_data_mean)

    zona = zona_ndvi(np_data_mean)
    st.write('Interpretación del valor NDVI de la cuadrícula', i, '->', zona)

# Créditos
# ========

st.markdown('---')
with st.expander('Créditos'):
    st.markdown("""
        24/02/2022

        * Pedro Biel
        * Yinet Castiblanco
        * Eva de Miguel

        * **Código fuente:** [GitHub](https://github.com/desertificacion-AI/desertificacion-AI).
    """)
