from math import sqrt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# Generador

a = 100
m = 165123
c = 1234
xn = 32
total_datos = 10000
confianza = 0.05


datos = []


for i in range(total_datos):
    xn1 = (a * xn + c) % m
    datos.append(xn1)
    xn = xn1
# print('Los datos son', datos)

# Prueba de Kolmogorov-Smirvov
max_numero = max(datos)
# print('numero maximo de los datos = ', max_numero)

# Dividir los datos entre el numero maximo
for i in range(total_datos):
    datos[i] = datos[i] / max_numero
# print("datos ordenados divididos entre el maximo numero", datos)

# Crear las clases e intervalos
numero_clases = int(sqrt(total_datos))
# print('numero de clases = ', numero_clases)
clases = [0.0]

clases = []
aux = 0


for i in range(numero_clases):
    clases.append(aux + 0.01)
    aux = round(clases[i], 2)
    round(clases[i], 0)
# print("las clases son", clases)

# Contar los numeros en los intervalos, frecuencia observada

fo = []
for i in range(numero_clases):
    fo.append(0)
for i in range(total_datos):
    if datos[i] <= clases[0]:
        fo[0] = fo[0] + 1
    for j in range(numero_clases):
        if clases[j-1] <= datos[i] <= clases[j]:
            fo[j] = fo[j] + 1
# print('frecuencia observada', fo)

# frecuencia observada acumulada

foacum = []
for i in range(numero_clases):
    foacum.append(0)
for i in range(numero_clases):
    aux = foacum[i-1]
    foacum[i] = aux + fo[i]
# print('frecuencia observada acumulada', foacum)

# probabilidad observada acumulada

poa = []
for i in range(numero_clases):
    poa.append(0)
for i in range(numero_clases):
    poa[i] = foacum[i]/total_datos

# print('probabilidad observada acumulada', poa)

# probabilidad esperada acumulada

pea = []
pea = clases
# print('probabilidad esperada acumulada', pea)

# PEA-POA
restaprobabilidades = []
for i in range(numero_clases):
    restaprobabilidades.append(0)
for i in range(numero_clases):
    restaprobabilidades[i] = abs(pea[i] - poa[i])
# print('PEA - POA', restaprobabilidades)

# dmCritico y dmCalculado

dmCalc = max(restaprobabilidades)
print('DM Calculado', dmCalc)
dmCritico = 1.36/sqrt(total_datos)
print('DM Critico', dmCritico)

if dmCalc <= dmCritico:
    print(dmCalc, '<=', dmCritico)
    print('Se acepta la hipótesis de que el generadores bueno en cuanto a uniformidad')
else:
    print('No se acepta la hipotesis')

print()
df = pd.DataFrame({"Clases": clases, "FrecObs": fo, "FrecObsAcum": foacum, "ProbObsAcum": poa, "ProbEspAcum": pea,  "PEA - POA": restaprobabilidades})
pd.set_option("max_rows", None)
df.head()
print(df)








