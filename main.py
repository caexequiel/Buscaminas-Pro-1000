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
        #self.nivel = int(kwargs.get("nivel", 10))  # Valor por defecto 10
    def ir_a_juego(self, nivel, mina):
        datos = {"nivel": nivel, "mina": mina}
        lanzar_juego = JuegoBuscamina(**datos)
        lanzar_juego.crear_campo_minado(nivel, mina)
        return lanzar_juego
        
        
class JuegoBuscamina(Screen):
    minas_restantes = NumericProperty()
    cronometro = NumericProperty()
    #Esta es la forma correcta de recibir los argumentos desde otra clase
    nivel = NumericProperty(default=10) 
    mina = NumericProperty(default=10)
    superBox = ObjectProperty()
    def __init__(self,**kwargs):  # Agrega un argumento posicional "nivel"
        super(JuegoBuscamina, self).__init__(**kwargs)
        self.filas = []
        self.columnas = []
        self.minas = []
        self.celdas = []
        
        print(self.nivel)
        print(self.mina)
        self.mostrar_campo()  
    """  
    def on_pre_enter(self):
        #Agregamos un Box Contenedor
        self.superBox = self.ids.campominado #self.ids.contenedor.ids.campominado
        
        print(self.nivel)
        print(self.mina)
        #Agregamos un Box Contenedor
        self.superBox = self.ids.campominado #self.ids.contenedor.ids.campominado
        
        # Eliminamos los elementos del superBox
        self.superBox.clear_widgets()
        
        num_celdas = self.nivel**2
        #Crea el GridLayout
        grid_layout = GridLayout(
            rows= self.nivel,
            cols= self.nivel,  # Usa la propiedad 'cols' en lugar de 'columns'
            size_hint=(1, 1),
        )
        # Añade el GridLayout al BoxLayout
        self.superBox.add_widget(grid_layout)
        # Crea los botones
        botones = [] 
        for i in range(num_celdas):
            button = Button(
            text="{}".format(i + 1),
            size_hint=(1, 1),
            )
            botones.append(button)
        # Añade los botones al GridLayout
        for boton in botones:
            grid_layout.add_widget(boton)
        #self.mostrar_campo(nivel, self.superBox)
        """
    def crear_campo_minado(self, nivel, minas):
        num_celdas = nivel**2
        #Generamos la posición de las minas de forma aleatoria
        for i in range(minas):
            self.minas.append(random.randint(0, num_celdas-1))
        #print(self.minas)
        
        #Asignamos a las celdas un false cuándo no hay minas true cuándo sí las hay
        self.celdas = self.minar_celdas(num_celdas, self.minas)
        #Agregamos los widget con el Grid y los botones
        self.mostrar_campo()
        #print(self.celdas)
        
    def minar_celdas(self, num_celdas, minas):
        celdas = [1] * num_celdas
        for i in range(num_celdas):
            if i not in minas:
                celdas[i] = 0
        return celdas
  
    def mostrar_campo(self):
        self.contenedor = Contenedor()
        self.volver = Volver()
        self.informacion = Informacion()
        self.campominado = CampoMinado()
        
        self.add_widget(self.contenedor)
        self.contenedor.add_widget(self.informacion)
        self.contenedor.add_widget(self.campominado)
        self.contenedor.add_widget(self.volver)
        
        # Eliminamos los elementos del superBox
        #self.campominado.clear_widgets()
        
        
  
        # Changing the color of buttons 
        # Agregamos el botón volver
        bt_volver = Button(pos_hint = {'center_x': 1, 'center_y': 0.5},
            size_hint = (.3, 1),
            text = 'Volver',
            font_size = 20,
            background_color = (1,0,1,1))
        bt_volver1 = Button(pos_hint = {'center_x': 1, 'center_y': 0.5},
            size_hint = (.3, 1),
            text = 'Volver',
            font_size = 20,
            background_color = (1,0,1,1))
        bt_volver2 = Button(pos_hint = {'center_x': 1, 'center_y': 0.5},
            size_hint = (.3, 1),
            text = 'Volver',
            font_size = 20,
            background_color = (1,0,1,1))
        # volver.add_widget(bt_volver)  
        #self.informacion.add_widget(bt_volver)  
        #campominado.add_widget(bt_volver2)  
        #campominado.add_widget(bt_volver1)  

        
        
        
        
        # #Agregamos los widgets
        # self.add_widget(contenedor)
        # contenedor.add_widget(campominado)
        # contenedor.add_widget(informacion)
        # contenedor.add_widget(volver)
        # campominado.add_widget(superBox)
        
        num_celdas = self.nivel**2
        # Crea el GridLayout
        grid_layout = GridLayout(
            rows=self.nivel,
            cols=self.nivel,  # Usa la propiedad 'cols' en lugar de 'columns'
            size_hint=(1, 1),
        )
        # Añade el GridLayout al BoxLayout
        #superBox.add_widget(grid_layout)
        # Crea los botones
        botones = []
        for i in range(num_celdas):
            button = Button(
            text="{}".format(i + 1),
            size_hint=(1, 1),
            )
            botones.append(button)
        # Añade los botones al GridLayout
        for boton in botones:
            grid_layout.add_widget(boton)
            
        print(self.nivel)
        print(self.mina)
  
                
class Informacion(BoxLayout):
    None
class Contenedor(BoxLayout):
    None
class CampoMinado(BoxLayout):
    None
class Volver(BoxLayout):
    None
    
class MainApp(App):
    title = "Buscaminas Pro 1000"
    icon = 'img/mina.png'
    def build(self):
        player = music()
        playing_label = player.play_music()
        print(playing_label)
        return MainWid()
    
if __name__ == '__main__':
    MainApp().run()