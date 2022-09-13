import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label

import plyer
import publisher as pub
import subscriber as sub
import threading

class DemoApp(MDApp):
    def build(self):
        screen = Screen()
        self.theme_cls.primary_palette = "Green"
        self.button = MDRectangleFlatButton(text = 'Enviar',pos_hint={'center_x':0.5, 'center_y':0.3}, on_release = self.btn_click)
        self.codigo = MDTextField(
            hint_text =  "Codigo",
            pos_hint = {'center_x':0.5, 'center_y':0.4},
            size_hint_x = None,
            width = 300,
        )
        self.nome = MDTextField(
            hint_text =  "Nome",
            pos_hint = {'center_x':0.5, 'center_y':0.5},
            size_hint_x = None,
            width = 300,
        )
        self.numero = MDTextField(
            hint_text =  "Numero",
            pos_hint = {'center_x':0.5, 'center_y':0.6},
            size_hint_x = None,
            width = 300,
        )
        #self.comando = Builder.load_string(text_field)
        screen.add_widget(self.codigo)
        screen.add_widget(self.button)
        screen.add_widget(self.nome)
        screen.add_widget(self.numero)
        return screen

    def t(self):
        print('aguardando topico client')
        comando = sub.run('admin')
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

    def btn_click(self,b):
        try:
            int(self.numero.text)
        except:
            popupWindow = Popup(title="erro",content = Label(text ="numero invalido"),size_hint=(None,None),size = (400,400))
            popupWindow.open()
            return

        if(self.codigo.text == "" or self.nome.text == ""):
            popupWindow = Popup(title="erro",content = Label(text ="preencha todos os campos"),size_hint=(None,None),size = (400,400))
            popupWindow.open()
            return

        if(self.is_calling):
            self.is_calling = False
            comando = (self.codigo.text,int(self.numero.text),self.nome.text)
            pub.run('send_data',comando)

    def isThreadAlive(self,*a):
        if(self.is_calling):
            pass
        else:
            pass

    def on_start(self):
        self.is_calling = False
        print('iniciando thread admin')

        th = threading.Thread(target = self.t)

        th.start()
        Clock.schedule_interval(self.isThreadAlive,0.2)

    def get_text(self):
        return self.codigo.text

DemoApp().run()