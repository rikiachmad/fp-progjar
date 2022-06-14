import os
import json
import base64
from glob import glob
import shelve
import random
import pyautogui
class ServerInterface:
    def __init__(self):
        self.object = shelve.open('g.db',writeback=True)
        self.object['location player 1']= "100,100"
        self.object['location player 2']= "100,100"
        x, y = self.get_rand()
        self.object['location food 1'] = f"{x},{y}"
        x, y = self.get_rand()
        self.object['location food 2'] = f"{x},{y}"
        x, y = self.get_rand()
        self.object['location food 3'] = f"{x},{y}"
        self.object['size player 1'] = "100"
        self.object['size player 2'] = "100"
        self.object['size food 1'] = "100"
        self.object['size food 2'] = "100"
        self.object['size food 3'] = "100"

    def set_location(self,params=[]):
        obj = params[0]
        oid = params[1]
        x = params[2]
        y = params[3]
        try:
            key = f"location {obj} {oid}"
            self.object[key]=f"{x},{y}"
            self.object.sync()
            return dict(status='OK', object=obj, oid=oid)
        except Exception as e:
            return dict(status='ERROR')

    def get_location(self,params=[]):
        obj = params[0]
        oid = params[1]
        try:
            key = f"location {obj} {oid}"
            return dict(status='OK',location=self.object[key])
        except Exception as ee:
            return dict(status='ERROR')

    def set_size(self, params=[]):
        obj = params[0]
        oid = params[1]
        size = params[2]
        try:
            key = f"size {obj} {oid}"
            self.object[key] = size
            self.object.sync()
            return dict(status='OK', object=obj, oid=oid)
        except Exception as ee:
            return dict(status="ERROR")

    def get_size(self, params=[]):
        obj = params[0]
        oid = params[1]
        try:
            key = f"size {obj} {oid}"
            return dict(status='OK', size=self.object[key])
        except Exception as ee:
            return dict(status='ERROR')

    def get_rand(self):
        width, height = pyautogui.size()
        print(width, height)
        return random.randint(0, width - 200), random.randint(0, height - 200)

if __name__=='__main__':
    p = ServerInterface()
    p.set_location(['player','1',100,100])
    print(p.get_location('player','1'))
    p.set_location(['food', '2',120,100])
    print(p.get_location('food','2'))
