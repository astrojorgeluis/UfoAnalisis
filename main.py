import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import time

# Titutlo de la pagina para la pestaña
st.set_page_config(
    page_title="Avistamientos OVNI",
    page_icon="💻",
)

# Contador Previo de la pagina
with st.spinner("Encendiendo detector de UFOs"):
    time.sleep(2)
with st.spinner("Analizando el cielo..."):
    time.sleep(3)
with st.spinner("Alien encontrado!"):
    time.sleep(2)
with st.spinner("Actualizando registro..."):
    time.sleep(2)
with st.spinner("Mostrando resultados..."):
    time.sleep(2)


# Ventanas disponibles
tab1, tab2, tab3, tab4 = st.tabs(["/ inicio", "/ análisis de los datos","/ conclusión de los datos","/ acerca del proyecto"])

with tab1:
    # Home - Titulo de la pagina
    st.subheader('[ registra tu OVNI ]', divider='gray')

    col1, col2 = st.columns(2)

    with col2:
        # Cuerpo del home  
        intro_text = """En esta página podrás visualizar los datos de avistamientos de OVINIs (Objetos Voladores No Identificados), entre 1910 y 2014. Éste dataset cuenta de cerca de 80.000 registros de testimonios de posibles avistamientos de estos. Los también llamados UFOS por sus siglas en inglés (Unidentified Flying Object), son elementos que pueden volar (o que puede parecer que lo hacen), cuyo origen desconocido. De hecho, los OVNIs son aquellos elementos que no pueden ser catalogados como vehículos, componentes o sujetos conocidos por el ser humano. A lo largo de la historia, se han informado avistamientos de luces y objetos en el cielo con características que desafían las explicaciones convencionales. Aunque algunos avistamientos de OVNIs pueden ser atribuidos a aeronaves militares, globos meteorológicos o errores de identificación, otros permanecen sin explicación clara. La posibilidad de vida extraterrestre ha sido una de las explicaciones no convencionales más populares para estos misteriosos elementos voladores, nos da paso a pensar si vida inteligente de otros lugares de la galaxia encontró nuestro pequeño hogar en la Vía Láctea; ¿Nos vigilan?, ¿Viven entre nosotros y lo que vemos es su despedida de nuestro sistema solar?, probablemente la respuesta a estas y muchas más preguntas al respecto nunca la tendremos…"""

        st.write(f'<p style="color:#9c9d9f; text-align: justify;">{intro_text}</p>',unsafe_allow_html=True)


    with col1:
        # Imagen
        st.image("ufo.jpg")
        st.caption(
            "Fotografia referencial.", unsafe_allow_html=True)
        
        st.subheader("[ objetivo ]", divider='gray')
        subintro_text = """El objetivo principal de nuestro proyecto es desarrollar un programa avanzado capaz de analizar y visualizar los datos recopilados, en éste caso en un dataset de avistamientos de OVNIs. El propósito fundamental es facilitar la comprensión de los datos de avistamientos de OVNIs, facilitando obtener datos concluyentes, y así contribuyendo al entendimiento de este fenómeno."""

        st.write(f'<p style="color:#9c9d9f; text-align: justify;">{subintro_text}</p>',unsafe_allow_html=True)

        st.subheader("[ github ]", divider='gray')
        st.write(
        '<p style="color:#9c9d9f; text-align: justify;"">El código de este proyecto es abierto, si quieres puedes chequearlo en <a href="https://github.com/astrojorgeluis/UfoAnalisis" style="color: #20C20E;">este link</a>.</p><br>',
        unsafe_allow_html=True,)


