# coding=utf-8
import pyautogui
import os
from os import system
import requests
from sys import platform
from pymongo import MongoClient
pyautogui.PAUSE=2
pyautogui.FAILSAFE=False
import time
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
        system('echo "DarkUser5" | sudo -S nohup mongod &> mongo.out')
        while not res:
            session = requests.session()
            session.proxies = {}
            session.proxies['http'] = 'socks5h://localhost:9050'
            session.proxies['https'] = 'socks5h://localhost:9050'
            try:
                system('nohup tor &')
                try:
                    respuesta = session.get('https://ipinfo.io/json')
                    ipactual=respuesta.json()
                except: 
                    try:
                        respuesta = session.get('https://ipapi.co/json')
                        ipactual=respuesta.json()
                    except:
                        try:
                            respuesta = session.get('http://ip-api.com/json')
                            ipactual=respuesta.json()
                            ipactual['ip'] = ipactual['query']
                        except:
                            try:
                                respuesta = session.get('https://api.myip.com/')
                                ipactual=respuesta.json()
                            except:
                                try:
                                    respuesta = session.get('https://api.myip.com/')
                                    ipactual=respuesta.json()
                                    ipactual = ipactual['ip']
                                except:
                                    try:
                                        respuesta = session.get('http://ipapi.xyz/json')
                                        ipactual=respuesta.json()
                                    except:
                                        try:
                                            respuesta = session.get('http://free.ipwhois.io/json/')
                                            ipactual=respuesta.json()
                                        except:
                                            try:
                                                respuesta = session.get('https://api.ip.sb/geoip/')
                                                ipactual=respuesta.json()
                                            except:
                                                try:
                                                    respuesta = session.get('https://ip-api.io/json/')
                                                    ipactual=respuesta.json()
                                                except:
                                                    respuesta = session.get('http://www.geoplugin.net/json.gp?ip')
                                                    ipactual=respuesta.json()
                                                    ipactual['ip'] = ipactual['geoplugin_request']
                db = cliente.ip
                ipguardadas = []
                algo = db.actual.find({})
                try:
                    for ip in algo:
                        ipguardadas.append(ip['ip'])
                    if ipactual['ip'] not in ipguardadas:
                        db.actual.insert_one(ipactual)
                    res = 1
                except:
                    pass
                cliente.close()
            except Exception as e:
                system('killall tor')
                time.sleep(2)
                system('echo "DarkUser5" | sudo -S rm -r nohup.out')
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
    
