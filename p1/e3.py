# -*- coding: iso-8859-15 -*-
# Ejercicio 3. Criba de erostóstones

# Funciones
# -----------------------
def criba_eratostenes(lista, n):
	fin = False
	i = 0
	while fin == False:
		if lista[i] != "null":
			if lista[i]*lista[i] > n:
				fin = True
			else:
				for j in range(i+1, len(lista)-1):
					if lista[j] != "null":
						if lista[j]%lista[i] == 0:
							lista[j] = "null"
		i=i+1

# Main
# -----------------------
num = 0
lista = []
indice = 0

print "Introduce el número hasta donde quieres encontrar los primos: "
num = int(raw_input())-1

for i in range(0,num):
	lista.append(i+2)

criba_eratostenes(lista, num)

for i in range(0,len(lista)):
	print lista[i]
