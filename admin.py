import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

from kivy.uix.button import Button

from kivy.uix.boxlayout import BoxLayout

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

import db

import plyer
import publisher as pub
import subscriber_admin as sub_admin
import subscriber_ack as sub_ack
import threading
import time

codigo = []
com = []
options_btn = [0,0,0]
enviar_pressed = [0]
cmd = []
inserting_db = []

class Options(Screen):
    def __init__(self,**kwargs):
        super(Options,self).__init__(**kwargs)
        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = "Green"
        self.Cad = MDRectangleFlatButton(text = 'Cadastrar',size_hint = (.15,.05),pos_hint={'center_x':0.5, 'center_y':0.6}, on_release = self.btn_Cad)
        self.List = MDRectangleFlatButton(text = 'Listar',size_hint = (.15,.05),pos_hint={'center_x':0.5, 'center_y':0.5}, on_release = self.btn_List)
        self.Del = MDRectangleFlatButton(text = 'Excluir',size_hint = (.15,.05),pos_hint={'center_x':0.5, 'center_y':0.4}, on_release = self.btn_Del)
        self.settings_btn = Button(background_normal = 'settings.png',background_down ='settings.png',size_hint = (0.09,0.1),pos_hint={'center_x':0.9, 'center_y':0.9}, on_release = self.btn_settings)

        #self.add_widget(self.Cad)
        self.add_widget(self.List)
        self.add_widget(self.Del)
        self.add_widget(self.settings_btn)

        Clock.schedule_interval(self.clock_verification,0.2)

    def btn_settings(self,b):
        self.manager.transition.direction = 'left'
        self.manager.current = 'servidor'

    def on_enter(self):
        if(len(inserting_db) != 0):
            db.insertCodeAdmin(inserting_db[0])
            inserting_db.pop(0)

    def btn_Cad(self,b):
        self.manager.transition.direction = 'left'
        self.manager.current = 'cadastro'

    def btn_List(self,b):
        self.manager.transition.direction = 'left'
        self.manager.current = 'listar'

    def btn_Del(self,b):
        self.manager.transition.direction = 'left'
        self.manager.current = 'excluir'

    def clock_verification(self,*a):
        if(options_btn[0] and not options_btn[1]):
            options_btn[1] = 1
            self.add_widget(self.Cad)
        if(not options_btn[0] and options_btn[2]):
            options_btn[2] = 0
            self.remove_widget(self.Cad)

