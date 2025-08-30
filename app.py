import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Modelo DuPont", layout="wide")
st.title("📊 Análisis de Rentabilidad – Modelo DuPont")

uploaded_file = st.file_uploader("📁 Cargar archivo Excel con la base de datos", type=["xlsx"])

if uploaded_file:
    df_raw = pd.read_excel(uploaded_file, sheet_name=0)
    st.success("✅ Archivo cargado correctamente.")

    with st.expander("🔍 Ver datos cargados"):
        st.dataframe(df_raw)

    try:
        # Validar encabezado de la primera columna
        if df_raw.columns[0].strip().lower() != "indicador":
            st.error("❌ La primera columna debe llamarse 'INDICADOR'.")
        else:
            # Transponer DataFrame
            df_transposed = df_raw.set_index("INDICADOR").T
            df_transposed.index.name = "Periodo"
            df_transposed.columns = [col.strip().lower().replace(" ", "_") for col in df_transposed.columns]

            with st.expander("🔁 Datos transpuestos"):
                st.dataframe(df_transposed)

            # Verificar que estén los campos clave
            expected = ["utilidad_neta", "ventas_netas", "activos_totales", "capital_contable"]
            if not all(col in df_transposed.columns for col in expected):
                st.error(f"❌ El archivo debe contener estas filas: {', '.join(expected)}")
            else:
                # Limpiar y convertir datos a tipo numérico
                for col in expected:
                    df_transposed[col] = (
                        df_transposed[col]
                        .astype(str)
                        .str.replace(",", "")
                        .str.strip()
                        .replace("", np.nan)
                        .astype(float)
                    )

                # Calcular ratios financieros
                ventas = df_transposed["ventas_netas"]
                utilidad = df_transposed["utilidad_neta"]
                activos = df_transposed["activos_totales"]
                capital = df_transposed["capital_contable"]

                margen_neto = utilidad / ventas
                rotacion = ventas / activos
                apalancamiento = activo
