
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

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

        def convertir_excel_con_formulas(df_original):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df_original.to_excel(writer, sheet_name='Datos', index=False)

            workbook = writer.book
            worksheet = writer.sheets['Datos']

            headers = ['Margen Neto (%)', 'Rotación (veces)', 'Apalancamiento (veces)', 
                       'ROE (%)', 'ROA (%)', 'Pay Back Capital (veces)', 'Pay Back Activos (veces)']
            for idx, header in enumerate(headers):
                worksheet.write(0, 5 + idx, header)

            for row in range(1, len(df_original) + 1):
                worksheet.write_formula(row, 5, f'=B{row + 1}/C{row + 1}*100')  # Margen Neto
                worksheet.write_formula(row, 6, f'=C{row + 1}/D{row + 1}')       # Rotación
                worksheet.write_formula(row, 7, f'=D{row + 1}/E{row + 1}')       # Apalancamiento
                worksheet.write_formula(row, 8, f'=F{row + 1}*G{row + 1}')       # ROE
                worksheet.write_formula(row, 9, f'=G{row + 1}*H{row + 1}')       # ROA
                worksheet.write_formula(row, 10, f'=1/(I{row + 1}/100)')         # Pay Back Capital
                worksheet.write_formula(row, 11, f'=1/(J{row + 1}/100)')         # Pay Back Activos

            writer.close()
            output.seek(0)
            return output

        st.download_button(
            label="📥 Descargar reporte en Excel con fórmulas",
            data=convertir_excel_con_formulas(df_grouped),
            file_name="reporte_dupont.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:
        st.error("⚠️ El archivo debe contener las siguientes columnas: " + ", ".join(columnas_necesarias))
else:
    st.info("📎 Sube un archivo Excel o CSV para comenzar el análisis.")
