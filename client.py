import publisher as pub
import subscriber_client as sub_client
import subscriber_ackn as sub_ackn
import threading
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.uix.button import Button
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screen import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image

from kivy.clock import Clock
import time
from functools import partial
import plyer
import db

# to change the kivy default settings we use this module config
from kivy.config import Config
     
# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False
Config.set('graphics', 'resizable', True)

was_thread_alive = [0]

class mainApp(MDApp):
    def build(self):
        self.screen = Screen()
        server = db.getServer()

        self.servidor = MDTextField(
            text =  server[1],
            pos_hint = {'center_x':0.5, 'center_y':0.8},
            size_hint_x = None,
            width = 300,
        )
        self.porta = MDTextField(
            text =  str(server[0]),
            pos_hint = {'center_x':0.5, 'center_y':0.7},
            size_hint_x = None,
            width = 300,
        )
        self.usuario = MDTextField(
            text = server[2],
            pos_hint = {'center_x':0.5, 'center_y':0.6},
            size_hint_x = None,
            width = 300,
        )
        self.senha = MDTextField(
            text =  server[3],
            password = True,
            pos_hint = {'center_x':0.5, 'center_y':0.5},
            size_hint_x = None,
            width = 300,
        )
        self.send = MDRectangleFlatButton(text = 'Enviar',size_hint = (.15,.05),pos_hint={'center_x':0.5, 'center_y':0.3}, on_release = self.btn_send)
        self.cancel = MDRectangleFlatButton(text = 'Cancelar',size_hint = (.15,.05),pos_hint={'center_x':0.5, 'center_y':0.2}, on_release = self.btn_cancel)
        self.settings = Button(background_normal = 'settings.png',background_down ='settings.png',size_hint = (0.09,0.1),pos_hint={'center_x':0.9, 'center_y':0.9}, on_release = self.btn_settings)

        self.b = MDRectangleFlatButton(
            text = "responder",
            size_hint = (0.1,0.1),
            pos_hint = {'center_x':0.5, 'center_y':0.5},
            opacity = 1,
            on_press=self.btn_click
        )
        if(server[4] == 0):
            self.screen.add_widget(self.servidor)
            self.screen.add_widget(self.porta)
            self.screen.add_widget(self.usuario)
            self.screen.add_widget(self.senha)
            self.screen.add_widget(self.send)
            self.screen.add_widget(self.cancel)
        else:
            print('else')
            self.screen.add_widget(self.b)
            self.screen.add_widget(self.settings)


        return self.screen
    
    def set_cad(self):
        print('set_cad')
        self.screen.add_widget(self.servidor)
        self.screen.add_widget(self.porta)
        self.screen.add_widget(self.usuario)
        self.screen.add_widget(self.senha)
        self.screen.add_widget(self.send)
        self.screen.add_widget(self.cancel)
        self.screen.remove_widget(self.b)
        self.screen.remove_widget(self.settings)

    def remove_cad(self):
        print('remove_cad')
        self.screen.remove_widget(self.servidor)
        self.screen.remove_widget(self.porta)
        self.screen.remove_widget(self.usuario)
        self.screen.remove_widget(self.senha)
        self.screen.remove_widget(self.send)
        self.screen.remove_widget(self.cancel)
        self.screen.add_widget(self.b)
        self.screen.add_widget(self.settings)

    def btn_send(self,b):
        try:
            int(self.porta.text)
        except:
            popupWindow = Popup(title="erro",content = Label(text ="Insira um valor valido para porta"),size_hint=(None,None),size = (400,400))
            popupWindow.open()
            return

        if(self.servidor.text == "" or self.usuario.text == "" or self.senha.text == ""):
            popupWindow = Popup(title="erro",content = Label(text ="Preencha todos os campos"),size_hint=(None,None),size = (400,400))
            popupWindow.open()
            return

        servidor = (int(self.porta.text),self.servidor.text,self.usuario.text,self.senha.text,1,int(self.porta.text))
        db.setServerBoo(servidor)

        self.remove_cad()

    def btn_cancel(self,b):
        self.remove_cad()

    def btn_settings(self,b):
        self.set_cad()

    def btn_click(self,b):
        self.is_calling = False
        pub.run('accept','accept')
        print('cliente: enviando accept')

    def t(self):
        print('aguardando topico client')
        comando = sub_client.run('client')
        print('aguardando ack')
        notification = plyer.notification.notify(title='Responder', message = comando)
        self.is_calling = True
        sub_ackn.run('ackn')
        print('ack recebido')
        self.is_calling = False
        print('ack recebido')
        notification = plyer.notification.notify(title='Já foi respondido', message = comando)
        
        th = threading.Thread(target = self.t)

        th.start()

    def isThreadAlive(self,*a):
        if(self.is_calling):
            try:
                self.screen.add_widget(self.b)
            except:
                pass
        else:
            self.screen.remove_widget(self.b)
            
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