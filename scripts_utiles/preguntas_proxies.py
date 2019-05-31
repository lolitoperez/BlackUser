from requests import get
from fake_useragent import UserAgent
from time import sleep, time
import json
from pymongo import MongoClient
from random import randint
from datetime import datetime
from multiprocessing import Process


def obtener_coleccion_status_proxies():
    MONGODB_HOST_GLOBAL = '54.183.65.225'
    MONGODB_PORT_GLOBAL = '27017'
    MONGODB_TIMEOUT_GLOBAL = 60000
    MONGODB_DATABASE_GLOBAL = 'global_scraper'
    MONGODB_USER_GLOBAL = 'GLoba15cRAperUsr'
    MONGODB_PASS_GLOBAL = 'ScR4p3r4txTst5%5Wtr'
    URI_CONNECTION_GLOBAL = "mongodb://" + MONGODB_USER_GLOBAL \
                                         + ":" + MONGODB_PASS_GLOBAL + "@" + MONGODB_HOST_GLOBAL \
                                         + ":" + MONGODB_PORT_GLOBAL + "/admin"
    nombre_coleccion_proxies = 'status_proxies'
    cliente = MongoClient(URI_CONNECTION_GLOBAL)
    base_datos = cliente[MONGODB_DATABASE_GLOBAL]
    coleccion_status_proxies = base_datos[nombre_coleccion_proxies]
    return coleccion_status_proxies


def obtener_puerto_aleatoreo():
    return str(randint(20001, 29999))


def obtener_nuevo_diccionario_proxies(puerto=None):
    if not puerto:
        puerto = obtener_puerto_aleatoreo()
    proxy_dict = {
        'http': 'http://sistemasProxies:Adrian2010%%@mx.smartproxy.com:' + puerto,
        'https': 'https://sistemasProxies:Adrian2010%%@mx.smartproxy.com:' + puerto

    }
    return proxy_dict


"""puerto = '20003'
proxy_dict = {
    'http': 'http://sistemasProxies:Adrian2010%%@mx.smartproxy.com:' + puerto,
    'https': 'https://sistemasProxies:Adrian2010%%@mx.smartproxy.com:' + puerto

}"""


def trabaja_hilo(num_hilo: int):
    coleccion_status_proxies = obtener_coleccion_status_proxies()
    ua = UserAgent()
    headers = {
        'user-agent': ua.random,
    }
    puerto = 20001 + num_hilo
    proxy_dict = obtener_nuevo_diccionario_proxies(puerto=str(puerto))
    #print(proxy_dict)
    for i in range(200):
        inicio = time()
        fecha_inicio = datetime.now()
        try:
            respuesta = get('https://ipinfo.io/json', headers=headers, proxies=proxy_dict)
            # respuesta2 = get('http://www.letshome.mx', headers=headers, proxies=proxy_dict)
        except Exception as e:
            print('exception ', e, puerto)
            continue
        fin = time()
        # print('tiempo request: ', fin-inicio)
        tiempo_total = fin - inicio
        contenido = respuesta.content
        contenido_json = json.loads(contenido)
        ip = contenido_json['ip']
        print(ip, ' ', tiempo_total)
        diccionario_insercion = {
            'tiempo': tiempo_total,
            'hora': fecha_inicio
        }
        coleccion_status_proxies.update_one({'ip': ip},
                                            {"$push":
                                                 {'mediciones': diccionario_insercion}
                                             },
                                            upsert=True)
        sleep(30)


num_hilos = 40
procesos = []
for num_hilo in range(num_hilos):
    proceso = Process(name=str(num_hilo), target=trabaja_hilo, args=(num_hilo,), daemon=False)
    procesos.append(proceso)

for proceso in procesos:
    proceso.start()

for proceso in procesos:
    proceso.join()