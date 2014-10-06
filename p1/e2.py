#Ordenacion
import random
import time

#Funciones
def ordenar_burbuja(matriz,tam):
    for i in range(1,tam):
        for j in range(0,tam-i):
            if(matriz[j] > matriz[j+1]):
                k = matriz[j+1]
                matriz[j+1] = matriz[j]
                matriz[j] = k;

def ordenar_seleccion(matriz,tam):
    for i in range(0,tam-1):
        min=i
        for j in range(i+1,tam):
            if matriz[min] > matriz[j]:
                min=j
        aux=matriz[min]
        matriz[min]=matriz[i]
        matriz[i]=aux

#Variables
lista=[]
cn=int(raw_input("Cantidad de numeros a ingresar: "))

for i in range(0,cn):
    lista.append(int(random.randint(0,100)))

inicio_burbuja = time.time()
ordenar_burbuja(lista,cn)
fin_burbuja = time.time()
tiempo_total_burbuja = fin_burbuja - inicio_burbuja
print ("El timpo que tarda la funcion de ordenado por burbuja es de ", tiempo_total_burbuja)


inicio_seleccion = time.time()
ordenar_seleccion(lista,cn)
fin_seleccion = time.time()
tiempo_total_seleccion = fin_seleccion - inicio_seleccion
print ("El timpo que tarda la funcion de ordenado por seleccion es de ", tiempo_total_seleccion)


