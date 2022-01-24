import math
import re
from math import sqrt
from re import split

import numpy as np
import pandas as pd

archivo = open("source.pdf.txt", encoding="utf8")
patron = '[^\W]'
listaSimbolos = []

for fileLine in archivo:
    palabras = split(patron, fileLine)
    for n in palabras:
        palabraLimpia = re.sub('\n|\s', '', n)
        if palabraLimpia != '' and palabraLimpia != ' ':
            listaSimbolos.append(palabraLimpia)
archivo.close()

archivo = open("source.pdf.txt", encoding="utf8")
leerArchivo = archivo.readlines()
listaPrueba = []

for i in range(len(leerArchivo)):
    listaPrueba.append(leerArchivo[i])

listaPruebaString = "".join(listaPrueba)
datos = []

for indice in range(len(listaSimbolos)):

    if indice > 0:
        primerSimbolo = listaSimbolos[indice - 1]
        segundoSimbolo = listaSimbolos[indice]
        try:
            indice_c = listaPruebaString.index(primerSimbolo)
            indice_h = listaPruebaString.index(segundoSimbolo)
            subcadena = listaPruebaString[indice_c + 1:indice_h]
            if len(subcadena) != 0:
                datos.append(len(subcadena))
            listaPruebaString = listaPruebaString[indice_h:-1]
            indice = indice + 1

        except ValueError:
            print()

datos = datos[:1000]
archivo.close()
print("datos generados: ", datos)
datosNormalizados = []
for i in range(len(datos)):
    datosNormalizados.append(datos[i] / max(datos))
print("datos Normalizados: ", datosNormalizados)


# Prueba de poker k = 3 - Confianza 5%
def truncate(num, ka):
    integer = int(num * (10 ** ka)) / (10 ** ka)
    return float(integer)


print()
print("PRUEBA DE POQUER , 3 Decimales")

datosParaPoker = []

# CONVERTIMOS LOS NUMEROS A STRINGS Y CORTAMOS LA CADENA DESDE LA SEGUNDA POSICION HASTA LA
# QUINTA PARA OBTENER LOS PRIMEROS 3 DECIMALES

for i in range(len(datosNormalizados)):
    aux = (str(datosNormalizados[i]))
    datosParaPoker.append(aux[2:5])

for i in range(len(datosNormalizados)):
    if len(datosParaPoker[i]) == 1:
        datosParaPoker[i] = '500'
    if datosParaPoker[i] == '1':
        datosParaPoker[i] = '000'
print('Datos para poker: ', datosParaPoker)

cartasIguales = 0
cartasDistintas = 0
dosIgualesUnaDistinta = 0

for i in range(len(datosParaPoker)):
    aux = datosParaPoker[i]
    if aux[0] == aux[1] and aux[0] == aux[2]:
        cartasIguales = cartasIguales + 1
    else:
        if aux[0] != aux[1] and aux[0] != aux[2] and aux[1] != aux[2]:
            cartasDistintas = cartasDistintas + 1
        else:
            dosIgualesUnaDistinta = dosIgualesUnaDistinta + 1

foPoker = [cartasIguales, cartasDistintas, dosIgualesUnaDistinta]
print(foPoker)

fePoker = [0.01 * len(datosNormalizados), 0.72 * len(datosNormalizados), 0.24 * len(datosNormalizados)]
strings = ["3 cartas iguales ", "3 Diferentes ", "2 Iguales una diferente "]
auxChicuadrado = []
for i in range(3):
    auxChicuadrado.append((fePoker[i] - foPoker[i]) ** 2 / fePoker[i])

df = pd.DataFrame({"Clases": strings, "FrecObs": foPoker, "FrecEsperada": fePoker, "fe-fo/fe": auxChicuadrado})
pd.set_option("max_rows", None)
df.head()
print(df)

chiCuadrado = 0
for i in range(3):
    chiCuadrado = chiCuadrado + ((fePoker[i] - foPoker[i]) ** 2 / fePoker[i])
print()
print('chiCuadrado obtenido:', chiCuadrado)
# 3 clases, 2 grados de libertad con confianza de 0.05
chiTabla = 5.99
print('chiCuadrado tabla (2 grados de libertad con confianza de 0.05) :', chiTabla)
print(chiCuadrado, '>', chiTabla)
print('RESULTADO: \nComo el valor calculado es mayor que el valor critico, no pasa la prueba! \n')

# Prueba de corridas con media como comparacion
print("PRUEBA DE CORRIDAS CON MEDIA COMO COMPARACION")
promedio = np.mean(datosNormalizados)
print('Promedio = ', promedio)
corridas = []
# si dato mayor que promedio + sino -
numeroCorridas = 0
positivos = 0
negativos = 0

for i in range(len(datosNormalizados)):
    if datosNormalizados[i] > promedio:
        corridas.append('+')
        positivos = positivos + 1
    else:
        corridas.append('-')
print(corridas)

for i in range(len(datosNormalizados) - 1):
    if corridas[i] != corridas[i + 1]:
        numeroCorridas = numeroCorridas + 1
negativos = len(datosNormalizados) - positivos
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

[infCrit, supCrit] = [-1.96 * varianza + media, 1.96 * varianza + media]

print('limite inferior = ', infCrit, ' -  limite superior = ', supCrit)

if supCrit >= numeroCorridas >= infCrit:
    print('El numero de corridas está entre los limites - Pasa La Prueba de corridas por encima y debajo de la media')
else:
    print('No Pasa La Prueba')

# Chi cuadrado confianza 5%
# Prueba CHI 2
print()
print("PRUEBA DE CHI CUADRADO")
confianza = 0.05
n = len(datos)
c = math.ceil((n ** (1 / 2)))
gradosLibertad = c - 1
frecuenciaEsperada = n / c

clases = []
aux = 0
for i in range(c + 1):
    clases.append(aux + 0.033)
    aux = round(clases[i], 2)
    round(clases[i], 0)
print("las clases son", clases)
fe = []
for i in range(c + 1):
    fe.append(n / c)

fo = []
for i in range(c + 1):
    fo.append(0)
for i in range(n):
    if datosNormalizados[i] <= clases[0]:
        fo[0] = fo[0] + 1
    for j in range(c):
        if clases[j - 1] <= datosNormalizados[i] <= clases[j]:
            fo[j] = fo[j] + 1

auxChicuadrado = []
for i in range(c + 1):
    auxChicuadrado.append((fe[i] - fo[i]) ** 2 / fe[i])

df = pd.DataFrame({"Clases": clases, "FrecObs": fo, "FrecEsperada": fe, "fe-fo/fe": auxChicuadrado})
pd.set_option("max_rows", None)
df.head()
print(df)

chiCuadrado = 0
for i in range(c + 1):
    chiCuadrado = chiCuadrado + ((frecuenciaEsperada - fo[i]) ** 2 / frecuenciaEsperada)
print()
print('chiCuadrado obtenido:', chiCuadrado)
print('Chi tabla = 44,9853')
print('El chiCalculado es mayor que el chiCritico por lo tanto el generador no pasa la prueba')
print()
