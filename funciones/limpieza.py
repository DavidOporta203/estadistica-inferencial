import pandas as pd

def preparar_variables(df):
    # Separar presión arterial
    presion = df["Presión arterial"].astype(str).str.split("/", expand=True)
    df["Sistólica"] = pd.to_numeric(presion[0], errors="coerce")
    df["Diastólica"] = pd.to_numeric(presion[1], errors="coerce")

    # Hipertensión
    df["Hipertensión"] = (
        (df["Sistólica"] >= 140) | (df["Diastólica"] >= 90)
    ).map({True: "Sí", False: "No"})

    # Sobrepeso
    df["Sobrepeso"] = (df["IMC"] >= 25).map({True: "Sí", False: "No"})

    return df
