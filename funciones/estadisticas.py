import math
import streamlit as st
import pandas as pd
from scipy import stats


# A y B. Promedios
def mostrar_promedios(df):
    st.header("Promedios generales y por sexo")

    altura_general = df["Estatura (m)"].mean()
    altura_hombres = df.loc[df["Sexo"] == "M", "Estatura (m)"].mean()
    altura_mujeres = df.loc[df["Sexo"] == "F", "Estatura (m)"].mean()

    peso_general = df["Peso (kg)"].mean()
    peso_hombres = df.loc[df["Sexo"] == "M", "Peso (kg)"].mean()
    peso_mujeres = df.loc[df["Sexo"] == "F", "Peso (kg)"].mean()

    st.subheader("a) Promedio de altura")
    c1, c2, c3 = st.columns(3)
    c1.metric("General", f"{altura_general:.3f} m")
    c2.metric("Hombres", f"{altura_hombres:.3f} m")
    c3.metric("Mujeres", f"{altura_mujeres:.3f} m")

    st.bar_chart(pd.Series({"General": altura_general, "Hombres": altura_hombres, "Mujeres": altura_mujeres}))

    st.subheader("b) Promedio de peso")
    c1, c2, c3 = st.columns(3)
    c1.metric("General", f"{peso_general:.2f} kg")
    c2.metric("Hombres", f"{peso_hombres:.2f} kg")
    c3.metric("Mujeres", f"{peso_mujeres:.2f} kg")

    st.bar_chart(pd.Series({"General": peso_general, "Hombres": peso_hombres, "Mujeres": peso_mujeres}))


# C y D. Hipertensión
def mostrar_hipertension(df):
    st.header("Hipertensión y peso")
    tiene_hta = df["Hipertensión"] == "Sí"
    cantidad_hta = int(tiene_hta.sum())
    porcentaje_hta = tiene_hta.mean() * 100

    st.subheader("c) Porcentaje de personas con hipertensión")
    c1, c2 = st.columns(2)
    c1.metric("Personas con hipertensión", cantidad_hta)
    c2.metric("Porcentaje", f"{porcentaje_hta:.2f}%")

    conteo_sexo = df.loc[tiene_hta, "Sexo"].value_counts()
    hombres_hta = int(conteo_sexo.get("M", 0))
    mujeres_hta = int(conteo_sexo.get("F", 0))

    if hombres_hta > mujeres_hta:
        comparacion = "Hay más hombres con hipertensión."
    elif mujeres_hta > hombres_hta:
        comparacion = "Hay más mujeres con hipertensión."
    else:
        comparacion = "Hay la misma cantidad de hombres y mujeres con hipertensión."

    st.success(comparacion)
    st.bar_chart(conteo_sexo)

    st.subheader("d) Relación entre hipertensión y peso")
    peso_por_hta = df.groupby("Hipertensión")["Peso (kg)"].mean()
    st.dataframe(peso_por_hta.rename("Peso promedio (kg)").to_frame(), use_container_width=True)
    st.bar_chart(peso_por_hta)


# E. Sobrepeso
def mostrar_sobrepeso(df):
    st.header("Sobrepeso, horas de trabajo y profesión")

    st.subheader("e) Relación entre sobrepeso y horas de trabajo")
    horas_por_sobrepeso = df.groupby("Sobrepeso")["Horas de trabajo/día"].mean()
    st.dataframe(horas_por_sobrepeso.rename("Horas promedio por día").to_frame(), use_container_width=True)
    st.bar_chart(horas_por_sobrepeso)

    st.subheader("Porcentaje de sobrepeso por profesión")
    resumen_profesion = (
        df.assign(Sobrepeso_num=(df["Sobrepeso"] == "Sí").astype(int))
        .groupby("Trabajo")["Sobrepeso_num"]
        .agg(["sum", "count", "mean"])
    )
    resumen_profesion["Porcentaje con sobrepeso (%)"] = resumen_profesion["mean"] * 100
    resumen_profesion = resumen_profesion.rename(
        columns={"sum": "Personas con sobrepeso", "count": "Total de personas"})
    st.dataframe(
        resumen_profesion[["Personas con sobrepeso", "Total de personas", "Porcentaje con sobrepeso (%)"]].round(2),
        use_container_width=True)
    st.bar_chart(resumen_profesion["Porcentaje con sobrepeso (%)"])


