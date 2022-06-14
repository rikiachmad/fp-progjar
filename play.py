from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.graphics import Color, Rectangle, Line, Ellipse
from functools import partial
from kivy.clock import  Clock

import socket
import logging
import json
import math
import pyautogui
import random

class ClientInterface:
    def __init__(self):
        self.server_address=('127.0.0.1',6666)

    def send_command(self,command_str=""):
        global server_address
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.server_address)
        logging.warning(f"connecting to {self.server_address}")
        try:
            logging.warning(f"sending message ")
            sock.sendall(command_str.encode())
            # Look for the response, waiting until socket is done (no more data)
            data_received="" #empty string
            while True:
                #socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
                data = sock.recv(16)
                if data:
                    #data is not empty, concat with previous content
                    data_received += data.decode()
                    if "\r\n\r\n" in data_received:
                        break
                else:
                    # no more data, stop the process by break
                    break
            # at this point, data_received (string) will contain all data coming from the socket
            # to be able to use the data_received as a dict, need to load it using json.loads()
            hasil = json.loads(data_received)
            logging.warning("data received from server:")
            return hasil
        except:
            logging.warning("error during data receiving")
            return False

class PlayerClientInterface(ClientInterface):
    def __init__(self, idplayer):
        super().__init__()
        self.idplayer = idplayer

    def set_location(self,x=100,y=100):
        player = self.idplayer
        command_str=f"set_location player {player} {x} {y}"
        hasil = self.send_command(command_str)
        if (hasil['status']=='OK'):
            return True
        else:
            return False

    def get_location(self):
        player = self.idplayer
        command_str=f"get_location player {player}"
        hasil = self.send_command(command_str)
        if (hasil['status']=='OK'):
            lokasi = hasil['location'].split(',')
            return (int(lokasi[0]),int(lokasi[1]))
        else:
            return False

    def set_size(self, size):
        player = self.idplayer
        command_str=f"set_size player {player} {size}"
        hasil = self.send_command(command_str)
        if (hasil['status']=='OK'):
            return True
        else:
            return False

    def get_size(self):
        player = self.idplayer
        command_str = f"get_size player {player}"
        hasil = self.send_command(command_str)
        if (hasil['status']=='OK'):
            size = hasil['size']
            return int(size)

class FoodClientInterface(ClientInterface):
    def __init__(self, idfood):
        super().__init__()
        self.idfood = idfood

    def set_location(self,x=100,y=100):
        food = self.idfood
        command_str=f"set_location food {food} {x} {y}"
        hasil = self.send_command(command_str)
        if (hasil['status']=='OK'):
            return True
        else:
            return False

    def get_location(self):
        food = self.idfood
        command_str=f"get_location food {food}"
        hasil = self.send_command(command_str)
        if (hasil['status']=='OK'):
            lokasi = hasil['location'].split(',')
            return (int(lokasi[0]),int(lokasi[1]))
        else:
            return False

    def set_size(self, size):
        food = self.idfood
        command_str=f"set_size food {food} {size}"
        hasil = self.send_command(command_str)
        if (hasil['status']=='OK'):
            return True
        else:
            return False

    def get_size(self):
        food = self.idfood
        command_str = f"get_size player {food}"
        hasil = self.send_command(command_str)
        if (hasil['status']=='OK'):
            size = hasil['size']
            return int(size)

class Food:
    def __init__(self,idfood='1', r=0, g=0, b=1):
        self.warna_r = r
        self.warna_g = g
        self.warna_b = b
        self.current_x, self.current_y = self.get_rand_pos()
        self.size = 25
        self.idfood = idfood
        self.widget = Widget()
        self.client_interface = FoodClientInterface(self.idfood)

    def get_client_interface(self):
        return self.client_interface

    def get_idplayer(self):
        return self.idplayer

    def draw(self):
        self.current_x, self.current_y = self.client_interface.get_location()
        wid = self.widget
        r = self.warna_r
        g = self.warna_g
        b = self.warna_b
        size = self.size

        with wid.canvas:
            Color(r, g, b)
            # Ellipse(pos=(self.current_x, self.current_y), size=(size, size))
            Line(circle=(self.current_x, self.current_y, size))

    def eaten(self):
        self.current_x, self.current_y = self.get_rand_pos()
        self.client_interface.set_location(self.current_x, self.current_y)
        self.draw()

    def set_xy(self,x=100,y=100):
        self.current_x = x
        self.current_y = y
        self.draw()
        #self.draw(self.widget, self.warna_r, self.warna_g, self.warna_b)

    def get_rand_pos(self):
        width, height = pyautogui.size()
        print(width, height)
        return random.randint(0, width-200), random.randint(0, height-200)
    def get_size(self):
        return self.size

    def get_widget(self):
        return self.widget

    def get_xy(self):
        return self.current_x, self.current_y