with tab2:
    
    # Leer el archivo CSV
    df = pd.read_csv("data.csv")

    # Limpieza de datos
    columnas_a_rellenar = ['city', 'state', 'country', 'shape', 'duration (seconds)', 'duration (hours/min)', 'comments', 'date posted']
    df.rename(columns={'longitude ': 'longitude'}, inplace=True)
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df[columnas_a_rellenar] = df[columnas_a_rellenar].fillna('unknown')
    df = df.dropna(subset=["latitude", "longitude"])
    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
    df.dropna(subset=['datetime'], inplace=True)

    col1, col2, col3 = st.columns(3)

    # Arreglar los datos
    ultima_fecha = df['datetime'].max()
    arreglada_ultima_fecha = ultima_fecha.strftime('%d %b %Y')
    forma_comun = df['shape'].mode().iloc[0]
    total_datos = df.shape[0]

    with col1:
        st.markdown(f"<span style='font-size: 1.8vh;'>[ forma mas comun ]<br></span> <span style='font-size: 3.4vh; color: white'>{forma_comun}</span>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<span style='font-size: 1.8vh;'>[ ultimo registro ]<br></span> <span style='font-size: 3.4vh; color: white'>{arreglada_ultima_fecha}</span>", unsafe_allow_html=True)

    with col3:
        st.markdown(f"<span style='font-size: 1.8vh;'>[ total de registros ]<br></span> <span style='font-size: 3.4vh; color: white'>{total_datos}</span>", unsafe_allow_html=True)

    # Mostrar DF
    df

    # Gráfico de barras
    st.subheader('[ tipo de avistamiento más común ]', divider='gray')
    bars = alt.Chart(df).mark_bar().encode(
        x='shape:N',
        color=alt.Color('count():Q', scale=alt.Scale(scheme='darkgreen')),
        y='count():Q'
    ).properties(
        width=800,
        height=400
    )
    st.altair_chart(bars)

    # Gráfico de dispersión
    st.subheader('[ cantidad de avistamientos en el tiempo ]', divider='gray')
    df['year_month'] = df['datetime'].dt.to_period('M')
    df['year_month'] = pd.to_datetime(df['year_month'].astype(str))
    cuenta_por_mes = df.groupby('year_month').size().reset_index(name='count')

    base = alt.Chart(cuenta_por_mes).mark_circle(opacity=0.5, size=30, color='#16D916').encode(
        x=alt.X('year_month:T', axis=alt.Axis(title='Año y Mes', format='%Y-%m', tickCount=10)),
        y='count:Q',
        tooltip=['year_month:T', 'count:Q']
    )
    linea = base.transform_loess('year_month', 'count', bandwidth=0.04).mark_line(size=3, color='white')
    st.altair_chart(base + linea, use_container_width=True)

    # Mapa
    st.subheader('[ avistamientos por el mundo ]', divider='gray')
    df["longitude "] = df["longitude"].astype(float) 
    df["latitude"] = df["latitude"].astype(float)
    st.map(df, use_container_width=True, zoom=1.5, color="#00FF00B3")
    st.caption(
    '<p style="color: #9c9d9f;">Nota: A veces la visualizacion no es correcta. El error se soluciona abriendo el mapa en pantalla completa. Luego de esto, ya estará en correcto funcionamiento.</p>',
    unsafe_allow_html=True,
    )

   # Testimonios
    st.subheader('[ testimonios ]', divider='gray')
    ciudad = sorted(df['city'].unique())
    selec_ciudad = st.selectbox("Seleccionar localidad", [""] + ciudad)
    testimonio_ciudad = df.loc[df['city'] == selec_ciudad]
    st.write(f'<span style="color: #9c9d9f;">Número de avistamientos: {testimonio_ciudad.shape[0]}</span>', unsafe_allow_html=True)    

    if selec_ciudad:
        st.write("---------")
        for indice, columna in testimonio_ciudad.iterrows():
            st.write(f"<p style='color: white;'>Fecha: {columna['datetime']}, Localidad: {columna['city']}, Forma: {columna['shape']}</p>", unsafe_allow_html=True)
            st.write(f"<p style='color: white;'>Descripcion: {columna['comments']}</p>", unsafe_allow_html=True)
            st.write("---------")
    else:
        st.write(f'<span style="color: red;">ERROR - No se ha seleccionado ninguna ciudad.</span>', unsafe_allow_html=True)    



with tab3:

    st.subheader('[ síntesis general de los datos ]', divider='gray')
        
    pais = df['country'].mode().iloc[0]
    ciudad = df['city'].mode().iloc[0]

    df['duration (hours/min)'] = pd.to_numeric(df['duration (hours/min)'], errors='coerce')
    duracion_prom = round(df['duration (hours/min)'].mean(), 1)
        
    mas_avistamientos = df['datetime'].dt.date.value_counts().idxmax()

    Conclusion1 = f"""El tipo de avistamiento más común es una Luz<br>
                    País con más avistamientos registrados es {pais} (Estados Unidos).<br>
                    Ciudad con más avistamientos registrados es {ciudad}.<br>
                    Duración promedio de un avistamiento es {duracion_prom} horas.<br>
                    Día con más avistamientos registrados fue el {mas_avistamientos}.<br>"""

    st.write(f'<p style="color:#9c9d9f; text-align: justify;">{Conclusion1}</p>', unsafe_allow_html=True)

    st.subheader('[ conclusión general como grupo ]', divider='gray')

    Conclusion2 = """Creemos que el incremento de los avistamientos en nuestros años de registros (1910-2014) se deben al desarrollo tecnológico, específicamente de herramientas visuales (cámaras, videograbadoras, etc.), ya que gran parte de los eventos registrados son accidentales y reconocidos mediante fotos o videos, donde se aprecia un elemento inusual en el cielo; además a lo largo de los años se masificado la posesión de cámaras y otros objetos tecnológicos que las posean. Bajo esta idea en nuestra opinión los registros de UFOs deberían disminuir, en torno a la mejora en la resolución de estas herramientas visuales, ya que se podrá apreciar con mayor claridad si estas dejaron registro de un verdadero OVNI."""

    st.write(f'<p style="color:#9c9d9f; text-align: justify;">{Conclusion2}</p>', unsafe_allow_html=True)


with tab4:

    st.subheader('[ descripción del proyecto ]', divider='gray')
        
    AcercaDe = """Éste proyecto fue desarrollado como parte de la evaluación final de la asignatura de Física Computacional 2 de la carrera de Astrofísica con Mención en Ciencia de Datos (USACH). Bajo el objetivo aplicar conocimientos adquiridos en programación (leguaje Python) sobre la limpieza, análisis y visualización de datos."""

    st.write(f'<p style="color:#9c9d9f; text-align: justify;">{AcercaDe}</p>', unsafe_allow_html=True)

    st.subheader('[ creadores ]', divider='gray')
        
    Amanda = """
    Amanda Achterberg<br>
    amanda.achterberg@usach.cl<br>  
    Estudiante de Astrofísica
    """

    Jorge = """
    Jorge Luis Guzman<br>  
    jorge.guzman.l@usach.cl<br>  
    Estudiante de Astrofísica
    """

    st.write(f'<p style="color:#ffffff; text-align: left;">{Amanda}</p>', unsafe_allow_html=True)
    st.write(f'<p style="color:#ffffff; text-align: left;">{Jorge}</p>', unsafe_allow_html=True)