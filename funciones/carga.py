import pandas as pd
import streamlit as st

def leer_excel(archivo):
    df = pd.read_excel(archivo)

    columnas_necesarias = [
        "Sexo",
        "Estatura (m)",
        "IMC",
        "Presión arterial",
        "Peso (kg)",
        "Horas de trabajo/día",
        "Trabajo"
    ]

    faltantes = [col for col in columnas_necesarias if col not in df.columns]
    if faltantes:
        st.error("Faltan estas columnas en el archivo: " + ", ".join(faltantes))
        st.stop()

    return df
