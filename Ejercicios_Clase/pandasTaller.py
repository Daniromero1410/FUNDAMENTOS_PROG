import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

df = pd.read_csv("Forms.csv")

# ---------- 1. Mostrar solo las columnas del dataframe ----------
print("#1. Columnas del dataframe")
print(list(df.columns))
print()

# ---------- 2. Tres filtros ----------
print("#2. Filtros")

# Filtro 1: estudiantes que reprobaron (promedio < 3.0)
reprobaron = df[df["PROMEDIO"] < 3.0]
print("Filtro 1 - Reprobaron (PROMEDIO < 3.0):")
print(reprobaron[["NOMBRE", "PROMEDIO"]] if not reprobaron.empty else "Ninguno reprobó")
print()

# Filtro 2: estudiantes con promedio mayor o igual a 4.3
destacados = df[df["PROMEDIO"] >= 4.3]
print("Filtro 2 - Promedio >= 4.3:")
print(destacados[["NOMBRE", "PROMEDIO"]])
print()

# Filtro 3: estudiantes que NO tienen Nu
sin_nu = df[df["¿Tiene Nu?"] == "No"]
print("Filtro 3 - Sin Nu:")
print(sin_nu[["NOMBRE", "¿Tiene Nu?"]])
print()

# ---------- 4. Nueva columna ----------
# ALTURA viene como "1.71m", "1.72 m", "1,80" y PESO como "71kg", así que
# para poder calcular creamos columnas numéricas nuevas (las originales quedan igual).
df["ALTURA_M"] = (
    df["ALTURA"].astype(str).str.lower()
    .str.replace("m", "", regex=False)
    .str.replace(",", ".", regex=False)
    .str.strip()
    .astype(float)
)
df["PESO_KG"] = df["PESO"].astype(str).str.lower().str.replace("kg", "", regex=False).str.strip().astype(float)

# IMC = peso / altura^2
df["IMC"] = (df["PESO_KG"] / df["ALTURA_M"] ** 2).round(1)
print("#4. Nueva columna IMC")
print(df[["NOMBRE", "PESO_KG", "ALTURA_M", "IMC"]])
print()

# ---------- 3. Pregunta resuelta con tratamiento de datos ----------
# Pregunta: ¿Qué estudiantes tienen un IMC fuera del rango normal (18.5 - 24.9)?
print("#3. ¿Qué estudiantes tienen un IMC fuera del rango normal (18.5 - 24.9)?")
fuera_rango = df[(df["IMC"] < 18.5) | (df["IMC"] > 24.9)]
print(fuera_rango[["NOMBRE", "IMC"]] if not fuera_rango.empty else "Todos están en rango normal")
print()

# ---------- 5. Promedio de una columna con groupby ----------
print("#5. Promedio de notas según si tiene Nu")
print(df.groupby("¿Tiene Nu?")["PROMEDIO"].mean().round(2))
print()

# ---------- 6. Conteo ----------
print("#6. Conteo de estudiantes por tipo de sangre")
print(df["TIPO DE SANGRE"].value_counts())
print()

# ---------- 7. Mínimo, máximo y promedio con su información ----------
print("#7. Mínimo, máximo y promedio de PROMEDIO")
cols_info = ["NOMBRE", "PROMEDIO", "SEMESTRE", "DONDE VIVE"]
print("Mínimo:")
print(df.loc[df["PROMEDIO"] == df["PROMEDIO"].min(), cols_info])
print("\nMáximo:")
print(df.loc[df["PROMEDIO"] == df["PROMEDIO"].max(), cols_info])
promedio = df["PROMEDIO"].mean()
print(f"\nPromedio del grupo: {promedio:.2f}")
# El promedio no es de una persona; mostramos quién queda más cerca
print("Estudiante más cercano al promedio:")
print(df.loc[[(df["PROMEDIO"] - promedio).abs().idxmin()], cols_info])
print()

# ---------- 8. agg con groupby ----------
print("#8. agg con groupby (por ¿Tiene Nu?)")
resumen = df.groupby("¿Tiene Nu?").agg(
    cantidad=("NOMBRE", "count"),
    promedio_notas=("PROMEDIO", "mean"),
    nota_max=("PROMEDIO", "max"),
    nota_min=("PROMEDIO", "min"),
    edad_promedio=("EDAD", "mean"),
    imc_promedio=("IMC", "mean"),
).round(2)
print(resumen)
