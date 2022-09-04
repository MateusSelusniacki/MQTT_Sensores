import subscriber as mqtt
import publisher as pub
import subscriber as sub
import threading
from kivy.app import App
from kivy.uix.button import Button
import time

class mainApp(App):
    def build(self):
        b = Button(
            text = "responder",
            size_hint = (0.1,0.1),
            opacity = 0,
            on_press=self.btn_click
        )
        b.pos_hint['x'] = 0.5
        b.pos_hint['y'] = 0.5
        return b

    def t(self):
        self.is_calling = True
        mqtt.run('client')
        self.root.opacity = 1

    def btn_click(self,b):
        pub.run('accept','accept')
        print('cliente: enviando accept')
        sub.run('ack')
        print('ack recebido')

        self.root.opacity = 0
        self.is_calling = False

        th = threading.Thread(target = self.t)

        th.start()

    def on_start(self):
        self.is_calling = False
        self.root.bind(on_press = self.btn_click)
        print('iniciando thread cliente')
        th = threading.Thread(target = self.t)

        th.start()
        
    '''def on_start(self):
        self.root.bind(on_press = self.btn_click)
        print('iniciando thread cliente')
        th = threading.Thread(target = self.t)

        th.start()'''
mainApp().run()