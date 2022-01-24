from math import sqrt
import math
import numpy as np
import pandas as pd
import itertools as it

datos = [0.3163, 0.4438, 0.5747, 0.1908, 0.2829, 0.6034, 0.2011, 0.6643, 0.9016, 0.2913,
         0.1319, 0.6235, 0.6208, 0.9173, 0.2296, 0.6305, 0.7348, 0.3657, 0.4250, 0.5200,
         0.7299, 0.3847, 0.6850, 0.9083, 0.1024, 0.7366, 0.2248, 0.7218, 0.2277, 0.6495,
         0.9208, 0.7804, 0.5920, 0.7126, 0.8892, 0.7757, 0.7795, 0.6775, 0.3438, 0.2234,
         0.2948, 0.6049, 0.7617, 0.5667, 0.0706, 0.4907, 0.0686, 0.4993, 0.7706, 0.5910,
         0.7113, 0.5349, 0.8835, 0.0349, 0.3063, 0.2370, 0.0985, 0.7607, 0.5853, 0.9042,
         0.0049, 0.9620, 0.4767, 0.9255, 0.5806, 0.1856, 0.0508, 0.4864, 0.7624, 0.2841,
         0.8394, 0.3062, 0.1635, 0.6599, 0.4443, 0.0346, 0.0260, 0.2889, 0.6681, 0.7640,
         0.9723, 0.9096, 0.4579, 0.8236, 0.3435, 0.9882, 0.0777, 0.6874, 0.3303, 0.5752]

# print(datos)
confianza = 0.1
total_datos = 90

# Prueba de Kolmogorov-Smirvov
print('Polmogorov-Smirnov\n')
max_numero = max(datos)
numero_clases = int(sqrt(total_datos))
clases = [0.0]
clases = []
aux = 0

for i in range(numero_clases):
    clases.append(aux + 0.11)
    aux = round(clases[i], 2)
    round(clases[i], 0)

fo = []
for i in range(numero_clases):
    fo.append(0)
for i in range(total_datos):
    if datos[i] <= clases[0]:
        fo[0] = fo[0] + 1
    for j in range(numero_clases):
        if clases[j - 1] <= datos[i] <= clases[j]:
            fo[j] = fo[j] + 1

foacum = []
for i in range(numero_clases):
    foacum.append(0)
for i in range(numero_clases):
    aux = foacum[i - 1]
    foacum[i] = aux + fo[i]

poa = []
for i in range(numero_clases):
    poa.append(0)
for i in range(numero_clases):
    poa[i] = foacum[i] / total_datos

pea = []
pea = clases
restaprobabilidades = []
for i in range(numero_clases):
    restaprobabilidades.append(0)
for i in range(numero_clases):
    restaprobabilidades[i] = abs(pea[i] - poa[i])

dmCalc = max(restaprobabilidades)
print('DM Calculado', dmCalc)
dmCritico = 1.22 / sqrt(total_datos)
print('DM Critico', dmCritico)

if dmCalc <= dmCritico:
    print(dmCalc, '<=', dmCritico)
    print('Se acepta la hipótesis de que el generadores bueno en cuanto a uniformidad')
else:
    print('No se acepta la hipotesis')

print()
df = pd.DataFrame({"Clases": clases, "FrecObs": fo, "FrecObsAcum": foacum, "ProbObsAcum": poa, "ProbEspAcum": pea,
                   "PEA - POA": restaprobabilidades})
pd.set_option("max_rows", None)
df.head()
print(df)

# Prueba de corridas(Por encima y debajo de la media)
print()
print("PRUEBA DE CORRIDAS\n")
promedio = np.mean(datos)
print('Promedio = ', promedio)
corridas = []
# si dato mayor que promedio + sino -
numeroCorridas = 0
positivos = 0
negativos = 0

for i in range(total_datos):
    if datos[i] > promedio:
        corridas.append('+')
        positivos = positivos + 1
    else:
        corridas.append('-')
print(corridas)

for i in range(total_datos - 1):
    if corridas[i] != corridas[i + 1]:
        numeroCorridas = numeroCorridas + 1
negativos = total_datos - positivos
print('numero de corridas', numeroCorridas)
print('positivos', positivos)
print('negativos', negativos)

# Aplicamos las fórmulas para media, varianza y Z.
media = ((2 * positivos * negativos) / (positivos + negativos)) + 1
print('media', media)

varianza = sqrt((2 * positivos * negativos * ((2 * positivos * negativos) - positivos - negativos))
                / (((positivos + negativos) ** 2) * (positivos + negativos + 1)))
print('varianza', varianza)
z = abs((numeroCorridas - media) / sqrt(varianza))
print("Z=", z)

[infCrit, supCrit] = [-1.65 * varianza + media, 1.65 * varianza + media]

print('limite inferior = ', infCrit, ' -  limite superior = ', supCrit)

if supCrit >= numeroCorridas >= infCrit:
    print('El numero de corridas está entre los limites - Pasa La Prueba')
else:
    print('No Pasa La Prueba')

# Prueba de series(k=4)

print()
print("PRUEBA DE SERIES\n")

k = 4
grupos = int(total_datos / 4)
total_clases = math.ceil(sqrt(grupos))
dimension = math.ceil(total_clases ** (1 / 4))

print('Grupos', grupos)
print('Total de clases', total_clases)
print('Dimension', dimension)
grupos_total = np.zeros((grupos, k))
total_final_clases = dimension ** k
print('Clases por dimension', total_final_clases)
fe = grupos / total_final_clases
print('Frecuencia esperada', fe)

aux = 0
for i in range(0, grupos * 4, 4):
    grupos_total[aux] = datos[i], datos[i + 1], datos[i + 2], datos[i + 3]
    aux += 1

print("Datos por grupos de 4 dimensiones: \n\n", grupos_total)

a = list(it.product([1, 2], repeat=4))
print()
print('codificacion para las clases \n', a)
print()

auxDatos = np.zeros((grupos, k))

for i in range(grupos):
    for j in range(k):
        if grupos_total[i][j] <= 0.5:
            auxDatos[i][j] = 1
        else:
            auxDatos[i][j] = 2

print('Datos codificados dependiendo si es menor o mayor a 0.5 (Dimension 2) \n', auxDatos)

fo = []
for i in range(total_final_clases):
    fo.append(0)

for i in range(grupos):
    for j in range(total_final_clases):
        if np.array_equal(auxDatos[i], a[j]):
            fo[j] = fo[j] + 1
print()
print('Frecuencias absolutas observadas\n', fo)
print()

df = pd.DataFrame({"Clases": a, "FrecObs": fo})
pd.set_option("max_rows", None)
df.head()
print(df)

chiCuadrado = 0
for i in range(total_final_clases):
    chiCuadrado = chiCuadrado + ((fe-fo[i])**2/fe)
print()
print('chiCuadrado obtenido:', chiCuadrado)
# 16 clases, 15 grados de libertad con confianza de 0.1
chiTabla = 22.31
print('chiCuadrado tabla (15 grados de libertad con confianza de 0.1) :', chiTabla)
print(chiCuadrado, '<' , chiTabla)
print()
print('RESULTADO: \nComo el valor calculado es menor que el valor critico, pasa la prueba!')

