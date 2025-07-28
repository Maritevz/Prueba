# Prueba sobre apuntamiento Precio Capturado de Energías Renovables

Este trabajo procesa datos de precios y volúmenes de generación solar (fotovoltaica) y eólica para calcular el **apuntamiento del precio capturado** por cada tecnología en períodos diario, mensual y anual.

## Pasos realizados

1. **Descarga y carga de datos**  
   Se importan archivos Excel con datos horarios de precios, volumen fotovoltaico y volumen eólico.

2. **Unificación y limpieza**  
   Se crea un DataFrame con fecha, año, mes, día, hora, precio, volumen solar y volumen eólico. Se guarda el dataset limpio en Excel.

3. **Cálculo de apuntamiento**  
   Se calcula el apuntamiento como el promedio ponderado del precio capturado por tecnología en los distintos periodos (diario, mensual y anual). Los resultados se exportan a Excel para revisión.

4. **Visualización**  
   Se generan gráficos interactivos con la librería Plotly, mostrando la evolución del apuntamiento para ambas tecnologías con tonos pastel.

## Resultados y conclusiones breves
