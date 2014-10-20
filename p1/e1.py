#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# mini-juego adivinar un número entre el 1 y el 100
import random

#Inicializamos variables
num_intentos = 0
aleatorio = random.randint(0,100)
numero = -0


print ("Juego del azar")

while num_intentos < 10:
    num_intentos = num_intentos + 1
    print ("Elige un número del 1 al 100: ")
    numero = raw_input()
    numero = int(numero)

    if numero < aleatorio:
    	print ("El número introducido es menor")

    if numero > aleatorio:
    	print ("El número introducido es mayor")

    if numero == aleatorio:
    	break

if numero == aleatorio:
	print ("Has ganado campeon")

if numero != aleatorio:
	print ("jaa jaa")