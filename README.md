# Modelo DuPont – Streamlit App

Esta aplicación permite cargar un archivo Excel con indicadores financieros y calcula automáticamente el modelo DuPont.

## Instrucciones

1. Clona este repositorio o descarga los archivos.
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta la app con:
   ```bash
   streamlit run app.py
   ```

## Estructura esperada del archivo Excel

- Primera columna: `INDICADOR`
- Filas: `Ventas Netas`, `Utilidad Neta`, `Activos Totales`, `Capital Contable`
- Columnas: Años o períodos financieros (2023, 2024, etc.)

