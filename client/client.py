import publisher as pub
import subscriber_client as sub_client
import subscriber_ackn as sub_ackn
import subscriber_ackn2 as sub_ackn2
import threading
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.uix.button import Button
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screen import Screen
from kivy.uix.popup import Popup
from kivymd.uix.label import MDLabel
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

broker_db = db.getServer()[0]

pub.broker = broker_db
sub_client.broker = broker_db
sub_ackn.broker = broker_db
sub_ackn2.broker = broker_db

print('broker_db',broker_db)

was_thread_alive = [0]

class mainApp(MDApp):
    def create_main_widget(self):
        self.IdentfControle = MDTextField(
            hint_text =  "identificador do Controle",
            pos_hint = {'center_x':0.5, 'center_y':0.8},
            size_hint_x = None,
            width = 300,
            disabled = True
        )
        
        self.CodItem = MDTextField(
            hint_text =  "Codigo do Item",
            pos_hint = {'center_x':0.5, 'center_y':0.7},
            size_hint_x = None,
            width = 300,
            disabled = True
        )
        
        self.NomeControle = MDTextField(
            hint_text =  "Nome",
            pos_hint = {'center_x':0.5, 'center_y':0.6},
            size_hint_x = None,
            width = 300,
            disabled = True
        )
        self.Descricao = MDTextField(
            hint_text =  "Descrição",
            pos_hint = {'center_x':0.5, 'center_y':0.5},
            size_hint_x = None,
            width = 300,
            disabled = True
        )
        
        self.CodControle = MDTextField(
            hint_text =  "Codigo do Controle",
            pos_hint = {'center_x':0.5, 'center_y':0.4},
            size_hint_x = None,
            width = 300,
            disabled = True
        )
        self.b = MDRectangleFlatButton(
            text = "responder",
            size_hint = (.15,.05),
            pos_hint={'center_x':0.5, 'center_y':0.3},
            opacity = 1,
            on_press=self.btn_click
        )
        
        self.label_conectado = MDLabel(text = "Conectado",pos_hint={'center_x':0.8,'center_y':0.02})
        self.settings = Button(background_normal = 'settings.png',background_down ='settings.png',size_hint = (0.1,0.05),pos_hint={'center_x':0.9, 'center_y':0.9}, on_release = self.btn_settings)
        
        self.label_falha = MDLabel(text = "",pos_hint = {'center_x':0.9,'center_y':0.5})
        
    def create_server_widgets(self):
        self.server = db.server
        self.broker = MDTextField(
            text =  self.server[0],
            pos_hint = {'center_x':0.5, 'center_y':0.8},
            size_hint_x = None,
            width = 300
        )
        self.send = MDRectangleFlatButton(text = 'Enviar',size_hint = (.15,.05),pos_hint={'center_x':0.5, 'center_y':0.3}, on_release = self.btn_send)
        self.cancel = MDRectangleFlatButton(text = 'Cancelar',size_hint = (.15,.05),pos_hint={'center_x':0.5, 'center_y':0.2}, on_release = self.btn_cancel)
        
    def build(self):
        self.screen = Screen()
        self.create_main_widget()
        self.create_server_widgets()

        self.screen.add_widget(self.label_falha)

        if(self.server[1] == 0):
            self.screen.add_widget(self.broker)
            self.screen.add_widget(self.send)
            self.screen.add_widget(self.cancel)
        else:
            self.screen.add_widget(self.label_conectado)
            self.screen.add_widget(self.settings)

        return self.screen
    
    def set_cad(self):
        print('set_cad')
        self.screen.add_widget(self.broker)
        self.screen.add_widget(self.send)
        self.screen.add_widget(self.cancel)
        self.screen.remove_widget(self.IdentfControle)
        self.screen.remove_widget(self.CodItem)
        self.screen.remove_widget(self.NomeControle)
        self.screen.remove_widget(self.Descricao)
        self.screen.remove_widget(self.CodControle)
        self.screen.remove_widget(self.b)
        self.screen.remove_widget(self.label_conectado)
        self.screen.remove_widget(self.settings)
        self.screen.remove_widget(self.label_falha)

    def remove_cad(self):
        print('remove_cad')
        self.screen.remove_widget(self.broker)
        self.screen.remove_widget(self.send)
        self.screen.remove_widget(self.cancel)
        self.screen.add_widget(self.settings)
        #self.screen.add_widget(self.label_falha)

    def btn_send(self,b):
        if(self.broker.text == ""):
            popupWindow = Popup(title="erro",content = Label(text ="Preencha todos os campos"),size_hint=(None,None),size = (400,400))
            popupWindow.open()
            return

        servidor = (self.broker.text)
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
        
    def parse_sub_client_response(self,resp):
        return resp.split(',')[0:-1]

    def update_text_fields(self,texts):
        self.IdentfControle.text = texts[0]
        self.CodItem.text = texts[1]
        self.NomeControle.text = texts[2]
        self.Descricao.text = texts[3]
        self.CodControle.text = texts[4]

    def t(self):
        print('1')
        sub_client.run('client')
        print('2')
        self.comando = self.parse_sub_client_response(sub_client.response.pop(0))
        print("comando: ",self.comando)
        print(self.comando,' 3')
        self.is_calling = True

        sub_ackn.run('ackn')

        print('4 btn',sub_ackn.response)
        sub_ackn.response.pop(0)
        print('5')
        self.is_calling = False
        
        threading.Thread(target = self.t).start()


    def isThreadAlive(self,*a):
        if(self.is_calling):
            try:
                self.update_text_fields(self.comando)
                self.screen.add_widget(self.b)
                self.screen.add_widget(self.IdentfControle)
                self.screen.add_widget(self.CodItem)
                self.screen.add_widget(self.NomeControle)
                self.screen.add_widget(self.Descricao)
                self.screen.add_widget(self.CodControle)
                self.screen.remove_widget(self.label_conectado)
            except:
                pass
        else:
            try:
                self.screen.add_widget(self.label_conectado)
            except:
                pass
            self.screen.remove_widget(self.b)
            self.screen.remove_widget(self.IdentfControle)
            self.screen.remove_widget(self.CodItem)
            self.screen.remove_widget(self.NomeControle)
            self.screen.remove_widget(self.Descricao)
            self.screen.remove_widget(self.CodControle)
            
    def on_start(self):
        self.is_calling = False
        self.root.bind(on_press = self.btn_click)
        print('iniciando thread cliente')

        th = threading.Thread(target = self.t)

        th.start()
        Clock.schedule_interval(self.isThreadAlive,0.2)
        
mainApp().run()