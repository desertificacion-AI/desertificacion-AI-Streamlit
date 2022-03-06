import matplotlib.pyplot as plt
import numpy as np
import random
import skimage.io as skio
import streamlit as st

from PIL import Image
from rasterio import plot
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Image.MAX_IMAGE_PIXELS = None

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
        * matplotlib &emsp; 3.5.1
        * numpy &emsp; &emsp; 1.22.2
        * PIL &emsp; &emsp; &emsp; &ensp; 9.0.1
        * rasterio &emsp; &emsp; 1.2.10
        * scikit-image &ensp; 0.19.2
        * scikit-learn &emsp; 1.0.2
        * streamlit &emsp; &ensp; 1.5.1
    """)

# Imágenes satelitales
# ====================

@st.cache
def lee_imagenes():
    img_name_1 = 'imagen_1.tif'
    img_name_2 = 'imagen_2.tif'
    img_name_3 = 'imagen_3.tif'
    img_name_4 = 'imagen_4.tif'
    img_name_5 = 'imagen_5.tif'
    img_name_6 = 'imagen_6.tif'

    img1 = skio.imread(img_name_1, plugin='pil')
    img2 = skio.imread(img_name_2, plugin='pil')
    img3 = skio.imread(img_name_3, plugin='pil')
    img4 = skio.imread(img_name_4, plugin='pil')
    img5 = skio.imread(img_name_5, plugin='pil')
    img6 = skio.imread(img_name_6, plugin='pil')

    return img1, img2, img3, img4, img5, img6

img1 = lee_imagenes()[0]
img2 = lee_imagenes()[1]
img3 = lee_imagenes()[2]
img4 = lee_imagenes()[3]
img5 = lee_imagenes()[4]
img6 = lee_imagenes()[5]

# @st.cache
def muestra_imagenes():
    st.markdown('---')
    st.subheader('Imágenes satelitales')

    col11, col12 = st.columns(2)
    with col11:
        st.write('1 - 20210316 - Tamaño:', img1.shape)
        st.image(img1, width=350, clamp=True)
    with col12:
        st.write('2 - 20210405 - Tamaño:', img1.shape)
        st.image(img2, width=350, clamp=True)

    col21, col22 = st.columns(2)
    with col21:
        st.write('3 - 20210505 - Tamaño:', img1.shape)
        st.image(img3, width=350, clamp=True)
    with col22:
        st.write('4 - 20210525 - Tamaño:', img1.shape)
        st.image(img4, width=350, clamp=True)

    col31, col32 = st.columns(2)
    with col31:
        st.write('5 - 20210614 - Tamaño:', img1.shape)
        st.image(img5, width=350, clamp=True)
    with col32:
        st.write('6 - 20210624 - Tamaño:', img1.shape)
        st.image(img6, width=350, clamp=True)

muestra_imagenes()

# Banda lateral
# =============

st.sidebar.markdown('# Cuadrícula de estudio')
st.sidebar.markdown("""
Cuadrícula de estudio dentro de la imagen, con un ancho y un alto en píxeles según lo indicado.

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
# coord_x = st.sidebar.slider('Coordenada x.0', y0, y1)
# coord_y = st.sidebar.slider('Coordenada y.0', x0, x1)

a0 = 1
a1 = 250
ancho = st.sidebar.slider('Ancho/Alto de la cuadrícula', a0, a1)

if coord_x + ancho > x1:
    coord_x = x1 - ancho
    xn = x1
else:
    xn = coord_x + ancho

if coord_y + ancho > y1:
    coord_y = y1 - ancho
    yn = y1
else:
    yn = coord_y + ancho

# st.sidebar.write('x0', coord_x)
# st.sidebar.write('y0', coord_y)
# st.sidebar.write('xn', xn)
# st.sidebar.write('yn', yn)
# st.sidebar.write('ancho', ancho)
# st.sidebar.write('x1', x1)
# st.sidebar.write('y1', y1)

# Cuadrículas
# ===========

st.markdown('---')
st.subheader('Cuadriculas de estudio e índice de vegetación NDVI')

x0 = coord_x
y0 = coord_y

