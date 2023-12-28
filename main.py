"""Too funcional 28/12/2023"""
import kivy
import numpy as np
#Importamos el juego que creamos
import buscaminas as bm

kivy.require("2.1.0")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.graphics import Canvas, Color, Rectangle
from kivy.properties import ListProperty, StringProperty, ObjectProperty, NumericProperty

import random
nivel = 10

class Notificacion(Popup):
    def __init__(self, title, text):
        super(Notificacion, self).__init__()
        self.title = title
        self.content = Label(text=text)
        self.size_hint = (0.8, 0.3)
class music():
    def __init__(self, music_number=1):
        self.music_number = music_number
        self.music_file = f"music/music{music_number}.mp3"
        self.music = SoundLoader.load(self.music_file)
        self.play_time = 0

    def on_music_end(self):
        self.music_number += 1
        # Logic to play the next music or perform other actions when current music ends
        player = music()
        playing_label = player.play_music(self.music_number)
        
    def play_music(self):
        self.music.play()
        
class MainWid(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    

class Niveles(Screen):
    
    def __init__(self, **kwargs):
        super(Niveles, self).__init__(**kwargs)
    def ir_a_juego(self, nivel, mina):
        nivel = nivel
        
        #buscaminas.mecanicaJuego(nivel)
        # Llamamos al módulo buscaminas
        juego_buscaminas = MainApp.get_juego_buscaminas()
        juego_buscaminas.mecanicaJuego(nivel)
        # Obtén los valores de nivel y mina      
        lanzar_juego = JuegoBuscamina()
        
        self.manager.current = "juego"
        #return lanzar_juego
        
        
class JuegoBuscamina(Screen):
    minas_restantes = NumericProperty()
    cronometro = NumericProperty()

    superBox = ObjectProperty()
    def __init__(self,**kwargs):  # Agrega un argumento posicional "nivel"
        super(JuegoBuscamina, self).__init__(**kwargs)
        self.filas = []
        self.columnas = []
        self.minas = []
        self.celdas = []

        # self.nivel = 9  
        # self.mina = 30
        #print(nivel)
        self.crear_campo_minado()
         
    def crear_campo_minado(self):
        juego_buscaminas = MainApp.get_juego_buscaminas()
        CampoJuego = juego_buscaminas.crear_campo_minado(nivel, nivel, 0.1)
        #Creamos la matriz privada
        matriz_privada = juego_buscaminas.contar_1_alrededor(CampoJuego)
        
        self.mostrar_campo(matriz_privada)
        
        #print(self.celdas)
    def mostrar_campo(self, matriz_privada):
        
        self.bandera = False
        self.contenedor = Contenedor()
        self.volver = Volver()
        self.informacion = Informacion()
        self.campominado = CampoMinado()

        #Agregamos los id
        self.volver.id = "id_volver"
        self.informacion.id = "id_informacion"
        self.contenedor.id = "contenedor"
        self.campominado.id ="campo"
        #Creamos el BoxLayout
        self.box_layout = BoxLayout(
            orientation="vertical"
        )
        #Agregamos los widgets
        self.box_layout.add_widget(self.informacion)
        self.box_layout.add_widget(self.campominado)
        self.box_layout.add_widget(self.volver)
        self.contenedor.add_widget(self.box_layout)
        self.add_widget(self.contenedor)
          
        # Eliminamos los elementos del superBox
        self.campominado.clear_widgets()

        num_celdas = nivel**2
        
        # Crea el GridLayout
        grid_layout = GridLayout(
            rows=nivel,
            cols=nivel,  
            size_hint=(1, 1),
         )
        grid_layout.id = "id_grid_layout"

        # Añade el GridLayout al BoxLayout
        self.campominado.add_widget(grid_layout)
        
        #Vamos a guardar los datos de la matriz privada en un array
        array_matriz = []
        # Bucle for anidado para recorrer todos los elementos de la matriz
        for fila in matriz_privada:
            for elemento in fila:
                array_matriz.append(elemento)

        # Crea los botones  
        botones = []
        for i in range(num_celdas):
            button = Button(
            text= "",#str(i),##str(array_matriz[i]),
            size_hint=(1, 1),
            )
            button.id = str(i)
            #button.on_press(text = str(celdas[i]))
            button.bind(on_press=lambda boton, i=i: self.abrir_boton(boton, i,matriz_privada, grid_layout))  # Usa bind() para pasar el botón como argumento
            
            botones.append(button)
            # Añade los botones al GridLayout
        for boton in botones:
            grid_layout.add_widget(boton)

        
    
    def abrir_boton(self,boton, indice, matriz_privada, grid_layout):
        print("El índice del botón presionado es: "+str(indice))
        juego_buscaminas = MainApp.get_juego_buscaminas()
        juego_buscaminas.mostrarMatriz(matriz_privada)
        # Obtener las coordenadas del botón
        x = (indice)//(nivel) #Columna
        y = (indice) - (x*nivel) #Fila
        #print(x + y)
        #print("El índice es: "+str(indice))

        boton.text = str(matriz_privada[x][y])
        #print(boton.text)
        
        todosCeros = []
        if boton.text == "0":
            todosCeros = juego_buscaminas.recorrer_matriz_radial(matriz_privada,y,x)

        if boton.text == "b": 
            # Ruta de la imagen
            img_path = 'Buscaminas-Pro-1000-main/img/mina.png'
            boton.text = ""
            # Establecer la imagen como fondo del botón
            boton.background_normal = img_path
            # Redimensionar la imagen
            self.perdiste()  
            print("¡Has perdido!")
            # Implementar acciones para finalizar la partida
            juego_buscaminas.eleccionUsuario(x,y,"b")
        else:
            juego_buscaminas.eleccionUsuario(x,y,boton.text)
            print("¡Sigue jugando!")
        self.pintarCeros(juego_buscaminas,grid_layout)
        #self.desabilitar_boton(boton)
    def pintarCeros(self, juego_buscaminas, grid_layout):
        
        #ids = {widget.id: widget for widget in grid_layout.walk() if hasattr(widget, 'id')} # Usamos 'walk()' para recorrer todos los widgets en el grid_layout y filtramos solo los widgets cuyos ids están definidos
        #print("Los ids son: "+str(ids))
        matriz_usuario = juego_buscaminas.matriz_usuario()
        #print("LLegó acá")
        juego_buscaminas.mostrarMatriz(matriz_usuario)
        for x in range(len(matriz_usuario)):
            for y in range(len(matriz_usuario[0])):
                #print(matriz_usuario[x][y], end=" ")
                #print(matriz_usuario[n])
                if str(matriz_usuario[x][y]) != "[ ]":
                    indice = (y+ (x*nivel)) #Fila
                    #print(indice)
                    boton = grid_layout.children[99-indice]
                    #print(indice)
                    boton.text = str(matriz_usuario[x][y])
                    print(boton.text)
                    boton.disabled = True
                    if boton.text == "-":
                        boton.background_color = 0,0,1,1
                    if boton.text == "1":
                        boton.background_color = .3,0,0,1
                    if boton.text == "2":
                        boton.background_color = .5,0,0,1
                    if boton.text == "3":
                        boton.background_color = .7,0,0,1
                    if boton.text == "":
                        None
                    else:
                        boton.disabled_color = .7,0,0,1
                    boton.color = 0,0,0,1
                        #boton.background_color = 1,0,0,1
                    #print("El índice "+str(indice)+" el id del button: "+str(boton.id))
                    #self.desabilitar_boton(boton)
                #boton.text = str(matriz_usuario[n])
                #self.encontrar_widget_por_id(grid_layout, indice)
            #print()
    def encontrar_widget_por_id(self, grid_layout, id_buscado):
        ids = {widget.id: widget for widget in grid_layout.walk() if hasattr(widget, 'id')}
        print("Los ids son: "+str(list(ids.keys())))
        

    def perdiste(self):
        popup = Notificacion(title='Qué lástima!', text='Has pisado un mina O_o')
        popup.open()
        #self.remove_widgets()
    def remove_widgets(self):
        self.clear_widgets()
    def desabilitar_boton(self,boton):
        boton.background_color = (1, 0, 1, 1)
        #boton.disabled = True
        #Cambiamos el color del botón
        boton.disabled_color = "#ffffff"
        boton.disabled_opacity: 0
        # Establece el color de fondo del botón deshabilitado
        """if boton.text == "0":
            boton.background_color = (1, 0, 1, 1)   
        if boton.text != "0":
            boton.background_color = (0, 1, 0, 1)  """

                
class Informacion(Screen,BoxLayout):
    None
class Contenedor(Screen,BoxLayout):
    None
class CampoMinado(Screen,BoxLayout):
    None
class Volver(Screen,BoxLayout):
    None
    
class MainApp(App):
    title = "Buscaminas Pro 1000"
    icon = 'img/mina.png'
    @staticmethod
    def get_juego_buscaminas():
        if not hasattr(MainApp, "_juego_buscaminas"):
            MainApp._juego_buscaminas = bm.juegoBuscamina()
        return MainApp._juego_buscaminas
    def build(self):
        buscaminas = bm.juegoBuscamina()
        # player = music()
        # playing_label = player.play_music()
        # print(playing_label)
        return MainWid()
    
if __name__ == '__main__':
    MainApp().run()