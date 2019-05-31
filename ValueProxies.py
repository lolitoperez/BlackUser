# coding=utf-8
import pyautogui
import os
from os import system
import requests
from sys import platform
from pymongo import MongoClient
pyautogui.PAUSE=2
pyautogui.FAILSAFE=False

from requests import get
from fake_useragent import UserAgent
from Log import Log
import numpy as np

cliente = MongoClient()

class ValueProxies():
    """docstring for ValueProxies"""
    def __init__(self):
        super(ValueProxies, self).__init__()
        self.OPERATING_SYSTEM = self.__getOperatingSystem()
        self.user_agent = UserAgent()
        self.Log=Log

    def getProxies(self):
        sopotamadre2 = '127.0.0.1:9050'
        #print('----------------',sopotamadre2)
        return sopotamadre2

    def evaluate_proxy(self):
        pass

    def __getOperatingSystem(self):

        # Regresa el sistema operativo en el que se está ejecutando
        if platform == "linux" or platform == "linux2":
        # linux
            return 'linux'
        elif platform == "darwin":
        # OS X
            return 'darwin'
        # elif platform == "win32":

    def obtener_proxy_buena(self, verbose=False):
        intentos = 0
        puerto = '9050'
        res  = None
        while not res:
            session = requests.session()
            session.proxies = {}
            session.proxies['http'] = 'socks5h://localhost:9050'
            session.proxies['https'] = 'socks5h://localhost:9050'
            try:
                system('echo "DarkUser5" | sudo -S nohup mongod &> mongo.out')
                respuesta = session.get('http://ipinfo.io/json')
                res = 1
                ipactual=respuesta.json()
                db = cliente.ip
                ipguardadas = []
                algo = db.actual.find({})
                try:
                    for ip in algo:
                        ipguardadas.append(ip['ip'])
                    if ipactual['ip'] not in ipguardadas:
                        db.actual.insert_one(ipactual)
                except:
                    pass
                cliente.close()
            except Exception as e:
                print(e)
                system('echo "DarkUser5" | sudo -S pkill mongod')
                system('rm -r mongo.out')
                cliente.close()
                #print("Supero el timeout")
                intentos += 1
                #print("Intntos", intentos)
        return 'mx.smartproxy.com:'+puerto , ipactual

    def obtener_puerto_aleatoreo(self):
        return str(str(np.random.randint(20001,29999)))

    def obtener_nuevo_diccionario_proxies(self, puerto=None):
        if not puerto:
            puerto = self.obtener_puerto_aleatoreo()
        proxy_dict = {
            'http': 'socks5h://localhost:9050',
            'https': 'socks5h://localhost:9050'
        }
        return proxy_dict
    
