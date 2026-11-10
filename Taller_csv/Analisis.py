# Actividad 3 · Corte 3: Mi análisis
# Nombres: Juan Diego Alvarez / Juan David Rosas
# Pregunta: ¿Qué categoría de producto genera más ingresos en las ventas de 3 o más unidades?
# Dataset: ventas.csv 

import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------------
# ETAPA 1 · Carga y limpia
# ---------------------------------------------------------------
df = pd.read_csv('FUNDAMENTOS_PROG/Taller_csv/ventas.csv')
print('Filas y columnas:', df.shape)
print(df.head())

print('\nFaltantes por columna:')
print(df.isnull().sum())

filas_antes = len(df)
df = df.dropna()
print(f'\nFilas antes: {filas_antes} | después de dropna(): {len(df)}')

# ---------------------------------------------------------------
# ETAPA 2 · Analiza (un filtro y un groupby)
# ---------------------------------------------------------------
df['ingreso'] = df['unidades'] * df['precio_unitario']

# Filtro: ventas de 3 o más unidades
grandes = df[df['unidades'] >= 3]

# Groupby: ingreso total por categoría
resultado = grandes.groupby('categoria')['ingreso'].sum().sort_values(ascending=False)
print('\nIngreso total por categoría (ventas de 3 o más unidades):')
print(resultado)

# ---------------------------------------------------------------
# ETAPA 3 · Grafica
# ---------------------------------------------------------------
plt.figure(figsize=(8, 5))
plt.bar(resultado.index, resultado.values, color='#1f3a5f')
plt.title('Ingresos totales por categoría (ventas de 3 o más unidades)')
plt.xlabel('Categoría')
plt.ylabel('Ingreso total (COP)')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('grafico.png', dpi=150)
plt.show()

# ---------------------------------------------------------------
# ETAPA 4 · Conclusión
# ---------------------------------------------------------------

#Tecnología es la categoría que más ingresos genera en las ventas de 3 o más unidades,
#con cerca de 39,4 millones de pesos, muy por encima de Deportes (6,5 M) y de Libros, 
#que es la última (1,2 M). Tecnología vende más de seis veces lo que vende la segunda categoría, 
# probablemente porque sus productos tienen un precio unitario mucho más alto. 
# Como los datos tienen filas eliminadas por valores faltantes (36 de 300), 
# el resultado podría cambiar un poco con el dataset completo.