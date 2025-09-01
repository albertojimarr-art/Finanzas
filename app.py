
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Modelo DuPont", layout="wide")

st.title("📊 Modelo DuPont – Análisis de Rentabilidad de Negocios")

st.sidebar.header("Carga tu archivo")
file = st.sidebar.file_uploader("Sube un archivo Excel o CSV", type=["csv", "xlsx"])

if file:
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    st.subheader("Vista previa de los datos")
    st.dataframe(df)

    columnas_necesarias = [
        'Periodo', 'Utilidad Neta', 'Ventas Netas',
        'Activos Totales', 'Capital Contable'
    ]

    if all(col in df.columns for col in columnas_necesarias):
        df_grouped = df.groupby('Periodo').sum().reset_index()

        df_grouped['Margen Neto (%)'] = (df_grouped['Utilidad Neta'] / df_grouped['Ventas Netas']) * 100
        df_grouped['Rotación (veces)'] = df_grouped['Ventas Netas'] / df_grouped['Activos Totales']
        df_grouped['Apalancamiento (veces)'] = df_grouped['Activos Totales'] / df_grouped['Capital Contable']
        df_grouped['ROE (%)'] = df_grouped['Margen Neto (%)'] * df_grouped['Rotación (veces)']
        df_grouped['ROA (%)'] = df_grouped['Rotación (veces)'] * df_grouped['Apalancamiento (veces)']
        df_grouped['Pay Back Capital (veces)'] = 1 / (df_grouped['ROE (%)'] / 100)
        df_grouped['Pay Back Activos (veces)'] = 1 / (df_grouped['ROA (%)'] / 100)

        columnas_relativas = ['Margen Neto (%)', 'ROE (%)', 'ROA (%)']
        columnas_absolutas = ['Rotación (veces)', 'Apalancamiento (veces)', 'Pay Back Capital (veces)', 'Pay Back Activos (veces)']

        df_grouped[columnas_relativas] = df_grouped[columnas_relativas].round(1)
        df_grouped[columnas_absolutas] = df_grouped[columnas_absolutas].round(1)

        df_resultado = df_grouped.set_index('Periodo')[
            columnas_relativas + columnas_absolutas
        ].T

        st.subheader("📋 Reporte de Rentabilidad - Modelo DuPont")
        st.dataframe(df_resultado)

        def convertir_excel(df):
            from io import BytesIO
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='DuPont')
            writer.close()
            output.seek(0)
            return output

        st.download_button(
            label="📥 Descargar reporte en Excel",
            data=convertir_excel(df_resultado),
            file_name="reporte_dupont.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:
        st.error("⚠️ El archivo debe contener las siguientes columnas: " + ", ".join(columnas_necesarias))
else:
    st.info("📎 Sube un archivo Excel o CSV para comenzar el análisis.")
