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
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.properties import ListProperty, StringProperty, ObjectProperty, NumericProperty


import random
nivel = 4
horas = 0
minutos = 0
segundos = 0
class Notificacion(Popup):
    def __init__(self, title, text, imagen):
        super(Notificacion, self).__init__()
        self.title = title             
        self.content = Label(text=text,
            size_hint = (0.8, 0.3),
            font_name = "font/broken_destroit.ttf",
            font_size = 40,
            #color = (0,0,0)
                             )
        self.size_hint = (0.8, 0.3)
        self.font_name = "font/broken_destroit.ttf"

        if imagen == "explosion":
            self.background = "img/explosion2.png"
            #self.background_color = (0, 0, 0 ,.5)
        if imagen == "ganaste":
            self.background = "img/ganaste.png"
            #self.background_color = (0, 0, 0 ,.5)
class Reproductor():
    def __init__(self, music_number=1):

        #self.music_file = f"music/music{music_number}.mp3"
        #self.music = SoundLoader.load(self.music_file)

        # Atributos
        self.music = None
        self.cancion_actual = None
    def volumen (self, vol):
        self.music.volume = vol  
    def reproducir(self, n_cancion):
        # Carga el archivo de audio
        #musica = "music/music{}.mp3".format(n_cancion)
        if type(n_cancion) == int:
            musica = "music/music{}.mp3".format(n_cancion)
        else:
            musica = n_cancion
        # Carga el archivo de audio
        try:
            self.music = SoundLoader.load(musica)
            self.volumen(0.3)
            self.music.play()
        except Exception as e:
            print("Error al cargar el archivo de audio:", e)
        # Maneja el error de forma adecuada, por ejemplo, mostrando un mensaje al usuario.
        print(musica)
        # Inicia la reproducción
        # Actualice el control deslizante de posición y la etiqueta de tiempo periódicamente     

    def cambiar_cancion(self, archivo):
        # Detiene la reproducción de la canción actual}
        self.music.stop()
        if self.music is not None:
            self.music.stop()
            
            
        # Carga el nuevo archivo de audio
        self.music = SoundLoader.load(archivo)
        # Inicia la reproducción
        self.volumen(0.3)
        self.music.play()
        
    def stop_music(self):
        self.music.stop()
        self.music.seek(0)  # Rebobinar al principio

    def pausar(self):
        # Pausa la reproducción
        self.music.stop()
        
    def play_music(self):
        self.music.play()   
        # Reanuda la reproducción

 
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
        #juego_buscaminas.mecanicaJuego(nivel)
        # Obtén los valores de nivel y mina      
        lanzar_juego = JuegoBuscamina()
        lanzar_juego.start()
        self.manager.current = "juego"
        #return lanzar_juego

class CronometroLabel(Label):
    None
        
