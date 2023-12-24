import kivy
import numpy as np

kivy.require("2.1.0")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.graphics import Canvas, Color, Rectangle
from kivy.properties import ListProperty, StringProperty, ObjectProperty, NumericProperty

import random

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
        # Obtén los valores de nivel y mina      
        lanzar_juego = JuegoBuscamina()
        self.manager.current = "juego"
        return lanzar_juego
        
        
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

        self.nivel = 9  
        self.mina = 30
        
        self.crear_campo_minado()
         
    def crear_campo_minado(self):
        nivel = self.nivel
        minas = self.mina
        num_celdas = nivel**2
        #Generamos la posición de las minas de forma aleatoria
        for i in range(minas):
            self.minas.append(random.randint(0, num_celdas-1))
        #print(self.minas)
        
        #Asignamos a las celdas un false cuándo no hay minas true cuándo sí las hay
        self.celdas = self.minar_celdas(num_celdas, self.minas)
        #print(self.celdas)
        #Agregamos los widget con el Grid y los botones
        self.mostrar_campo(self.nivel)
        
        #print(self.celdas)
        
    def minar_celdas(self, num_celdas, minas):
        celdas = [1] * num_celdas
        for i in range(num_celdas):
            if i not in minas:
                celdas[i] = 0
        return celdas
  
    def mostrar_campo(self, nivel):
        self.bandera = False
        self.contenedor = Contenedor()
        self.volver = Volver()
        self.informacion = Informacion()
        self.campominado = CampoMinado()
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

        num_celdas = self.nivel**2
        
        # Crea el GridLayout
        grid_layout = GridLayout(
            rows=nivel,
            cols=nivel,  
            size_hint=(1, 1),
         )
        # Añade el GridLayout al BoxLayout
        self.campominado.add_widget(grid_layout)
        # Crea los botones
        botones = []
        for i in range(num_celdas):
            button = Button(
            text= str(i),
            size_hint=(1, 1),
            )
            #button.on_press(text = str(celdas[i]))
            button.bind(on_press=lambda x, i=i: self.abrir_boton(x, i))  # Usa bind() para pasar el botón como argumento
            
            botones.append(button)
            # Añade los botones al GridLayout
        for boton in botones:
            grid_layout.add_widget(boton)
        #print(self.nivel)
        #print(self.mina)
    
    def abrir_boton(self,boton, indice):
        valor_celda = int(self.celdas[indice])
        #boton.text = str(valor_celda)
        #print("El valor del indice es: "+ str(indice))
        #print("El valor del botón es: "+str(boton))

        # Acciones del juego (ejemplo básico):
        print(self.celdas)
        if self.celdas[valor_celda] == 1:
            print("self.celdas es: "+str(self.celdas))
            print("self.celdas[valor_celda] es: "+str(self.celdas[valor_celda]))
            boton.text = "1"
            # ¡Mina!          
            print("¡Has perdido!")
            # Implementar acciones para finalizar la partida
        else:
            print("self.celdas es: "+str(self.celdas))
            print("self.celdas[valor_celda] es: "+str(self.celdas[valor_celda]))
            boton.text = "0"
            #print(self.celdas)
            # Celda sin mina
            # Implementar acciones para descubrir celdas adyacentes,
            # actualizar el contador de minas restantes, etc.
                
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
    def build(self):
        # player = music()
        # playing_label = player.play_music()
        # print(playing_label)
        return MainWid()
    
if __name__ == '__main__':
    MainApp().run()