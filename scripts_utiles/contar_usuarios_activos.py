from pymongo import MongoClient
from datetime import datetime
from dateparser import parse


MONGODB_HOST = '13.52.11.40'
MONGODB_PORT = '27017'
MONGODB_TIMEOUT = 60000
MONGODB_DATABASE = 'XLamudi'
MONGODB_USER = 'Scraper%2Fops'
MONGODB_PASS = 'R3vim3x5o5%2F%2F'
URI_CONNECTION = "mongodb://" + MONGODB_USER+":"+MONGODB_PASS+"@"+MONGODB_HOST + ":"+MONGODB_PORT+ "/admin"
MONGODB_COLLECTION = 'superuser_cloud_listas'

coneccion = MongoClient(URI_CONNECTION)
base = coneccion[MONGODB_DATABASE]
coleccion = base[MONGODB_COLLECTION]

cursor = coleccion.find({})
todos = [elemento for elemento in cursor]


conteos_exito = 0
conteos_totales = 0
for lista in todos:
    lista_historia = lista['history']
    for elemento in lista_historia:
        inicio = elemento['Inicio']


        if True:#inicio > datetime(2019, 4, 10, 23, 20, 0):
            print(elemento)
            conteos_totales += 1
            if elemento['status'] == 'exitosa':
                conteos_exito += 1
print('conteos con exito: ', conteos_exito)
print('conteos totales: ', conteos_totales)
