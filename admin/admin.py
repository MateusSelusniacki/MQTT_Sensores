import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.button import MDRectangleFlatButton,MDRectangleFlatIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.icon_definitions import md_icons
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFloatingActionButton
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
import subscriber_db as sub_db
import subscriber_cont_press as sub_press

import threading
import re
import time

codigo = []
options_btn = [0,0,0]
enviar_pressed = [0]
cmd = ['']
inserting_db = []

class Options(Screen):
    def __init__(self,**kwargs):
        super(Options,self).__init__(**kwargs)
        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = "Green"
        self.Cad = MDRectangleFlatButton(text = 'Novo',size_hint = (.35,.05),pos_hint={'center_x':0.5, 'center_y':0.6}, on_release = self.btn_Cad)
        self.ignore = MDRectangleFlatIconButton(text = " ignorar",size_hint = (.05,.05),pos_hint={'center_x':0.75, 'center_y':0.6},icon = 'trash-can', on_release = self.btn_ignore)
        self.List = MDRectangleFlatButton(text = 'Listar',size_hint = (.35,.05),pos_hint={'center_x':0.5, 'center_y':0.5}, on_release = self.btn_List)
        self.Del = MDRectangleFlatButton(text = 'Excluir',size_hint = (.35,.05),pos_hint={'center_x':0.5, 'center_y':0.4}, on_release = self.btn_Del)
        self.settings_btn = Button(background_normal = 'settings.png',background_down ='settings.png',size_hint = (0.1,0.05),pos_hint={'center_x':0.9, 'center_y':0.9}, on_release = self.btn_settings)
        self.label_conectado = MDLabel(text = "Conectado",pos_hint={'center_x':0.8,'center_y':0.02})

        self.add_widget(self.Cad)
        #self.add_widget(self.ignore)
        #self.add_widget(self.label_conectado)
        self.add_widget(self.List)
        self.add_widget(self.Del)
        self.add_widget(self.settings_btn)
        self.add_widget(self.label_conectado)


    def btn_settings(self,b):
        self.manager.transition.direction = 'left'
        self.manager.current = 'servidor'        
    
    def btn_ignore(self,b):
        pub.run('send_data','ignored')

    def btn_Cad(self,b):
        self.manager.transition.direction = 'left'
        self.manager.current = 'novo' 

    def btn_List(self,b):
        self.manager.transition.direction = 'left'
        self.manager.current = 'listar'

    def btn_Del(self,b):
        self.manager.transition.direction = 'left'
        self.manager.current = 'excluir'

class Novo(Screen):
    def __init__(self,**kwargs):
        super(Novo,self).__init__(**kwargs)
        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = "Green"
        self.label_press3sec = MDLabel(text = "Pressione Continuamente o Botão",pos_hint={'center_x':0.75, 'center_y':0.5})
        self.cancel = MDRectangleFlatButton(text = 'Cancelar',size_hint = (.15,.05),pos_hint={'center_x':0.5, 'center_y':0.2}, on_release = self.btn_cancel)
    
        self.add_widget(self.label_press3sec)
        self.add_widget(self.cancel)

        self.e = Clock.schedule_interval(self.clock_verification,0.2)
        self.go2cad = False
    
    def clock_verification(self,*a):
        if(self.go2cad):
            self.go2cad = False
            self.manager.transition.direction = 'left'
            self.manager.current = 'cadastro'

    def thread_wait_button(self):
        sub_press.run('sub_press_btnsec')
        if(len(sub_press.response) != 0):
            cmd[0] = sub_press.response.pop(0)
        else:
            return
        self.go2cad = True
        print('fim thread_wait_button','go2cad',self.go2cad)

    def on_enter(self):
        threading.Thread(target = self.thread_wait_button).start()
    
    def on_leave(self):
        print('leaving')
        client = sub_press.global_client.pop(0)
        print('client',client)
        client.disconnect()
        print('client disconnected')

    def btn_cancel(self,b):
        self.manager.transition.direction = 'right'
        self.manager.current = 'options'