class JuegoBuscamina(Screen):
    superBox = ObjectProperty()
    cronometro = 0
    horas = 0
    minutos = 0
    segundos = 0
    def __init__(self,**kwargs):  # Agrega un argumento posicional "nivel"
        super(JuegoBuscamina, self).__init__(**kwargs)
        self.filas = []
        self.columnas = []
        self.minas = []
        self.celdas = []
        self.matriz_privada = []
        self.matriz_usuario = []
        self.partida_en_juego = True
        self.bandera = False
        self.hay_bandera = True
        self.Laberl_Crono = CronometroLabel()
        self.banderas_colocadas = 0
        self.reproductor = Reproductor()

        # self.nivel = 9  
        # self.mina = 30
        #print(nivel)
        self.crear_campo_minado()  
    def increment_time(self, interval):
        global horas
        global minutos
        global segundos
        self.cronometro += 1
        segundos = self.cronometro
        if segundos >= 60:
            minutos += 1
            segundos = 0
        if minutos >= 60:
            horas += 1
            minutos = 0
        
        self.cronometro += 1
        self.Laberl_Crono.text = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
        #self.Laberl_Crono.text = str(self.cronometro)
        if self.partida_en_juego == False:
            self.Stop()
            
        #return self.cronometro
    def start(self):
        Clock.unschedule(self.increment_time)
        #self.cornometro(1)
        Clock.schedule_interval(self.increment_time, 1)
    def Stop(self):
        Clock.unschedule(self.increment_time)  # Pausa la función increment_time
    def crear_campo_minado(self):
        #self.partida_en_juego = False
        juego_buscaminas = MainApp.get_juego_buscaminas()
        juego_buscaminas.nivel = nivel
        CampoJuego = juego_buscaminas.crear_campo_minado(nivel, nivel, 0.1)
        #Creamos la matriz privada
        self.matriz_privada = juego_buscaminas.contar_1_alrededor(CampoJuego)
        
        
        self.mostrar_campo(self.matriz_privada)
        
        #print(self.celdas)
    def mostrar_campo(self, matriz_privada):        
        # Eliminamos los widgets existentes
        self.clear_widgets()
        
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
                  
        #Agregamos la sección información----------------------------
        self.Laberl_Crono = Label()
        self.Label_minas_restantes = Label()
        self.BT_bandera = Button(
            text= "",
            size_hint=(None, None),
            color = (1,1,1,1),
            
            font_size= 50,
            background_normal = 'img/mina2.png',
            #background_color = (0,0,0,1),
            )
        
        #Cronómetro--------------------------
        #agregamos el texto y las funciones al button
        self.Laberl_Crono.text = "Tiempo"
        self.Laberl_Crono.font_name = "font/norwester.otf"
        self.Laberl_Crono.font_size = 30
        self.Laberl_Crono.color = (0,0,0,1)
        
        
        ################################################
        self.total_minas = self.contar_valor("Bom",self.matriz_privada)
        self.banderas_colocadas = self.contar_valor("Ban",self.matriz_usuario)
        self.Label_minas_restantes.text = "Minas: "+str(self.total_minas-self.banderas_colocadas)
        self.Label_minas_restantes.color = (0,0,0,1)
        self.Label_minas_restantes.font_name = "font/norwester.otf"
        self.Label_minas_restantes.font_size = 30
        self.BT_bandera.bind(on_press = self.boton_bandera)
        
        
        self.Box_info = BoxLayout()
        self.informacion.add_widget(self.Box_info)
        self.Box_info.add_widget(self.Laberl_Crono)
        self.Box_info.add_widget(self.BT_bandera)
        self.Box_info.add_widget(self.Label_minas_restantes)
        self.Box_info.orientation = 'horizontal'
        #Sección Grid Layout---------------------------------------
        num_celdas = nivel**2
        
        # Crea el GridLayout
        grid_layout = GridLayout(
            rows=nivel,
            cols=nivel,  
            size_hint=(None, None),
            #size_hint=(1, 1),
            spacing = 2,
            padding = 2,
         )
        grid_layout.bind(minimum_height=grid_layout.setter('height'),minimum_width=grid_layout.setter('width'))
        
        ### Programamos el zoom ####################################
        
      
        
        grid_layout.id = "id_grid_layout"
        
        #Creamos el ScrollView###################################
        scrollview = ScrollView(size_hint=(1, 1))
        # Añade el GridLayout al ScrollView
        scrollview.add_widget(grid_layout)
        # Añade el GridLayout al BoxLayout
        #self.campominado.add_widget(grid_layout)
        # Añade el ScrollView al BoxLayout
        self.campominado.add_widget(scrollview)
              
        scrollview.bind(on_scroll=self.on_scroll)        
        #Vamos a guardar los datos de la matriz privada en un array
        array_matriz = []
        # Bucle for anidado para recorrer todos los elementos de la matriz
        for fila in matriz_privada:
            for elemento in fila:
                array_matriz.append(elemento)

        # Crea los botones ######################################### 
        botones = []
        for i in range(num_celdas):
            button = Button(
            text= "",#str(i),##str(array_matriz[i]),
            size_hint=(1, 1),
            size_hint_max=(None, None),
            size_hint_min=(50, 50),
            background_color = "#7BB2FA",
            background_normal = "#7BB2FA",           
            )
            button.id = str(i)
            #button.on_press(text = str(celdas[i]))
            button.bind(on_press=lambda boton, i=i: self.abrir_boton(boton, i,matriz_privada, grid_layout))  # Usa bind() para pasar el botón como argumento
            
            botones.append(button)
            # Añade los botones al GridLayout
        for boton in botones:
            grid_layout.add_widget(boton)
        
        
        return self.Laberl_Crono
                                
    def on_scroll(self, scroll_view, touch_pos, scroll_delta):
        # Calcula el factor de escala
        scale_factor = 1.0 + scroll_delta.y * 0.01

        # Actualiza el tamaño de los botones
        for button in self.botones:
            button.size_hint_x *= scale_factor
            button.size_hint_y *= scale_factor
    
    def boton_bandera(self,instance):  
        """Para que tu botón haga self.bandera = True cuando se presiona una vez y 
        self.bandera = False cuando se lo presiona otra vez, puedes utilizar una variable de estado."""
        self.bandera = not self.bandera
        if self.bandera:
            self.BT_bandera.text = ""
            img_path = 'img/bandera2.png'
        else:
            img_path = 'img/mina2.png'
            self.BT_bandera.text = ""
        # Establecer la imagen como fondo del botón
        self.BT_bandera.background_normal = img_path
    def abrir_boton(self,boton, indice, matriz_privada, grid_layout):
        #Comenzamos a correr el tiempo
        self.start()
        
        #Colocamos musica
        self.reproductor.reproducir("music/boton.mp3")
        
        juego_buscaminas = MainApp.get_juego_buscaminas()
        
        # Obtener las coordenadas del botón
        x = (indice)//(nivel) #Columna
        y = (indice) - (x*nivel) #Fila

        if self.bandera == False:
            boton.disabled = True
            boton.text = str(matriz_privada[x][y])
            self.formatoCelda(boton)
            todosCeros = []
            if boton.text == "":
                todosCeros = juego_buscaminas.recorrer_matriz_radial(matriz_privada,y,x)
                self.pintarCeros(juego_buscaminas,grid_layout,self.matriz_usuario)
            if boton.text == "Bom": 
                print("¡Has perdido!")
                self.perdiste(juego_buscaminas, grid_layout,matriz_privada)  
            else:
                None
                #print("¡Sigue jugando!")
            
            juego_buscaminas.eleccionUsuario(x,y,boton.text)
        if self.bandera == True:
            self.hay_bandera = not self.hay_bandera
            if self.hay_bandera:
                self.banderas_colocadas += 1
                img_path = "img/bandera.png"
                # Establecer la imagen como fondo del botón
                boton.background_normal = img_path
                juego_buscaminas.eleccionUsuario(x,y,"Ban")
            else:
                # Quitar la imagen del botón
                boton.background_normal = ""
                self.banderas_colocadas -= 1
                juego_buscaminas.eleccionUsuario(x,y,"[ ]")
        
        self.matriz_usuario = juego_buscaminas.matriz_usuario() 
        #Mostramos las matrices
        print("La matriz privada es: ")
        resultado = self.recorrerMatriz()
        if resultado:
            self.pintarCeros(juego_buscaminas,grid_layout,matriz_privada)
        print("\nLa matriz privada es:") 
        juego_buscaminas.mostrarMatriz(matriz_privada)   
        print("\nLa matriz del jugador es:") 
        juego_buscaminas.mostrarMatriz(self.matriz_usuario)   
    def pintarCeros(self, juego_buscaminas, grid_layout,matriz):
        #ids = {widget.id: widget for widget in grid_layout.walk() if hasattr(widget, 'id')} # Usamos 'walk()' para recorrer todos los widgets en el grid_layout y filtramos solo los widgets cuyos ids están definidos
        #print("Los ids son: "+str(ids))
        #print("LLegó acá")
        juego_buscaminas.mostrarMatriz(matriz)
        for x in range(len(matriz)):
            for y in range(len(matriz[0])):
                #print(matriz[x][y], end=" ")
                #print(matriz[n])
                
                if str(matriz[x][y]) != "[ ]":
                    indice = (y+ (x*nivel)) #Fila
                    #print(indice)
                    boton = grid_layout.children[(nivel**2-1)-indice]
                    boton.text = str(matriz[x][y])
                    #print(boton.text)
                    self.formatoCelda(boton)                 
    def formatoCelda(self, boton):
        boton.disabled_opacity: 1
        boton.disabled = True
        if boton.text == '-':
            boton.background_color = "#40ACFF"
            boton.color = "#40ACFF"
        if boton.text == '':
            boton.text == ""
            boton.color = "#40ACFF"
            boton.background_color = "#40ACFF"
        if boton.text == "1":
            boton.color = "#FFA741"
            boton.background_color = "#FAF469"
        if boton.text == "2":
            boton.color = "#DB8F37"
            boton.background_color = "#F99532"
        if boton.text == "3":
            boton.color = "#DB8F37"
            boton.background_color = "#FA5926"
        if boton.text == 'Bom':
            boton.disabled = False
            #boton.text = ""
            # Ruta de la imagen
            img_path = 'img/mina.png'
            boton.background_color = 0,0,0,1
            # Establecer la imagen como fondo del botón
            boton.background_normal = img_path                  
        else:
            boton.disabled_color = "#FA7601"
            boton.color = "#613F18"
        boton.font_size = 25
        boton.font_name = "font/broken_destroit.ttf"
    def eliminar_widgets(self):
        # Eliminamos los widgets existentes
        if self.partida_en_juego == False:
            if self.children:
                for child in self.children[:]:
                    self.remove_widget(child)
            self.crear_campo_minado() 
            self.partida_en_juego = True
        
        #print("Entró")
    def desabilitar_boton(self,boton):
        boton.background_color = (1, 0, 1, 1)
        #boton.disabled = True
        #Cambiamos el color del botón
        boton.disabled_color = "#ffffff"
        boton.disabled_opacity: 0
    def contar_valor(self,valor, matriz):
        contador = 0
        for x in range(len(matriz)):
            for y in range(len(matriz[0])):
                if str(matriz[x][y]) == valor:
                    contador += 1   
        return contador       
    def recorrerMatriz(self):
        matriz_auxiliar = np.copy(self.matriz_privada)
        for x in range(len(self.matriz_usuario)):
            for y in range(len(self.matriz_usuario)):
                if str(self.matriz_usuario) != "[ ]": 
                    if str(matriz_auxiliar[x][y]) == "Bom":
                        matriz_auxiliar[x][y] = "Ban"
                    if (matriz_auxiliar == self.matriz_usuario).all():
                        # Hacer algo si todos los elementos de las matrices son iguales
                        print("Las matrices son iguales")
                        self.ganaste()
                        matriz_auxiliar = []
                        self.cronometro = 0
                        return True
                    #print("Matriz auxiliar "+matriz_auxiliar[x][y])
                    #print("Matriz usuario "+str(self.matriz_usuario[x][y]))
                else:
                    #print("Continúa jugando")
                    return False
        if self.partida_en_juego == False:
            matriz_auxiliar = []
    def perdiste(self,juego_buscaminas, grid_layout,matriz_privada):
        self.pintarCeros(juego_buscaminas,grid_layout,matriz_privada)
        self.Stop()
        popup = Notificacion(title='Qué lástima!', text='Has pisado un mina', imagen = "explosion")
        popup.open()
        self.partida_en_juego = False
        self.reproductor.reproducir("music/explosion.mp3")
    def ganaste(self):
        print(" Entró a ganaste")
        self.Stop()
        popup = Notificacion(title='Buenísimo!', text='Has ganado el juego', imagen = "ganaste")
        popup.open()
        self.partida_en_juego = False
        
        self.reproductor.cambiar_cancion("music/win.mp3")
        
        
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
    size = (1000, 1000)
    @staticmethod
    def get_juego_buscaminas():
        if not hasattr(MainApp, "_juego_buscaminas"):
            MainApp._juego_buscaminas = bm.juegoBuscamina()
        return MainApp._juego_buscaminas
    def build(self):
        buscaminas = bm.juegoBuscamina()
        reproductor = Reproductor()
        reproductor.reproducir(1)
        return MainWid()
    
if __name__ == '__main__':
    MainApp().run()