# F. Intervalo de confianza
def mostrar_intervalo_confianza(df):
    st.header("Intervalo de confianza de la diferencia de alturas")
    confianza = st.slider("Nivel de confianza", min_value=0.80, max_value=0.99, value=0.95, step=0.01)

    alturas_h = df.loc[df["Sexo"] == "M", "Estatura (m)"].dropna()
    alturas_m = df.loc[df["Sexo"] == "F", "Estatura (m)"].dropna()

    nh, nm = len(alturas_h), len(alturas_m)
    media_h, media_m = alturas_h.mean(), alturas_m.mean()
    sd_h, sd_m = alturas_h.std(ddof=1), alturas_m.std(ddof=1)

    diferencia = media_h - media_m
    error_estandar = math.sqrt((sd_h ** 2 / nh) + (sd_m ** 2 / nm))
    gl = nh + nm - 2
    alfa_ic = 1 - confianza
    t_critico = stats.t.ppf(1 - alfa_ic / 2, gl)

    li = diferencia - t_critico * error_estandar
    ls = diferencia + t_critico * error_estandar

    st.write(f"Cantidad de hombres: **{nh}**")
    st.write(f"Cantidad de mujeres: **{nm}**")
    st.write(f"Promedio altura hombres: **{media_h:.4f} m**")
    st.write(f"Promedio altura mujeres: **{media_m:.4f} m**")
    st.write(f"Diferencia de medias (H - M): **{diferencia:.4f} m**")
    st.write(f"Error estándar: **{error_estandar:.4f}**")
    st.write(f"Grados de libertad: **{gl}**")
    st.write(f"Valor t crítico: **{t_critico:.4f}**")

    st.success(f"IC al {confianza * 100:.0f}%: [{li:.4f}, {ls:.4f}] metros")


# G. Prueba de hipótesis
def mostrar_prueba_hipotesis(df):
    st.header("Prueba de hipótesis para el promedio de IMC")

    promedio_poblacional = st.number_input("IMC promedio poblacional", min_value=1.0, value=25.0, step=0.5)
    alfa = st.number_input("Nivel de significancia", min_value=0.01, max_value=0.20, value=0.05, step=0.01)

    imc = df["IMC"].dropna()
    n = len(imc)
    media_muestra = imc.mean()
    desviacion_muestra = imc.std(ddof=1)
    gl = n - 1

    t_calculado = (media_muestra - promedio_poblacional) / (desviacion_muestra / math.sqrt(n))
    p_valor = stats.t.cdf(t_calculado, gl)
    t_critico = stats.t.ppf(alfa, gl)

    st.write(f"H₀: μ ≥ {promedio_poblacional:.2f}")
    st.write(f"H₁: μ < {promedio_poblacional:.2f}")
    st.write(f"Tamaño de la muestra: **{n}**")
    st.write(f"Media muestral del IMC: **{media_muestra:.4f}**")
    st.write(f"Desviación estándar muestral: **{desviacion_muestra:.4f}**")
    st.write(f"Grados de libertad: **{gl}**")
    st.write(f"t calculado: **{t_calculado:.4f}**")
    st.write(f"t crítico: **{t_critico:.4f}**")
    st.write(f"p-valor: **{p_valor:.4f}**")

    if p_valor < alfa:
        st.success("Decisión: Se rechaza H₀.")
        st.write(
            "Hay evidencia estadística suficiente para afirmar que "
            "el IMC promedio es menor que el promedio poblacional indicado."
        )
    else:
        st.warning("Decisión: No se rechaza H₀.")
        st.write(
            "No hay evidencia estadística suficiente para afirmar que "
            "el IMC promedio es menor que el promedio poblacional indicado."
        )
