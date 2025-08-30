import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Modelo DuPont", layout="wide")

st.title("📊 Análisis de Rentabilidad – Modelo DuPont")

# Cargar archivo
uploaded_file = st.file_uploader("📁 Cargar archivo Excel con la base de datos", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name=0)
    st.success("Archivo cargado correctamente.")

    # Mostrar DataFrame original
    with st.expander("🔍 Ver datos cargados"):
        st.dataframe(df)

    # Verificar columnas necesarias
    required_cols = ["Periodo", "Utilidad Neta", "Ventas Netas", "Activos Totales", "Capital Contable"]
    if not all(col in df.columns for col in required_cols):
        st.error(f"❌ El archivo debe contener las siguientes columnas: {', '.join(required_cols)}")
    else:
        # Convertimos el DataFrame al índice "Periodo"
        df.set_index("Periodo", inplace=True)

        # Cálculos
        resultado = pd.DataFrame(index=[
            "Margen Neto", "Rotación", "Apalancamiento",
            "ROE (Retorno Capital)", "ROA (Retorno Activos)",
            "Pay Back Capital", "Pay Back Activos"
        ])

        # Calcular métricas
        utilidad_neta = df["Utilidad Neta"]
        ventas = df["Ventas Netas"]
        activos = df["Activos Totales"]
        capital = df["Capital Contable"]

        margen_neto = utilidad_neta / ventas
        rotacion = ventas / activos
        apalancamiento = activos / capital
        roe = margen_neto * rotacion
        roa = rotacion * apalancamiento
        payback_capital = 1 / roe
        payback_activos = 1 / roa

        # Agregar a tabla
        resultado.loc["Margen Neto"] = (margen_neto * 100).round(1)
        resultado.loc["Rotación"] = rotacion.round(1)
        resultado.loc["Apalancamiento"] = apalancami
