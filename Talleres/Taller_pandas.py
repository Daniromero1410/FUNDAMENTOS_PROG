import pandas as pd

df = pd.read_csv('FUNDAMENTOS_PROG/Talleres/creditos_colombia.csv')

#1) Mostrar Columnas
print(f"Las columnas son: {df.columns.tolist()}")

# 2) 3 Filtros
# Filtro 1: Los creditos informales
informales = df[df['Tipo'] == 'Informal']
print(f"Informales: {informales.head()}")

# Filtro 2: Monto mayor a 400000
mayor_400k = df[df['Monto_Solicitado'] > 400000]
print(f"Cupo mayor a 400k: {mayor_400k.head()}")

# Filtro 3: Satisfaccion mayor o igual a 8
recomendados = df[df['Satisfaccion_Cliente'] >= 8]
print(f"Recomendados: {recomendados.head()}")

# 3) Pregunta que se pueda tratar con tratamiento de datos
# Pregunta: ¿Qué créditos formales (sin riesgo) tienen tasa menor a 2.15% y satisfacción >= 8, ordenados de mejor a peor satisfacción?
convenientes = df [
    (df["Tipo"] != "Informal") &
    (df["Tasa_Interes_Mensual"] < 2.15) &
    (df["Satisfaccion_Cliente"] >= 8)
]
convenientes = convenientes[['Entidad', 'Tipo', 'Tasa_Interes_Mensual', 'Cuotas', 'Satisfaccion_Cliente']]
convenientes = convenientes.sort_values('Satisfaccion_Cliente', ascending=False)
print(f"Créditos convenientes:\n{convenientes}")

# 4) Nueva columna: interés por cada $100.000 prestados (interés simple)
df['Interes_por_100k'] = 100000 * (df['Tasa_Interes_Mensual'] / 100) * df['Cuotas']
print(f"Interés por cada $100.000 prestados:\n{df[['Entidad', 'Tipo', 'Interes_por_100k']]}")

# 5) Promedio de una columna con groupby: Tasa de Interés Mensual por Tipo
promedio_tasa = df.groupby("Tipo")["Tasa_Interes_Mensual"].mean().sort_values()
print(f"Promedio de Tasa de Interés Mensual por Tipo:\n{promedio_tasa}")

# 6) Hacer un conteo por tipo
conteo_tipo = df['Tipo'].value_counts()
print(f"Conteo por tipo:\n{conteo_tipo}")

# 7) Minimo maximo y promedio de la columna Monto_Solicitado por tipo
datos_monto = df.groupby("Tipo")["Monto_Solicitado"].agg(['min', 'max', 'mean'])
print(f"Mínimo, máximo y promedio de Monto_Solicitado por Tipo:\n{datos_monto}")

# 8) Función agg con groupby
resumen = df.groupby('Tipo').agg({
    'Tasa_Interes_Mensual': ['min', 'max', 'mean'],
    'Satisfaccion_Cliente': 'mean',
    'Interes_por_100k': 'mean'
})
print(f"Resumen por tipo:\n{resumen}")