class Cadastro(Screen):
    def __init__(self,**kwargs):
        super(Cadastro,self).__init__(**kwargs)
        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = "Green"
        self.send = MDRectangleFlatButton(text = 'Enviar',size_hint = (.15,.05),pos_hint={'center_x':0.5, 'center_y':0.3}, on_release = self.btn_send)
        self.cancel = MDRectangleFlatButton(text = 'Cancelar',size_hint = (.15,.05),pos_hint={'center_x':0.5, 'center_y':0.2}, on_release = self.btn_cancel)
        self.IdentfControle = MDTextField(
            hint_text =  "identificador do Controle",
            pos_hint = {'center_x':0.5, 'center_y':0.8},
            size_hint_x = None,
            width = 300,
        )
        self.CodItem = MDTextField(
            hint_text =  "Codigo do Item",
            pos_hint = {'center_x':0.5, 'center_y':0.7},
            size_hint_x = None,
            width = 300,
        )
        self.NomeControle = MDTextField(
            hint_text =  "Nome",
            pos_hint = {'center_x':0.5, 'center_y':0.6},
            size_hint_x = None,
            width = 300,
        )
        self.Descricao = MDTextField(
            hint_text =  "Descrição",
            pos_hint = {'center_x':0.5, 'center_y':0.5},
            size_hint_x = None,
            width = 300,
        )
        self.CodControle = MDTextField(
            hint_text =  "Codigo do Controle",
            pos_hint = {'center_x':0.5, 'center_y':0.4},
            size_hint_x = None,
            width = 300,
        )
        #self.comando = Builder.load_string(text_field)
        self.add_widget(self.IdentfControle)
        self.add_widget(self.CodItem)
        self.add_widget(self.NomeControle)
        self.add_widget(self.Descricao)
        self.add_widget(self.CodControle)
        self.add_widget(self.send)
        self.add_widget(self.cancel)
    
        Clock.schedule_interval(self.clock_verification,0.2)
    
    def clock_verification(self,*a):
        if(len(cmd) != 0):
            print(type(cmd[0]),cmd[0])
            self.CodControle.text = cmd[0]
            cmd.pop(0)
    
    def clear_field(self):
        self.IdentfControle.text = ""
        self.CodItem.text = ""
        self.NomeControle.text = ""
        self.Descricao.text = ""
        self.CodControle.text = ""

    def btn_send(self,b):
        try:
            int(self.IdentfControle.text)
        except:
            popupWindow = Popup(title="erro",content = Label(text ="Identificador de Controle Inválido"),size_hint=(None,None),size = (400,400))
            popupWindow.open()
            return

        try:
            int(self.CodItem.text)
        except:
            popupWindow = Popup(title="erro",content = Label(text ="Código do Item Inválido"),size_hint=(None,None),size = (400,400))
            popupWindow.open()
            return

        if(self.CodControle.text == ""):
            popupWindow = Popup(title="erro",content = Label(text ="Código de Controle Precisa ser preenchido"),size_hint=(None,None),size = (400,400))
            popupWindow.open()
            return

        enviar_pressed[0] = 1
        enviar_pressed.append(int(self.IdentfControle.text))
        enviar_pressed.append(int(self.CodItem.text))
        enviar_pressed.append(self.NomeControle.text)
        enviar_pressed.append(self.Descricao.text)
        enviar_pressed.append(self.CodControle.text)

        self.clear_field()

        self.manager.transition.direction = 'right'
        self.manager.current = 'options'
        options_btn[2] = 1

    def btn_cancel(self,b):
        self.manager.transition.direction = 'right'
        self.manager.current = 'options'

class Servidor(Screen):
    def __init__(self,**kwargs):
        super(Servidor,self).__init__(**kwargs)
        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = "Green"

        server = db.getServerAdmin()

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

        self.Enviar = MDRectangleFlatButton(text = 'Enviar',size_hint = (.15,.05),pos_hint={'center_x':0.5, 'center_y':0.3}, on_release = self.btn_send)
        self.Cancelar = MDRectangleFlatButton(text = 'Cancelar',size_hint = (.15,.05),pos_hint={'center_x':0.5, 'center_y':0.2}, on_release = self.btn_cancel)

        self.add_widget(self.servidor)
        self.add_widget(self.porta)
        self.add_widget(self.usuario)
        self.add_widget(self.senha)
        self.add_widget(self.Enviar)
        self.add_widget(self.Cancelar)

    def btn_cancel(self,b):
        self.manager.transition.direction = 'right'
        self.manager.current = 'options'

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
        
        print('setando server')
        servidor_tup = (int(self.porta.text),self.servidor.text,self.usuario.text,self.senha.text,int(self.porta.text))
        db.setServerAdmin(servidor_tup)

        self.manager.transition.direction = 'right'
        self.manager.current = 'options' 

class Listar(Screen):
    def __init__(self,**kwargs):
        super(Listar,self).__init__(**kwargs)
        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = "Green"
        self.create_list()
        
    def create_list(self):
        self.scroll = ScrollView(
            do_scroll_y = True,
            do_scroll_x = False,
            size=(Window.width, Window.height),
            size_hint = (1,None)
        )
        
        self.boxlayout = BoxLayout(
            orientation = 'vertical',
            spacing = 10,
            size_hint_y = None,
            height = 1000
        )

        self.boxlayout.bind(minimum_height = self.boxlayout.setter('height'))
        
        self.cancel = MDRectangleFlatButton(text = '<',size_hint = (.1,.05),pos_hint={'center_x':0.1, 'center_y':0.8}, on_release = self.btn_cancel)
        
        self.boxlayout.add_widget(self.cancel)

        self.scroll.add_widget(self.boxlayout)
        self.add_widget(self.scroll)

    def on_enter(self):
        self.boxlayout.clear_widgets()
        self.create_list()
        self.list_all()

    def list_all(self):
        content = db.getAll()
        for i in content:   
            self.boxlayout.add_widget(MDRectangleFlatButton(
                text = i[3],
                size_hint = (.2,.05),
                pos_hint = {'center_x':0.5},
                on_release = self.btn_click
            ))
        
    def btn_click(self,b):
        print(Window.width,Window.height)
        print(self.boxlayout.size)

    def btn_cancel(self,b):
        self.manager.transition.direction = 'right'
        self.manager.current = 'options'

