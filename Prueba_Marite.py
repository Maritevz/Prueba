import pandas as pd
import plotly.graph_objects as go

# --- Paso 1: Descargar y cargar datos ---

def cargar_archivo(nombre_archivo, nombre_columna):
    df = pd.read_excel(nombre_archivo, header=1)
    df = df[['datetime', 'value']].copy()
    df = df.rename(columns={'value': nombre_columna})
    df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
    return df

precios = cargar_archivo('Precios.xlsx', 'precio')
fotovoltaica = cargar_archivo('Fotovoltaica.xlsx', 'volumen_pv')
eolica = cargar_archivo('Eolica.xlsx', 'volumen_wind')

# --- Paso 2: Crear dataframe unificado con columnas fecha, año, mes, día, hora, precio, volumen_pv, volumen_wind ---

df = precios.merge(fotovoltaica, on='datetime').merge(eolica, on='datetime')

df['año'] = df['datetime'].dt.year
df['mes'] = df['datetime'].dt.month
df['día'] = df['datetime'].dt.day
df['hora'] = df['datetime'].dt.hour
df['fecha'] = df['datetime'].dt.date

# Guardar datos limpios para revisión
df_exportar = df[['fecha', 'año', 'mes', 'día', 'hora', 'precio', 'volumen_pv', 'volumen_wind']]
df_exportar.to_excel('datos_limpios_unidos.xlsx', index=False)
print("✅ Archivo 'datos_limpios_unidos.xlsx' creado con éxito.")

# --- Paso 3: Calcular el apuntamiento (precio capturado) para cada tecnología y periodo ---

# Crear columnas auxiliares necesarias para cálculo
df['precio_pv'] = df['precio'] * df['volumen_pv']
df['precio_wind'] = df['precio'] * df['volumen_wind']

def calcular_apuntamiento(df, tecnologia, energia, periodo, nombre_columna):
    if periodo == 'diario':
        group_cols = ['año', 'mes', 'día']
    elif periodo == 'mensual':
        group_cols = ['año', 'mes']
    elif periodo == 'anual':
        group_cols = ['año']
    else:
        raise ValueError("Periodo debe ser 'diario', 'mensual' o 'anual'")
    
    apun = df.groupby(group_cols).apply(
        lambda x: x[energia].sum() / x[tecnologia].sum()
    ).reset_index(name=nombre_columna)
    
    return apun

apun_diario_pv = calcular_apuntamiento(df, 'volumen_pv', 'precio_pv', 'diario', 'apuntamiento_pv')
apun_diario_wind = calcular_apuntamiento(df, 'volumen_wind', 'precio_wind', 'diario', 'apuntamiento_wind')
apun_diario = apun_diario_pv.merge(apun_diario_wind, on=['año', 'mes', 'día'])

apun_mensual_pv = calcular_apuntamiento(df, 'volumen_pv', 'precio_pv', 'mensual', 'apuntamiento_pv')
apun_mensual_wind = calcular_apuntamiento(df, 'volumen_wind', 'precio_wind', 'mensual', 'apuntamiento_wind')
apun_mensual = apun_mensual_pv.merge(apun_mensual_wind, on=['año', 'mes'])

apun_anual_pv = calcular_apuntamiento(df, 'volumen_pv', 'precio_pv', 'anual', 'apuntamiento_pv')
apun_anual_wind = calcular_apuntamiento(df, 'volumen_wind', 'precio_wind', 'anual', 'apuntamiento_wind')
apun_anual = apun_anual_pv.merge(apun_anual_wind, on='año')

# Guardar apuntamientos a Excel para revisión
with pd.ExcelWriter('apuntamientos_generacion.xlsx') as writer:
    apun_diario.to_excel(writer, sheet_name='Diario', index=False)
    apun_mensual.to_excel(writer, sheet_name='Mensual', index=False)
    apun_anual.to_excel(writer, sheet_name='Anual', index=False)

print("✅ Archivo 'apuntamientos_generacion.xlsx' creado con éxito.")

# --- Paso 4: Graficar apuntamientos ---

def graficar_apuntamiento(df_pv, df_wind, eje, titulo, eje_x_label, nombre_archivo):
    df_plot = df_pv.merge(df_wind, on=eje, suffixes=('_pv', '_wind'))
    
    if isinstance(eje, list):
        df_plot['x'] = df_plot[eje].astype(str).agg('-'.join, axis=1)
    else:
        df_plot['x'] = df_plot[eje].astype(str)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_plot['x'],
        y=df_plot['apuntamiento_pv'],
        mode='lines+markers',
        name='Solar',
        line=dict(color='#FFA07A')  
    ))

    fig.add_trace(go.Scatter(
        x=df_plot['x'],
        y=df_plot['apuntamiento_wind'],
        mode='lines+markers',
        name='Eólica',
        line=dict(color='#87CEFA')  
    ))

    fig.update_layout(
        title=titulo,
        xaxis_title=eje_x_label,
        yaxis_title='Precio Capturado (€/MWh)',
        legend=dict(x=0.01, y=0.99),
        template='plotly_white'
    )

    fig.write_html(nombre_archivo)
    print(f"✅ Gráfico guardado como {nombre_archivo}")

# Generar y guardar gráficos
graficar_apuntamiento(apun_diario_pv, apun_diario_wind, ['año', 'mes', 'día'], 
                      'Apuntamiento Diario Solar vs Eólica', 'Día', 'grafico_apuntamiento_diario.html')

graficar_apuntamiento(apun_mensual_pv, apun_mensual_wind, ['año', 'mes'], 
                      'Apuntamiento Mensual Solar vs Eólica', 'Mes', 'grafico_apuntamiento_mensual.html')

graficar_apuntamiento(apun_anual_pv, apun_anual_wind, 'año', 
                      'Apuntamiento Anual Solar vs Eólica', 'Año', 'grafico_apuntamiento_anual.html')


