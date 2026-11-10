
import pandas as pd
import matplotlib.pyplot as plt

# El CSV está en la misma carpeta que este archivo
RUTA_CSV = __file__.replace("actividad3_analisis.py", "ventas_tienda.csv")


# ------------------------------------------------------------
# 1. CARGA Y LIMPIA
# ------------------------------------------------------------
df = pd.read_csv(RUTA_CSV)
print("Filas y columnas:", df.shape)
print(df.head())

# ¿Cuántos datos faltan en cada columna?
print("\nDatos faltantes por columna:")
print(df.isnull().sum())

# Eliminamos las filas que tienen algún dato faltante
filas_antes = len(df)
df = df.dropna()
print("\nFilas antes:", filas_antes)
print("Filas después:", len(df))
print("Filas eliminadas:", filas_antes - len(df))
print("Faltantes que quedan:", df.isnull().sum().sum())


# ------------------------------------------------------------
# 2. ANALIZA
# ------------------------------------------------------------
# Columna nueva: total de cada venta
df["total"] = df["cantidad"] * df["precio_unitario"]

# Filtro: solo Bucaramanga
bucaramanga = df[df["ciudad"] == "Bucaramanga"]
print("\nVentas en Bucaramanga:", len(bucaramanga))

# Groupby: total vendido por categoría, de mayor a menor
ventas_categoria = bucaramanga.groupby("categoria")["total"].sum().sort_values(ascending=False)
print("\nTotal vendido por categoría en Bucaramanga:")
print(ventas_categoria)

# Porcentaje que aporta cada categoría
porcentaje = (ventas_categoria / ventas_categoria.sum() * 100).round(1)
print("\nPorcentaje del total:")
print(porcentaje)


# ------------------------------------------------------------
# 3. GRAFICA
# Gráfico de barras: compara el dinero vendido entre categorías
# ------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
barras = ax.bar(ventas_categoria.index, ventas_categoria.values / 1_000_000, color="#1f4e79")

ax.set_title("Ventas por categoría en Bucaramanga (jul–oct 2026)", fontsize=13, fontweight="bold")
ax.set_xlabel("Categoría de producto")
ax.set_ylabel("Total vendido (millones de pesos)")
ax.bar_label(barras, fmt="%.2f M", padding=3)

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# 4. CONCLUYE
# ------------------------------------------------------------
print("\nCategoría que más vende:", ventas_categoria.index[0], "-", porcentaje.iloc[0], "%")
print("Categoría que menos vende:", ventas_categoria.index[-1], "-", porcentaje.iloc[-1], "%")

# CONCLUSIÓN:
# En Bucaramanga, Calzado es la categoría que más dinero genera, con el 68 %
# del dinero vendido, aunque Ropa vende casi las mismas unidades (70 contra 69):
# la diferencia la hace el precio alto de los tenis y los guayos.
# Accesorios es la que menos aporta (2,7 %), porque son productos baratos y se
# venden poco. Por eso, a la tienda le conviene mantener bien surtido el calzado
# en Bucaramanga y usar los accesorios como complemento de esas compras.
