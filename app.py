import streamlit as st
from funciones import carga, limpieza, estadisticas

st.set_page_config(page_title="Laboratorio de Estadística", layout="wide")
st.title("Laboratorio de Estadística Inferencial")

archivo = st.file_uploader("Seleccione el archivo Excel (.xlsx)", type=["xlsx"])
if archivo is None:
    st.info("Suba el archivo Base_datos_muestra_40_personas.xlsx para comenzar.")
    st.stop()

df = carga.leer_excel(archivo)
df = limpieza.preparar_variables(df)

with st.expander("Ver base de datos"):
    st.dataframe(df, use_container_width=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Promedios", "Hipertensión", "Sobrepeso", "Intervalo de confianza", "Prueba de hipótesis"
])

with tab1:
    estadisticas.mostrar_promedios(df)

with tab2:
    estadisticas.mostrar_hipertension(df)

with tab3:
    estadisticas.mostrar_sobrepeso(df)

with tab4:
    estadisticas.mostrar_intervalo_confianza(df)

with tab5:
    estadisticas.mostrar_prueba_hipotesis(df)