st.markdown(f'Coordenadas de la esquina superior izquierda: &emsp; $x_0$ * $y_0$ = {x0} * {y0} px')
st.markdown(f'Coordenadas de la esquina superior derecha: &emsp; $x_n$ * $y_n$ = {xn} * {yn} px')

cuadrícula1 = img1[y0:yn, x0:xn]
cuadrícula2 = img2[y0:yn, x0:xn]
cuadrícula3 = img3[y0:yn, x0:xn]
cuadrícula4 = img4[y0:yn, x0:xn]
cuadrícula5 = img5[y0:yn, x0:xn]
cuadrícula6 = img6[y0:yn, x0:xn]
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
    st.markdown(f'')
    st.markdown(f'##### Cuadrícula {i}')
    st.image(cuadricula, width=400, clamp=True)

    st.text('Valor NDVI de cada píxel de la cuadrícula:')
    np_data = np.asarray(cuadricula)
    st.write(np.round(np_data, 3))

    np_data_mean = np_data.mean()
    st.markdown(f'##### Valor promedio NDVI del conjunto de píxeles de la cuadrícula: &emsp; {np_data_mean:.3f}')

    zona = zona_ndvi(np_data_mean)
    st.markdown(f'##### Interpretación del valor promedio NDVI de la cuadrícula {i} &ensp; → &ensp; {zona}')

# Random Forest
# =============

st.markdown('---')
st.subheader('Predicción de la IA')
st.markdown(
    """
    El sistema se entrena con una porción igual de cada una de las imágenes 1 a 5. Esta porción es un recuadro de \
    coordenadas aleatorias y dimensiones igual al ancho/alto de la cuadrícula indicado en la banda lateral.
    
    La razón de elegir un recuadro reducido es el elevado coste computacional que tiene el entrenamiento del sistema. \
    De esta forma la aplicación puede mostrar unos resultados de una forma relativamente ágil.
    
    Para el test se ha elegido las imágenes de las cuadrículas 1 a 5 con las que se ha obtenido el índice NDVI.
    
    La predicción se hace con la cuadrícula 6. Se compara la imagen original con la predicha por la IA.
    """
)

# Imágenes de entrenamiento
# -------------------------
numpydata1 = np.asarray(img1)
numpydata2 = np.asarray(img2)
numpydata3 = np.asarray(img3)
numpydata4 = np.asarray(img4)
numpydata5 = np.asarray(img5)

# Imágenes para test
# ------------------
numpydata6 = np.asarray(img6)

X = []
y = []

dim = ancho
i0 = random.randint(0, x1 - dim)  # Mitad izquierda de la imagen
j0 = random.randint(0, y1 - dim)
ik = i0 + dim - 2
jk = j0 + dim - 2

for i in range(i0, ik):
    for j in range(j0, jk):
        X.append(
            [
                numpydata1[i, j], numpydata1[i, j + 1], numpydata1[i, j + 2],
                numpydata1[i + 1, j], numpydata1[i + 1, j + 1], numpydata1[i + 1, j + 2],
                numpydata1[i + 2, j], numpydata1[i + 2, j + 1], numpydata1[i + 2, j + 2],
                numpydata2[i, j], numpydata2[i, j + 1], numpydata2[i, j + 2],
                numpydata2[i + 1, j], numpydata2[i + 1, j + 1], numpydata2[i + 1, j + 2],
                numpydata2[i + 2, j], numpydata2[i + 2, j + 1], numpydata2[i + 2, j + 2],
                numpydata3[i, j], numpydata3[i, j + 1], numpydata3[i, j + 2],
                numpydata3[i + 1, j], numpydata3[i + 1, j + 1], numpydata3[i + 1, j + 2],
                numpydata3[i + 2, j], numpydata3[i + 2, j + 1], numpydata3[i + 2, j + 2],
                numpydata4[i, j], numpydata4[i, j + 1], numpydata4[i, j + 2],
                numpydata4[i + 1, j], numpydata4[i + 1, j + 1], numpydata4[i + 1, j + 2],
                numpydata4[i + 2, j], numpydata4[i + 2, j + 1], numpydata4[i + 2, j + 2],
                numpydata5[i, j], numpydata5[i, j + 1], numpydata5[i, j + 2],
                numpydata5[i + 1, j], numpydata5[i + 1, j + 1], numpydata5[i + 1, j + 2],
                numpydata5[i + 2, j], numpydata5[i + 2, j + 1], numpydata5[i + 2, j + 2]
            ]
        )
        y.append(numpydata6[i + 1, j + 1])

