import numpy
import random

# Lista de posiciones visitadas
visitados = []
matrizUsuario = []
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
    ceros = []
    ceros.append((fila, columna))
    cont = 0
    while len(ceros)>0:
        fila,columna = ceros.pop()
    #Si la casilla se puede destapar
    if not matriz[fila][columna] == matrizUsuario[fila][columna] and matriz[fila][columna] != 0:
        eleccionUsuario(fila, columna, str(matriz[fila][columna]),matrizUsuario)
    # Si no hay minas cerca, intento destapar las vecinas
    if matriz[fila][columna] == 0 and matriz[fila][columna] != matrizUsuario[fila][columna]:
        for fila2 in range(max(0, fila - 1), min(9, fila + 1) + 1):
            for columna2 in range(max(0, columna - 1), min(9, columna + 1) + 1):
                # Si la posición está dentro de los límites de la matriz
                if 0 <= fila2 < len(matriz) and 0 <= columna2 < len(matriz[0]):
                    if matriz[fila2][columna2] != 9:
                        if matriz[fila2][columna2] == 0:
                            eleccionUsuario(fila2, columna2, "0", matrizUsuario)
                            ceros.append((fila2, columna2))
                            cont+=1
                        else:
                            eleccionUsuario(fila2, columna2, matriz[fila2][columna2], matrizUsuario)
    recurrente(matriz, ceros, matrizUsuario)
    print("Entró a la llamada recurrente " +str(cont)+" veces")
    
    
def recurrente(matriz, ceros, matrizUsuario):
    for fila, columna in ceros:
        # Si la posición no se ha visitado anteriormente
        if (fila, columna) not in visitados:
            # Agrega la posición a la lista de visitados
            visitados.append((fila, columna))
            # Llama a la función recursiva
            recorrer_matriz_radial(matriz, fila, columna,matrizUsuario)
    
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
def matriz_usuario():
    print(matrizUsuario)
def mecanicaJuego():
    nivel = 9
    #Campo de juego coloca las bombas en las diferentes posiciones
    CampoJuego = crear_campo_minado(nivel, nivel, 0.1)
    print("Campo de juego")
    #mostrarMatriz(CampoJuego)
    #la matriz contar es solo para el programa, ya están reveladas las celdas
    matriz_con_contar = contar_1_alrededor(CampoJuego)
    print("La matriz privada:")
    mostrarMatriz(matriz_con_contar)
    
    matrizUsuario = [['-' for i in range(len(CampoJuego[0]))] for j in range(len(CampoJuego))]
    print("La matriz que se le muestra al usuario")
    matriz_usuario()
    
    x = int(input("Elije la fila: "))
    y = int(input("Elije la columna: "))
    
    #recorrer_matriz_radial(matriz_con_contar, x, y, matrizUsuario)
    
    
    while (CampoJuego[x][y] == 0):
        # if matriz_con_contar[x][y] == 0:
        #     recorrer_matriz_radial(matriz_con_contar, x, y, matrizUsuario)
        jugar(matriz_con_contar,x,y, matrizUsuario)
        print("La matriz privada:")
        mostrarMatriz(matriz_con_contar)
        print("La matriz que se le muestra al usuario")
        matriz_usuario()
        x = int(input("Elije la fila: "))
        y = int(input("Elije la columna: "))
        
    print("Perdiste")
    
        
        


mecanicaJuego()