class Cadastro(Screen):
    def __init__(self,**kwargs):
        super(Cadastro,self).__init__(**kwargs)
        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = "Green"
        self.cancel = MDRectangleFlatButton(text = 'Cancelar',size_hint = (.15,.05),pos_hint={'center_x':0.5, 'center_y':0.2}, on_release = self.btn_cancel)
        self.send = MDRectangleFlatButton(
            text = 'Enviar',
            size_hint = (.15,.05),
            pos_hint={'center_x':0.5, 'center_y':0.3},
            on_release = self.btn_send
            )
        self.IdentfControle = MDTextField(
            hint_text =  "identificador do Controle",
            pos_hint = {'center_x':0.5, 'center_y':0.8},
            size_hint_x = None,
            width = 300
        )
        self.CodItem = MDTextField(
            hint_text =  "Codigo do Item",
            pos_hint = {'center_x':0.5, 'center_y':0.7},
            size_hint_x = None,
            width = 300
        )
        self.NomeControle = MDTextField(
            hint_text =  "Nome",
            pos_hint = {'center_x':0.5, 'center_y':0.6},
            size_hint_x = None,
            width = 300
        )
        self.Descricao = MDTextField(
            hint_text =  "Descrição",
            pos_hint = {'center_x':0.5, 'center_y':0.5},
            size_hint_x = None,
            width = 300
        )
        self.CodControle = MDTextField(
            hint_text =  "Codigo do Controle",
            pos_hint = {'center_x':0.5, 'center_y':0.4},
            size_hint_x = None,
            width = 300,
            disabled = True
        )

        #self.comando = Builder.load_string(text_field)
        self.add_widget(self.IdentfControle)
        self.add_widget(self.CodItem)
        self.add_widget(self.NomeControle)
        self.add_widget(self.Descricao)
        self.add_widget(self.CodControle)
        self.add_widget(self.send)
        self.add_widget(self.cancel)
    
        self.e = Clock.schedule_interval(self.clock_verification,0.2)
    
    def clock_verification(self,*a):
        if(cmd[0] != ''):
            self.CodControle.text = cmd[0]

    def clear_field(self):
        self.IdentfControle.text = ""
        self.CodItem.text = ""
        self.NomeControle.text = ""
        self.Descricao.text = ""
        self.CodControle.text = ""

    def btn_send(self,b):
        if(self.IdentfControle.text == ""):    
            popupWindow = Popup(title="erro",content = Label(text ="Código do Item Precisa ser preenchido"),size_hint=(None,None),size = (400,400))
            popupWindow.open()
            return

        if(self.CodItem.text == ""):    
            popupWindow = Popup(title="erro",content = Label(text ="Código do Item Precisa ser preenchido"),size_hint=(None,None),size = (400,400))
            popupWindow.open()
            return

        if(self.CodControle.text == ""):
            popupWindow = Popup(title="erro",content = Label(text ="Código de Controle Precisa ser preenchido"),size_hint=(None,None),size = (400,400))
            popupWindow.open()
            return

        enviar_pressed[0] = 1
        enviar_pressed.append(self.IdentfControle.text)
        enviar_pressed.append(self.CodItem.text)
        enviar_pressed.append(self.NomeControle.text)
        enviar_pressed.append(self.Descricao.text)
        enviar_pressed.append(self.CodControle.text)

        self.clear_field()

        self.manager.transition.direction = 'right'
        self.manager.current = 'options'
        options_btn[2] = 1
        self.is_calling = 1

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

        self.Enviar = MDRectangleFlatButton(text = 'Enviar',size_hint = (.35,.05),pos_hint={'center_x':0.5, 'center_y':0.3}, on_release = self.btn_send)
        self.Cancelar = MDRectangleFlatButton(text = 'Cancelar',size_hint = (.35,.05),pos_hint={'center_x':0.5, 'center_y':0.2}, on_release = self.btn_cancel)

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
        self.label_carregando = MDLabel(text = "Carregando dados...",pos_hint={'center_x':0.8,'center_y':0.5})
        self.not_server = MDLabel(text = "Servidor não localizado",pos_hint={'center_x':0.8,'center_y':0.5})

        self.boxlayout.add_widget(self.cancel)
        self.scroll.add_widget(self.boxlayout)
        self.add_widget(self.scroll)
        self.add_widget(self.label_carregando)

    def list_all(self):
        print('dentro da thread')
        pub.run('send_db','trash')
        
        sub_db.run('server_send_db')
        
        if(sub_db.response == []):
            self.add_widget(self.not_server)
            return
        
        content_raw = sub_db.response.pop(0)

        parsed = re.split('[|(|,|)|]',content_raw.replace(' ','').replace('\'',''))[1:-1]

        content = []
        i = 0
        while i < len(parsed):
            parsed[i] = int(parsed[i])
            parsed[i+1] = parsed[i+1]
            content.append(tuple(parsed[i:i+6]))
            i += 8

        for i in content:
            self.boxlayout.add_widget(MDRectangleFlatButton(
                text = i[3],
                size_hint = (.2,.05),
                pos_hint = {'center_x':0.5},
                on_release = self.btn_click
            ))
        
    def on_enter(self):
        self.remove_widget(self.not_server)
        self.remove_widget(self.label_carregando)
        self.list_all()

    def on_leave(self):
        self.boxlayout.clear_widgets()
        self.boxlayout.add_widget(self.cancel)
        self.add_widget(self.label_carregando)
        self.remove_widget(self.not_server)
    
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
        self.label_carregando = MDLabel(text = "Carregando dados...",pos_hint={'center_x':0.8,'center_y':0.5})
        self.not_server = MDLabel(text = "Servidor não localizado",pos_hint={'center_x':0.8,'center_y':0.5})

        self.boxlayout.add_widget(self.cancel)
        self.scroll.add_widget(self.boxlayout)
        self.add_widget(self.scroll)
        self.add_widget(self.label_carregando)

    def list_all(self):
        print('dentro da thread')
        pub.run('send_db','trash')
        
        sub_db.run('server_send_db')
        
        if(sub_db.response == []):
            self.add_widget(self.not_server)
            return
        
        content_raw = sub_db.response.pop(0)

        parsed = re.split('[|(|,|)|]',content_raw.replace(' ','').replace('\'',''))[1:-1]

        content = []
        i = 0
        print("parsed",parsed)
        while i < len(parsed):
            parsed[i] = int(parsed[i])
            parsed[i+1] = parsed[i+1]
            content.append(tuple(parsed[i:i+6]))
            i += 8

        for i in content:
            self.boxlayout.add_widget(MDRectangleFlatButton(
                text = i[3],
                size_hint = (.2,.05),
                pos_hint = {'center_x':0.5},
                on_release = self.btn_click
            ))
        
    def on_enter(self):
        self.remove_widget(self.label_carregando)
        self.list_all()

    def on_leave(self):
        self.boxlayout.clear_widgets()
        self.boxlayout.add_widget(self.cancel)
        self.add_widget(self.label_carregando)
        self.remove_widget(self.not_server)
    
    def server_toString(self):
        server = getServerAdmin()
        server_string = str(server[0]) + "," + server[1] + "," + server[2] + "," + server[3] + "," 
        return server_string

    def btn_click(self,b):
        pub.run('delete',server_toString() + b.text)

        self.boxlayout.remove_widget(b)

    def btn_cancel(self,b):
        self.manager.transition.direction = 'right'
        self.manager.current = 'options'

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class DemoApp(MDApp):   
    def build(self):
        self.o = Options(name = "options")
        self.c = Cadastro(name = "cadastro")
        self.n = Novo(name = "novo")
        self.s = Servidor(name = "servidor")
        self.l = Listar(name = "listar")
        self.e = Excluir(name = "excluir")
        
        self.screen_manager = ScreenManagement(transition=SlideTransition())
        self.screen_manager.add_widget(self.o)
        self.screen_manager.add_widget(self.n)
        self.screen_manager.add_widget(self.c)
        self.screen_manager.add_widget(self.s)
        self.screen_manager.add_widget(self.l)
        self.screen_manager.add_widget(self.e)

        Window.bind(on_request_close=self.on_request_close)

        return self.screen_manager
    
    def isThreadAlive(self,*a):        
        if(enviar_pressed[0]):
            enviar_pressed[0] = 0
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
            
    def t(self):
        print('aguardando topico admin')
        sub_admin.run('admin')
        c = sub_admin.response.pop(0)
        options_btn[0] = 1
        print(f'appending cmd {c}')
        cmd[0] = c
        if(len(codigo) == 0):
            codigo.append(c)

        print('aguardando ack')
        self.is_calling = True
        sub_ack.run('admin_ack')

        if(len(sub_ack.response) == 0):
            print('falha ao cadastrar')
            threading.Thread(target = self.t).start()
            self.is_calling = False
            options_btn[0] = 0
            options_btn[2] = 1
            return
        else:
            print('cadastrado')
        inserted_data = sub_ack.response.pop(0)
        print(f'dados inseridos {inserted_data}')
        self.is_calling = False
        print('ack recebido')
        options_btn[0] = 0
        options_btn[1] = 0
        options_btn[2] = 1
        
        threading.Thread(target = self.t).start()
        print('fim thread')

    def on_start(self):
        self.is_calling = False
        print('iniciando thread admin')

        th = threading.Thread(target = self.t)

        th.start()

        Clock.schedule_interval(self.isThreadAlive,0.2)

    def on_request_close(self, *args):
        self.o.e.cancel()
        self.c.e.cancel()

        if(len(sub_admin.global_client) != 0):
            sub_admin.response.append('pitanganamadrugadaerrada')
            sub_admin.global_client[0].disconnect()
        time.sleep(0.5)
        if(len(sub_ack.global_client) != 0):
            sub_ack.response.append('pitanganamadrugadaerrada')
            sub_ack.global_client[0].disconnect()
        time.sleep(0.5)
        return True

DemoApp().run()