# Clasificador
# ------------

cls = RandomForestRegressor()

# Entrenamiento
# -------------

cls.fit(X, y)

A = []
b = []

i0 = x0
j0 = y0
ik = i0 + dim
jk = j0 + dim

for i in range(j0, jk):
    for j in range(i0, ik):
        A.append(
            [
                numpydata1[i, j], numpydata1[i, j + 1], numpydata1[i, j + 2],
                numpydata1[i + 1, j], numpydata1[i + 1, j + 1], numpydata1[i + 1, j + 2],
                numpydata1[i + 2, j], numpydata1[i + 2, j + 1], numpydata1[i + 2, j + 2],
                numpydata2[i, j], numpydata2[i, j + 1], numpydata2[i, j + 2],
                numpydata2[i + 1, j], numpydata2[i + 1, j + 1], numpydata2[i + 1, j + 2],
                numpydata2[i + 2, j], numpydata2[i + 2, j + 1], numpydata2[i + 2, j + 2],
                numpydata3[i, j], numpydata3[i, j + 1], numpydata3[i, j + 2],
                numpydata3[i + 1, j], numpydata3[i + 1, j + 1], numpydata3[i + 1, j + 2],
                numpydata3[i + 2, j], numpydata3[i + 2, j + 1], numpydata3[i + 2, j + 2],
                numpydata4[i, j], numpydata4[i, j + 1], numpydata4[i, j + 2],
                numpydata4[i + 1, j], numpydata4[i + 1, j + 1], numpydata4[i + 1, j + 2],
                numpydata4[i + 2, j], numpydata4[i + 2, j + 1], numpydata4[i + 2, j + 2],
                numpydata5[i, j], numpydata5[i, j + 1], numpydata5[i, j + 2],
                numpydata5[i + 1, j], numpydata5[i + 1, j + 1], numpydata5[i + 1, j + 2],
                numpydata5[i + 2, j], numpydata5[i + 2, j + 1], numpydata5[i + 2, j + 2]
            ]
        )
        b.append(numpydata6[i + 1, j + 1])

b_predicho = cls.predict(A)
mse = mean_squared_error(b, b_predicho)

# Plot
# ----

tfreal = b
tfpredicho = b_predicho.tolist()

anp=np.array(tfpredicho)
anp=np.reshape(anp, (ik - i0, jk - j0))
org=np.array(tfreal)
org=np.reshape(org, (ik - i0, jk - j0))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
ax1.imshow(org.astype(np.float64), interpolation='nearest')
ax2.imshow(anp.astype(np.float64), interpolation='nearest')
ax1.set_title('Imagen original')
ax2.set_title('Imagen predicha por la IA')
st.pyplot(fig)

st.markdown(f'Coordenadas de la esquina superior izquierda: &emsp; $i_0$ * $j_0$ = {i0} * {j0} px')
st.markdown(f'Coordenadas de la esquina superior derecha: &emsp; $i_n$ * $j_n$ = {ik} * {jk} px')

st.markdown(f'##### Error cuadrático promedio: &emsp; {mse:.5f}')

# Créditos
# ========

st.markdown('---')
with st.expander('Créditos'):
    st.markdown(
        """
        06/03/2022
        
        Autores:
        
        * [Eva de Miguel](https://www.linkedin.com/in/eva-de-miguel-morales-a63938a0/)
        * [Pedro Biel](www.linkedin.com/in/pedrobiel)
        * [Yinet Castiblanco](https://www.linkedin.com/in/yinethcastiblancorojas/)
        
        ---
        
        * **Artículo Medium** [Medium](https://medium.com/saturdays-ai/predicci%C3%B3n-de-zonas-de-desertificaci%C3%B3n-en-arag%C3%B3n-usando-ia-ee59c15c12a5)
        * **Código fuente:** [GitHub](https://github.com/desertificacion-AI/desertificacion-AI)
        """
    )
