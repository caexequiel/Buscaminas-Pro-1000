from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.slider import MDSlider
from kivymd.uix.label import MDLabel
from kivy.clock import Clock

class PlayerScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.sound = SoundLoader.load('music/Music2.mp3')  # Load the music file

        # Create UI elements
        self.play_button = MDFlatButton(text="Play", on_press=self.play_music)
        self.pause_button = MDFlatButton(text="Pause", on_press=self.pause_music)
        self.stop_button = MDFlatButton(text="Stop", on_press=self.stop_music)
        self.volume_slider = MDSlider(min=0, max=1, value=0.5)
        self.position_slider = MDSlider(min=0, max=self.sound.length, value=0)
        self.time_label = MDLabel(text="0:00")

        # Add UI elements to the screen
        # ... (Use appropriate layout methods like add_widget)

    def play_music(self):
        self.sound.play()

        # Actualice el control deslizante de posición y la etiqueta de tiempo periódicamente
        Clock.schedule_interval(self.update_position, 1)

    def pause_music(self):
        self.sound.stop()
        Clock.unschedule(self.update_position)

    def stop_music(self):
        self.sound.stop()
        self.sound.seek(0)  # Rebobinar al principio
        Clock.unschedule(self.update_position)
        self.position_slider.value = 0
        self.time_label.text = "0:00"

    def update_position(self, dt):
        self.position_slider.value = self.sound.get_pos()
        time_text = self.format_time(self.sound.get_pos())
        self.time_label.text = time_text

    def format_time(self, time_in_seconds):
        minutes = int(time_in_seconds // 60)
        seconds = int(time_in_seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
  
    
class MusicPlayerApp(MDApp):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(PlayerScreen(name="player"))
        return screen_manager

if __name__ == "__main__":
    MusicPlayerApp().run()
