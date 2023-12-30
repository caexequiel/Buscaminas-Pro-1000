import kivy  
       
from kivy.app import App 
     
kivy.require('1.9.0')
 
from kivy.uix.label import Label
 
from kivy.clock import Clock
class ClockDemo(App):
 
    count = 0
 
    def build(self):
       self.myLabel = Label(text ='Waiting for updates...')
 
       
       Clock.schedule_interval(self.Callback_Clock, 1)
        
       return self.myLabel
 
    def Callback_Clock(self, dt):
        self.count = self.count + 1
        self.myLabel.text = "Updated % d...times"% self.count
 
        
if __name__ == '__main__':
    ClockDemo().run()