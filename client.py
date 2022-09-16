import publisher as pub
import subscriber as sub
import threading
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.textfield import MDTextField
from kivy.clock import Clock
import time
from functools import partial
import plyer

class mainApp(MDApp):
    def build(self):
        b = MDRectangleFlatButton(
            text = "responder",
            size_hint = (0.1,0.1),
            pos_hint = {'center_x':0.5, 'center_y':0.5},
            opacity = 1,
            on_press=self.btn_click
        )
        return b

    def btn_click(self,b):
        self.is_calling = False
        pub.run('accept','accept')
        print('cliente: enviando accept')

    def t(self):
        print('aguardando topico client')
        comando = sub.run('client')
        print('aguardando ack')
        notification = plyer.notification.notify(title='Responder', message = comando)
        self.is_calling = True
        sub.run('ack')
        print('ack recebido')
        self.is_calling = False
        print('ack recebido')
        notification = plyer.notification.notify(title='Já foi respondido', message = comando)
        
        th = threading.Thread(target = self.t)

        th.start()

    def isThreadAlive(self,*a):
        if(self.is_calling):
            self.root.opacity = 1
        else:
            self.root.opacity = 0

    def on_start(self):
        self.is_calling = False
        self.root.bind(on_press = self.btn_click)
        print('iniciando thread cliente')

        th = threading.Thread(target = self.t)

        th.start()
        Clock.schedule_interval(self.isThreadAlive,0.2)
    
    def on_stop(self):
        pub.disconnect()
        print('fechando')
        
mainApp().run()