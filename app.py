import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Modelo DuPont", layout="wide")

st.title("Modelo DuPont – Análisis de Rentabilidad de Negocios")

# Carga de archivo
uploaded_file = st.file_uploader("Carga tu base de datos (Excel o CSV)", type=["xlsx", "xls", "csv"])

if uploaded_file:
    # Lectura del archivo
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Datos cargados")
    st.dataframe(df)

    # Verificación de columnas necesarias
    columnas_necesarias = ["Periodo", "Utilidad Neta", "Ventas Netas", "Activos Totales", "Capital Contable"]
    if all(col in df.columns for col in columnas_necesarias):
        df = df[columnas_necesarias]
        df = df.sort_values("Periodo")
        df.set_index("Periodo", inplace=True)

        # Cálculos de indicadores
        resultados = pd.DataFrame(index=[
            "Margen Neto", "Rotación", "Apalancamiento", "ROE (Retorno Capital)",
            "ROA (Retorno Activos)", "Pay Back Capital", "Pay Back Activos"
        ])

        margen_neto = df["Utilidad Neta"] / df["Ventas Netas"]
        rotacion = df["Ventas Netas"] / df["Activos Totales"]
        apalancamiento = df["Activos Totales"] / df["Capital Contable"]

        roe = margen_neto * rotacion
        roa = rotacion * apalancamiento

        payback_capital = 1 / roe.replace(0, np.nan)
        payback_activos = 1 / roa.replace(0, np.nan)

        # Redondeo con formato requerido
        resultados.loc["Margen Neto"] = (margen_neto * 100).round(1)
        resultados.loc["Rotación"] = rotacion.round(1)
        resultados.loc["Apalancamiento"] = apalancamiento.round(1)
        resultados.loc["ROE (Retorno Capital)"] = (roe * 100).round(1)
        resultados.loc["ROA (Retorno Activos)"] = (roa * 100).round(1)
        resultados.loc["Pay Back Capital"] = payback_capital.round(1)
        resultados.loc["Pay Back Activos"] = payback_activos.round(1)

        # Agregar variación porcentual v%
        def variacion_porcentual(serie):
            return (serie.pct_change(axis="columns") * 100).iloc[:, -1].round(1)

        resultados["v%"] = variacion_porcentual(resultados.drop(columns="v%", errors='ignore'))

        st.subheader("Reporte DuPont")
        st.dataframe(resultados)

    else:
        st.error(f"Tu archivo debe contener estas columnas: {', '.join(columnas_necesarias)}")
