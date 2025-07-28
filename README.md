# Prueba sobre apuntamiento Precio Capturado de Energías Renovables ☀️🌬️

Este trabajo procesa datos de precios y volúmenes de generación solar (fotovoltaica) y eólica para calcular el **apuntamiento del precio capturado** por cada tecnología en períodos diario, mensual y anual.

## Pasos realizados

1. **Descarga y carga de datos**  
   Se importan archivos Excel con datos horarios de precios, volumen fotovoltaico y volumen eólico.

2. **Unificación y limpieza**  
   Se crea un DataFrame con fecha, año, mes, día, hora, precio, volumen solar y volumen eólico. Se guarda el dataset limpio en Excel.

3. **Cálculo de apuntamiento**  
   Se calcula el apuntamiento como el promedio ponderado del precio capturado por tecnología en los distintos periodos (diario, mensual y anual). Los resultados se exportan a Excel para revisión.

4. **Visualización**  
   Se generan gráficos interactivos con la librería Plotly, mostrando la evolución del apuntamiento para ambas tecnologías.

## Instrucciones para ejecutar y generar archivos

Para ejecutar este proyecto correctamente, se deberán seguir estos pasos:

1. **Archivos base necesarios**  
   Asegúrate de tener los siguientes archivos Excel con los datos horarios en la misma carpeta que el script, todos ellos disponibles en el repositorio:
   - `Precios.xlsx` — con columnas `datetime` y `value` para los precios horarios.
   - `Fotovoltaica.xlsx` — con columnas `datetime` y `value` para el volumen fotovoltaico horario.
   - `Eolica.xlsx` — con columnas `datetime` y `value` para el volumen eólico horario.

2. **Ejecutar el script**  
   Corre el script Python (Prueba_Marite.py) desde Visual Studio Code.

3. **Archivos generados**  
   Al finalizar, el script generará:
   - "datos_limpios_unidos.xlsx" — contiene los datos combinados con columnas de fecha, hora, precio y volúmenes.
   - "apuntamientos_generacion.xlsx" — contiene los resultados del apuntamiento diario, mensual y anual para cada tecnología.
   - Tres archivos HTML interactivos con gráficos:  
     "grafico_apuntamiento_diario.html" 
     "grafico_apuntamiento_mensual.html"  
     "grafico_apuntamiento_anual.html"

4. **Revisión de resultados**  
   Si se desea revisar con más detalle, los archivos Excel con los datos base y los apuntamientos estan disponibles, y los archivos HTML pueden ser abiertos en cualquier navegador para visualizar los gráficos interactivos.

## Resultados y conclusiones breves



