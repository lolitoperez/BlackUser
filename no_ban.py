from pymongo import MongoClient
import time
import requests
from os import system

class Saca:

    def obtener_proxy_buena():
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
                #time.sleep(0.2)
                system('echo "DarkUser5" | sudo -S rm -r nohup.out')
                cliente.close()
                #print("Supero el timeout")
                intentos += 1
                #print("Intntos", intentos)
        return 'mx.smartproxy.com:'+puerto , ipactual


while 1:
    Saca.obtener_proxy_buena()