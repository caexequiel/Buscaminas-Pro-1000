import numpy
import random


def crear_campo_minado(n, m, proporcion):
    matriz = [[0 for i in range(m)] for j in range(n)]
    for i in range(n):
        for j in range(m):
            if random.random() < proporcion:
                matriz[i][j] = 1
    return matriz

def contar_1_alrededor(matriz):
    matriz2 = [[0 for i in range(len(matriz[0]))] for j in range(len(matriz))]
    for x in range(len(matriz)):
        for y in range(len(matriz[0])):
            # Inicializa el número de 1 a su alrededor en 0
            
            num_1_alrededor = 0
            if matriz[x][y] != 1:
                # Verifica los elementos adyacentes
                for di in range(-1, 2):
                    for dj in range(-1, 2):              
                        if 0 <= x + di < len(matriz) and 0 <= y + dj < len(matriz[0]):
                            if matriz[x + di][y + dj] == 1:
                                num_1_alrededor += 1
            else:
                num_1_alrededor = "b"
            # Almacena el resultado
            matriz2[x][y] = num_1_alrededor

    return matriz2
            
def mostrarMatriz(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            print(matriz[i][j], end=" ")
        print() 
       
def recorrer_matriz_radial(matriz, fila, columna,matrizUsuario):
    # Lista de posiciones encontradas
    posiciones_encontradas = []
    # Recorre las celdas adyacentes
    for fila_adyacente in range(fila - 1, fila + 2):
        for columna_adyacente in range(columna - 1, columna + 2):
            # Si la posición adyacente está dentro de la matriz
            if 0 <= fila_adyacente < len(matriz) and 0 <= columna_adyacente < len(matriz[0]):
                # Si la celda adyacente tiene valor cero
                if matriz[fila_adyacente][columna_adyacente] == 0:
                    # Toma la celda adyacente como nueva posición central
                    fila = fila_adyacente
                    columna = columna_adyacente
                    #guardamos la elección del usuario
                    eleccionUsuario(fila,columna, "-",matrizUsuario)
                    
                    
                # Si el valor en la posición adyacente es distinto de 0
                if matriz[fila_adyacente][columna_adyacente] != 0:
                    # Agrega la posición a la lista de posiciones encontradas
                    eleccionUsuario(fila_adyacente,columna_adyacente, matriz[fila_adyacente][columna_adyacente],matrizUsuario)
                    posiciones_encontradas.append((fila_adyacente, columna_adyacente))

    # Devuelve la lista de posiciones encontradas
    print(posiciones_encontradas)
    return posiciones_encontradas

def jugar(matriz,x,y, matrizUsuario):
    if matriz[x][y] == "b":
        print("perdiste")
        eleccionUsuario(x,y, "B",matrizUsuario)
    if matriz[x][y] == 0:
        recorrer_matriz_radial(matriz,x,y,matrizUsuario)  
        print("Llegó")#matriz2)          
    else:
        eleccionUsuario(x,y, str(matriz[x][y]),matrizUsuario)
    

def eleccionUsuario(x,y, valor, matrizUsuario):
    matrizUsuario[x][y] = valor
    
def mecanicaJuego():
    nivel = 9
    #Campo de juego coloca las bombas en las diferentes posiciones
    CampoJuego = crear_campo_minado(nivel, nivel, 0.1)
    print("Campo de juego")
    mostrarMatriz(CampoJuego)
    #la matriz contar es solo para el programa, ya están reveladas las celdas
    matriz_con_contar = contar_1_alrededor(CampoJuego)
    print("La matriz privada:")
    mostrarMatriz(matriz_con_contar)
    
    matrizUsuario = [[0 for i in range(len(CampoJuego[0]))] for j in range(len(CampoJuego))]
    print("La matriz que se le muestra al usuario")
    mostrarMatriz(matrizUsuario)
    
    x = int(input("Elije la fila: "))
    y = int(input("Elije la columna: "))
    
    #recorrer_matriz_radial(matriz_con_contar, x, y, matrizUsuario)
    
    
    while (CampoJuego[x][y] == 0):
        if matriz_con_contar[x][y] == 0:
            recorrer_matriz_radial(matriz_con_contar, x, y, matrizUsuario)
    
        #jugar(matriz_con_contar,x,y, matrizUsuario)
        print("La matriz privada:")
        mostrarMatriz(matriz_con_contar)
        x = int(input("Elije la fila: "))
        y = int(input("Elije la columna: "))
        print("La matriz que se le muestra al usuario")
        mostrarMatriz(matrizUsuario)
    print("Perdiste")
    
        
        


mecanicaJuego()
