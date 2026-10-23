import pandas as pd


df = pd.read_csv("Formulario de Registro de Datos Estudiantiles.csv")
print(df.head())

# 1. Mostrar solo las columnas del dataframe
print("\n#1. Columnas del dataframe:")
print(df.columns)

# 2. Hacer 3 filtros
print("\n#2. Filtros")
print("Filtro 1 - Estudiantes que reprobaron (promedio menor a 3.0):")
reprobados = df[df["PROMEDIO"] < 3.0]
print(reprobados)

print("\nFiltro 2 - Estudiantes con promedio mayor o igual a 4.3:")
buenos = df[df["PROMEDIO"] >= 4.3]
print(buenos[["NOMBRE", "PROMEDIO"]])

print("\nFiltro 3 - Estudiantes que tienen Nu:")
con_nu = df[df["¿Tiene Nu?"] == "Sí"]
print(con_nu[["NOMBRE", "¿Tiene Nu?"]])

# 3. Pregunta: ¿Quién es el estudiante con el mejor promedio?
print("\n#3. ¿Quién es el estudiante con el mejor promedio?")
ordenados = df.sort_values("PROMEDIO", ascending=False)
print(ordenados[["NOMBRE", "PROMEDIO"]].head(1))

# 4. Crear una nueva columna: el promedio en escala de 0 a 100
print("\n#4. Nueva columna PROMEDIO_100:")
df["PROMEDIO_100"] = df["PROMEDIO"] * 20
print(df[["NOMBRE", "PROMEDIO", "PROMEDIO_100"]])

# 5. Calcular el promedio de una columna con groupby
print("\n#5. Promedio académico por tipo de sangre:")
prom = df.groupby("TIPO DE SANGRE")["PROMEDIO"].mean()
print(prom)

# 6. Hacer un conteo
print("\n#6. Cantidad de estudiantes por tipo de sangre:")
conteo = df["TIPO DE SANGRE"].value_counts()
print(conteo)

# 7. Mínimo, máximo y promedio de una columna con su respectiva información
print("\n#7. Edad mínima, máxima y promedio")
print("Estudiante(s) con la edad mínima:")
print(df[df["EDAD"] == df["EDAD"].min()][["NOMBRE", "EDAD"]])
print("\nEstudiante(s) con la edad máxima:")
print(df[df["EDAD"] == df["EDAD"].max()][["NOMBRE", "EDAD"]])
print("\nEdad promedio del grupo:")
print(df["EDAD"].mean())

# 8. Utilizar la función agg de pandas con groupby
print("\n#8. Mínimo, promedio y máximo del PROMEDIO por tipo de sangre:")
resumen = df.groupby("TIPO DE SANGRE")["PROMEDIO"].agg(["min", "mean", "max"])
print(resumen)
