
# Modelo DuPont – Streamlit App

Esta aplicación permite realizar un análisis financiero usando el modelo DuPont para medir la rentabilidad de negocios. Desarrollado en Python con Streamlit.

## Características

- Carga de archivos CSV o Excel
- Cálculo de indicadores DuPont:
  - Margen Neto (%)
  - Rotación (veces)
  - Apalancamiento (veces)
  - ROE (%)
  - ROA (%)
  - Pay Back Capital (veces)
  - Pay Back Activos (veces)
- Visualización en tabla: columnas = períodos, filas = indicadores
- Exportación del reporte a Excel

## Requisitos

- Python 3.8 o superior
- Instala dependencias con:

```
pip install -r requirements.txt
```

## Ejecución

```
streamlit run app.py
```

## Formato de Datos Esperado

El archivo debe contener las siguientes columnas:
- `Periodo`
- `Utilidad Neta`
- `Ventas Netas`
- `Activos Totales`
- `Capital Contable`
