from datetime import datetime
import pymongo
from getpass import getuser
class Log(object):
	"""Modulo de logs :)"""
	def __init__(self,proxy,dictproxy,nombre):
		super(Log, self).__init__()
		self.nombre = nombre
		self.conect =  pymongo.MongoClient('mongodb://Scraper%2Fops:R3vim3x5o5%2F%2F@104.199.125.135:27017/admin')
		self.db = self.conect.XLamudi
		self.collection = self.db['historial_superuser']
		self.cookie = {
						'IP_server':self.nombre,
						'proxy':proxy,
						'Informacion_proxy':dictproxy,
						'Usuario_instancia':getuser(),
						'Inicio':datetime.now(),
						'Camino':[]
					  }
					  
	def set_url_clickeado(self,url_clickeado):
		self.cookie['url_click']=url_clickeado
	def set_url_buscado(self,url_buscado):
		self.cookie['url_buscado']=url_buscado
	def setKeyword(self,keyword):
		self.cookie['Search'] = keyword
	def setUserAgent(self,user_agent):
		self.cookie['user_agen'] = user_agent

	def setStatus(self,status):
		self.cookie['status'] = status

	def camino(self,eleccion):
		self.cookie['Camino'] += [eleccion]

	def endCookie(self):
		self.cookie['ID'] = self.cookie['proxy']+'---'+self.cookie['user_agen']
		self.cookie['Fin'] = datetime.now()
		self.cookie['Duracion'] = str(self.cookie['Fin']-self.cookie['Inicio'])
		self.collection.insert_one(self.cookie)