class Player:
    def __init__(self,idplayer='1',r=1,g=0,b=0):
        self.current_x = 100
        self.current_y = 100
        self.size = 100
        self.warna_r = r
        self.warna_g = g
        self.warna_b = b
        self.idplayer = idplayer
        self.widget = Widget()
        self.buttons = None
        self.client_interface = PlayerClientInterface(self.idplayer)
        self.inisialiasi()
        #self.draw(self.widget,self.warna_r,self.warna_g,self.warna_b)
    def get_client_interface(self):
        return self.client_interface
    def get_idplayer(self):
        return self.idplayer
    def set_xy(self,x=100,y=100):
        self.current_x = x
        self.current_y = y
        #self.draw(self.widget, self.warna_r, self.warna_g, self.warna_b)

    def set_size(self, size):
        self.size = size
        self.draw()

    def get_size(self):
        return self.size

    def get_widget(self):
        return self.widget
    def get_buttons(self):
        return self.buttons

    def get_xy(self):
        return self.current_x, self.current_y

    def draw(self):
        self.current_x, self.current_y = self.client_interface.get_location()
        self.size = self.client_interface.get_size()
        wid = self.widget
        r = self.warna_r
        g = self.warna_g
        b = self.warna_b

        with wid.canvas:
            Color(r, g, b)
            # Ellipse(pos=(self.current_x, self.current_y), size=(self.size_x, self.size_y))
            Line(circle=(self.current_x, self.current_y, self.size))

    def eat(self):
        self.size = self.size + 20
        self.client_interface.set_size(self.size)
        self.draw()

    def move(self,wid, arah,*kwargs):
        #self.draw(wid,0,0,0)
        if (arah=='right'):
            self.current_x = self.current_x + 20
        if (arah=='left'):
            self.current_x = self.current_x - 20
        if (arah=='up'):
            self.current_y = self.current_y + 20
        if (arah=='down'):
            self.current_y = self.current_y - 20
        self.client_interface.set_location(self.current_x,self.current_y)
        #self.draw(wid,self.warna_r,self.warna_g,self.warna_b)

    def reset(self):
        self.current_x = 100
        self.current_y = 100
        self.size = 100
        self.client_interface.set_location(self.current_x, self.current_y)
        self.draw()

    def inisialiasi(self):
        wid = self.widget
        btn_left = Button(text='left',on_press=partial(self.move, wid, 'left'))
        btn_up = Button(text='up',on_press=partial(self.move, wid, 'up'))
        btn_down = Button(text='down',on_press=partial(self.move, wid, 'down'))
        btn_right = Button(text='right',on_press=partial(self.move, wid, 'right'))

        self.buttons = BoxLayout(size_hint=(2, None), height=50)
        self.buttons.add_widget(btn_left)
        self.buttons.add_widget(btn_up)
        self.buttons.add_widget(btn_down)
        self.buttons.add_widget(btn_right)



class MyApp(App):
    players = []
    foods = []

    def refresh(self, callback):
        for i in self.players:
            i.get_widget().canvas.clear()
            player_x, player_y = i.get_xy()
            player_size = i.get_size()
            for j in self.foods:
                food_x, food_y = j.get_xy()
                food_size = j.get_size()
                # print(f'px: {player_x}, py: {player_y}, fx: {food_x}, fy: {food_y}, ps: {player_size}, fs: {food_size}')
                if self.player_eat_food(player_x, player_y, food_x, food_y, food_size, player_size):
                    i.eat()
                    j.eaten()

            i.draw()

        for i in self.foods:
            i.get_widget().canvas.clear()
            i.draw()

    def player_eat_food(self, player_x, player_y, food_x, food_y, food_size, player_size):
        dist_sq = math.sqrt(((player_x - food_x) * (player_x - food_x)) + ((player_y - food_y) * (player_y - food_y)));
        if dist_sq + food_size <= player_size:
            return True
        return False

    def build(self):

        p1 = Player('1', 1, 0, 0)
        p1.set_xy(100, 100)
        widget1 = p1.get_widget()
        buttons1 = p1.get_buttons()
        self.players.append(p1)

        p2 = Player('2', 0, 1, 0)
        p2.set_xy(100, 200)
        widget2 = p2.get_widget()
        buttons2 = p2.get_buttons()
        self.players.append(p2)

        food1 = Food('1',1, 1, 1)
        fwidget1 = food1.get_widget()
        self.foods.append(food1)

        food2 = Food('2', 1, 1, 1)
        fwidget2 = food2.get_widget()
        self.foods.append(food2)

        food3 = Food('3', 1, 1, 1)
        fwidget3 = food3.get_widget()
        self.foods.append(food3)

        root = BoxLayout(orientation='horizontal')
        root.add_widget(widget1)
        root.add_widget(buttons1)
        root.add_widget(widget2)
        root.add_widget(buttons2)
        root.add_widget(fwidget1)
        root.add_widget(fwidget2)
        root.add_widget(fwidget3)

        Clock.schedule_interval(self.refresh,1/60)

        return root

if __name__ == '__main__':
    MyApp().run()