class Excluir(Screen):
    def __init__(self,**kwargs):
        super(Excluir,self).__init__(**kwargs)
        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = "Green"
        self.create_list()
        
    def create_list(self):
        self.scroll = ScrollView(
            do_scroll_y = True,
            do_scroll_x = False,
            size=(Window.width, Window.height),
            size_hint = (1,None)
        )
        
        self.boxlayout = BoxLayout(
            orientation = 'vertical',
            spacing = 10,
            size_hint_y = None,
            height = 1000
        )

        self.boxlayout.bind(minimum_height = self.boxlayout.setter('height'))
        
        self.cancel = MDRectangleFlatButton(text = '<',size_hint = (.1,.05),pos_hint={'center_x':0.1, 'center_y':0.8}, on_release = self.btn_cancel)
        
        self.boxlayout.add_widget(self.cancel)

        self.scroll.add_widget(self.boxlayout)
        self.add_widget(self.scroll)

    def on_enter(self):
       self.list_all()

    def list_all(self):
        content = db.getAll()
        for i in content:   
            self.boxlayout.add_widget(MDRectangleFlatButton(
                text = i[3],
                size_hint = (.2,.05),
                pos_hint = {'center_x':0.5},
                on_release = self.btn_click
            ))
        
    def btn_click(self,b):
        pub.run('delete',b.text)
        print(f'deleting {b.text}')
        db.deleteCodeAdmin(b.text)

        self.remove_widget(self.scroll)

        self.create_list()

    def btn_cancel(self,b):
        self.manager.transition.direction = 'right'
        self.manager.current = 'options'

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class DemoApp(MDApp):
    def build(self):
        self.screen_manager = ScreenManagement(transition=SlideTransition())
        self.screen_manager.add_widget(Options(name = "options"))
        self.screen_manager.add_widget(Cadastro(name = "cadastro"))
        self.screen_manager.add_widget(Servidor(name = "servidor"))
        self.screen_manager.add_widget(Listar(name = "listar"))
        self.screen_manager.add_widget(Excluir(name = "excluir"))

        return self.screen_manager
    
    def isThreadAlive(self,*a):        
        if(enviar_pressed[0]):
            enviar_pressed[0] = 0
            if(self.is_calling):
                self.is_calling = False
                print('is alive is calling')
                comando = tuple(enviar_pressed[1:6])
                enviar_pressed.pop(5)
                enviar_pressed.pop(4)
                enviar_pressed.pop(3)
                enviar_pressed.pop(2)
                enviar_pressed.pop(1)
                enviar_pressed[0] = 0

                print('comando',comando)
                pub.run('send_data',comando)
                
                inserting_db.append(comando)
                time.sleep(2)
        
    def t(self):
        print('aguardando topico client')
        sub_admin.run('admin')
        c = sub_admin.response.pop(0)
        options_btn[0] = 1
        com.append(c)
        print(f'appending cmd {com}')
        cmd.append(c)
        if(len(codigo) == 0):
                codigo.append(c)

        print('aguardando ack')
        notification = plyer.notification.notify(title='Responder', message = c)
        self.is_calling = True
        sub_ack.run('admin_ack')
        sub_ack.response.pop(0)
        print('ack recebido')
        self.is_calling = False
        print('ack recebido')
        notification = plyer.notification.notify(title='Já foi respondido', message = c)
        options_btn[0] = 0
        options_btn[1] = 0
        options_btn[2] = 1
        print('fim thread')
        th = threading.Thread(target = self.t)

        th.start()

    def on_start(self):
        self.is_calling = False
        print('iniciando thread admin')

        th = threading.Thread(target = self.t)

        th.start()
        Clock.schedule_interval(self.isThreadAlive,0.2)

DemoApp().run()