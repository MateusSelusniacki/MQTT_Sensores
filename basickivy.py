import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from notify import Notification

class MyApp(App):

    def build(self):
        return Label(text='Hello world')

    def on_start(self):
        Notification('what you want said').notify()

if __name__ == '__main__':
    MyApp().run()