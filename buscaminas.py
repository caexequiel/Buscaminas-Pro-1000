import numpy as np
import random

# Lista de posiciones visitadas
visitados = []
cerosTotales=[]
nivel = 4

class juegoBuscamina():
    def __init__(self, filas=5, columnas=5):
        #self.mecanicaJuego(self.nivel)

        self.matrizUsuario = [['[ ]' for i in range(nivel)] for j in range(nivel)]
        self.matriz_privada = [['[ ]' for i in range(nivel)] for j in range(nivel)]  
    def crear_campo_minado(self,n, m, proporcion):
        nivel = n
        matriz = [[0 for i in range(m)] for j in range(n)]
        for i in range(n):
            for j in range(m):
                if random.random() < proporcion:
                    matriz[i][j] = 1
        return matriz

    def contar_1_alrededor(self, matriz):
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
                    num_1_alrededor = "Bom"
                # Almacena el resultado
                if num_1_alrededor == 0:
                    num_1_alrededor = ""
                matriz2[x][y] = num_1_alrededor

        return matriz2
                
    def mostrarMatriz(self, matriz):
        matriz_auxiliar = np.copy(matriz)
        for i in range(len(matriz)):
            for j in range(len(matriz[0])):
                if matriz[i][j] == "":
                    matriz_auxiliar[i][j] = "0"
                print(matriz_auxiliar[i][j], end=" ")
            print() 

    def recorrer_matriz_radial(self, matriz, fila, columna):
        ceros = []
        ceros.append((fila, columna))
        
        #cerosTotales.append((fila, columna))
        while len(ceros)>0:
            fila,columna = ceros.pop()
        
        # Si la posición no se ha visitado anteriormente
        if (fila, columna) not in cerosTotales:
            # Agrega la posición a la lista de visitados
            cerosTotales.append((fila, columna))
            #Si la casilla se puede destapar
            if not matriz[fila][columna] == self.matrizUsuario[fila][columna] and matriz[fila][columna] != "":
                self.eleccionUsuario(fila, columna, str(matriz[fila][columna]))
            # Si no hay minas cerca, intento destapar las vecinas
            if matriz[fila][columna] == "" and matriz[fila][columna] != self.matrizUsuario[fila][columna]:
                for fila2 in range(max(0, fila - 1), min(nivel, fila + 1) + 1):
                    for columna2 in range(max(0, columna - 1), min(nivel, columna + 1) + 1):
                        # Si la posición está dentro de los límites de la matriz
                        if 0 <= fila2 < len(matriz) and 0 <= columna2 < len(matriz[0]):
                            if matriz[fila2][columna2] != 9:
                                if matriz[fila2][columna2] == "":
                                    self.eleccionUsuario(fila2, columna2, "")
                                    ceros.append((fila2, columna2))
                                                                
                                else:
                                    self.eleccionUsuario(fila2, columna2, matriz[fila2][columna2])
                
        #return cerosTotales
        self.recurrente(matriz, ceros)
        
    def recurrente(self, matriz, ceros):
        for fila, columna in ceros:
            # Si la posición no se ha visitado anteriormente
            if (fila, columna) not in visitados:
                # Agrega la posición a la lista de visitados
                visitados.append((fila, columna))
            
                # Llama a la función recursiva
                self.recorrer_matriz_radial(matriz, fila, columna)
    def matriz_usuario(self):
        return self.matrizUsuario 


    def jugar(self, matriz,x,y):
        if matriz[x][y] == "Bom":
            print("perdiste")
            self.eleccionUsuario(x,y, "Bom")
        if matriz[x][y] == "":
            self.recorrer_matriz_radial(matriz,x,y)  
            print("Llegó")#matriz2)          
        else:
            self.eleccionUsuario(x,y, str(matriz[x][y]))
        

    def eleccionUsuario(self,y,x, valor):
        self.matrizUsuario[y][x] = valor
        
"""    def mecanicaJuego(self, nivel):
        #Campo de juego coloca las bombas en las diferentes posiciones
        CampoJuego = self.crear_campo_minado(nivel, nivel, 0.1)
        #la matriz contar es solo para el programa, ya están reveladas las celdas
        self.matriz_privada = self.contar_1_alrededor(CampoJuego)


juego = juegoBuscamina()
"""
    
        