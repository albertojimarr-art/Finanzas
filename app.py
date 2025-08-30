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
        # Validar que la primera columna sea "INDICADOR"
        if df_raw.columns[0].strip().lower() != "indicador":
            st.error("❌ La primera columna debe llamarse 'INDICADOR'.")
        else:
            # Transponer
            df_transposed = df_raw.set_index("INDICADOR").T
            df_transposed.index.name = "Periodo"
            df_transposed.columns = [col.strip().lower().replace(" ", "_") for col in df_transposed.columns]

            with st.expander("🔁 Datos transpuestos"):
                st.dataframe(df_transposed)

            # Verificar columnas requeridas
            expected = ["utilidad_neta", "ventas_netas", "activos_totales", "capital_contable"]
            if not all(col in df_transposed.columns for col in expected):
                st.error(f"❌ El archivo debe contener estas filas: {', '.join(expected)}")
            else:
                # Convertir a tipo numérico
                for col in expected:
                    df_transposed[col] = pd.to_numeric(df_transposed[col], errors="coerce")

                ventas = df_transposed["ventas_netas"]
                utilidad = df_transposed["utilidad_neta"]
                activos = df_transposed["activos_totales"]
                capital = df_transposed["capital_contable"]

                margen_neto = utilidad / ventas
                rotacion = ventas / activos
                apalancamiento = activos / capital
                roe = margen_neto * rotacion
                roa = rotacion * apalancamiento
                payback_capital = 1 / roe
                payback_activos = 1 / roa

                # Crear DataFrame con columnas como los periodos
                resultado = pd.DataFrame(
                    index=[
                        "Margen Neto", "Rotación", "Apalancamiento",
                        "ROE (Retorno Capital)", "ROA (Retorno Activos)",
                        "Pay Back Capital", "Pay Back Activos"
                    ],
                    columns=df_transposed.index.astype(str)
                )

                # Asignación de métricas
                resultado.loc["Margen Neto"] = (margen_neto * 100).round(1).values
                resultado.loc["Rotación"] = rotacion.round(1).values
                resultado.loc["Apalancamiento"] = apalancamiento.round(1).values
                resultado.loc["ROE (Retorno Capital)"] = (roe * 100).round(1).values
                resultado.loc["ROA (Retorno Activos)"] = (roa * 100).round(1).values
                resultado.loc["Pay Back Capital"] = payback_capital.round(1).values
                resultado.loc["Pay Back Activos"] = payback_activos.round(1).values

                # Cálculo de variación %
                if resultado.shape[1] >= 2:
                    var = ((resultado.iloc[:, -1] - resultado.iloc[:, -2]) / resultado.iloc[:, -2] * 100).round(1)
                    resultado["v%"] = var
                else:
                    resultado["v%"] = np.nan

                st.subheader("📈 Resultados del Modelo DuPont")
                st.dataframe(resultado, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ Error al procesar archivo: {e}")

