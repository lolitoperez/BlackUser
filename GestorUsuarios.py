from datetime import datetime
from UsuarioWeb import UsuarioWeb
from ValueProxies import ValueProxies
from random import randrange
from traceback import format_exc
from os import system
import pymongo
from copy import copy
from Log import Log
from pyautogui import PAUSE,FAILSAFE,hotkey
import sys
import logging
from logging import handlers
from getpass import getuser


class GestorUsuarios(object):
	"""docstring for GestorUsuarios"""
	def __init__(self,recurrents):
		super(GestorUsuarios, self).__init__()
		# self.userWeb = None
		PAUSE = 3
		FAILSAFE = False
		self.DICTIONARY_USERS = self.__setUsers(recurrents)

		self.MONGODB_HOST = '104.199.125.135'
		self.MONGODB_PORT = '27017'
		self.MONGODB_TIMEOUT = 60000
		self.MONGODB_DATABASE = 'XLamudi'
		self.MONGODB_USER = 'Scraper%2Fops'
		self.MONGODB_PASS = 'R3vim3x5o5%2F%2F'
		self.URI_CONNECTION = "mongodb://" + self.MONGODB_USER+":"+ self.MONGODB_PASS+"@"+ self.MONGODB_HOST + ":"+self.MONGODB_PORT+ "/admin"

		self.local_logger = logging.getLogger('super_logger')
		self.local_logger.setLevel(logging.DEBUG)
		self.local_logger.setLevel(logging.INFO)
		self.local_logger.setLevel(logging.WARNING)

		handler = handlers.TimedRotatingFileHandler('/home/'+getuser()+'/superusercloud/logs_superuser.txt', when='midnight')
		formater = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
		handler.setFormatter(formater)
		self.local_logger.addHandler(handler)
		self.MONGODB_COLLECTION = 'superuser_cloud_listas'
		self.proxy_manager = ValueProxies()
		self.listProxies = []
		self.users = {'padreSonador': {'rangeTime':range(0,24), 'typeUser':'padreSonador'}, 'solteraPlanificadora': {'rangeTime':range(0,24), 'typeUser':'solteraPlanificadora'},'mamaPrimeriza': {'rangeTime':range(0,24), 'typeUser':'mamaPrimeriza'},'inversionista2': {'rangeTime':range(0,24), 'typeUser':'inversionista2'},'solteroAfterOffice': {'rangeTime':range(0,24), 'typeUser':'solteroAfterOffice'},'padreAbuelo': {'rangeTime':range(0,24), 'typeUser':'padreAbuelo'}}

	def createUsers(self, timeMinutes):

		connection = self.__mongoconexion()
		ip = self.__get_ip()
		##ip = 'X_0'

		# Working 
		#self.__update_status('working', 'status22', connection, self.MONGODB_DATABASE, ip)
		#print('[X] -- Inicia gestor de usuarios')
		
		startTime = datetime.now()
		timeSeconds = timeMinutes*60
		timeRest = 0 
		timesExecute = 0
		userWebTmp = None

		try:
			while timeRest < timeSeconds:
				self.setProxies()

				#print('[X] -- Obtiene tipo de usuario')
				typeUser = self.getTypeUser()
				#proxy = self.listProxies[randrange(0, len(self.listProxies))]
				self.local_logger.info('Iniciamos obteniendo proxy buena')
				proxy,dictproxy = self.proxy_manager.obtener_proxy_buena()
				self.local_logger.info('Terminé obteniendo proxy buena')
				#print('[X] -- Obtiene usuario ', typeUser)

				if typeUser:
					logObject = Log(proxy,dictproxy,ip)
					#este usuario tiene la proxy cargada como campo, la cargará en firefox
					#
					self.local_logger.info('Instanciando usuario')
					userWeb = UsuarioWeb(typeUser, proxy, self.__getUsers(), logObject)
					self.local_logger.info('Fin instancia objeto')
					self.local_logger.info('Iniciando processUser')
					self.proccessUser(userWeb)
					self.local_logger.info('Iniciando usuario')
					hotkey('ctrl', 'w')
					hotkey('ctrl', 'w')
					system('pkill -9 firefox')
					# userWebTmp = copy(userWeb)
					# del userWeb
					
				else:
					timesExecute = timesExecute + 1

				if timesExecute == 4:
					break
				timeRest = datetime.now() - startTime
				timeRest = timeRest.seconds

			# self.finaliceSession(userWebTmp)
			#self.__update_status('finalizado', 'status22', connection, self.MONGODB_DATABASE, ip)
			#print(datetime.now()-startTime)

		except Exception as e:
			self.__set_error(format_exc(), 'E_superuser.txt')
			# self.finaliceSession(userWebTmp)
			#self.__update_status('error', 'status22', connection, self.MONGODB_DATABASE, ip)
			#print(e)
			hotkey('ctrl', 'w')
			hotkey('ctrl', 'w')
			system('pkill -9 firefox')


		

		# Finalizado
	def proccessUser(self, user):
		#print('[X] -- Inicia Usuario')
		# user.getUserParameters()
		#print('[X] -- Obtiene parametros de usuario')
		user.setParameters()
		#print('[X] -- Inicia parametros configuración')
		# print('[X] -- Inicia búsqueda')
		# user.search('letshome', 'google')
		# user.findSite('letshome')

	def finaliceSession(self, user):
		user.closeSession(user)

	def setProxies(self):
		self.listProxies = self.proxy_manager.getProxies()

	def getTypeUser(self):
		time = datetime.now()
		listUsers = [i for i in self.users if time.hour in self.users[i]['rangeTime']]
		#print('[X] -- Lista de usuarios ', listUsers)
		if listUsers:
			return listUsers[randrange(0, len(listUsers))]
		else:
			return None



	def __mongoconexion(self):
		
		try:
			client = pymongo.MongoClient(self.URI_CONNECTION, serverSelectionTimeoutMS=self.MONGODB_TIMEOUT)
			client.server_info()
			#print ('OK -- Connected to MongoDB at server %s' % (self.MONGODB_HOST))
			client.close()
		except pymongo.errors.ServerSelectionTimeoutError as error:
			pass
			#print ('Error with MongoDB connection: %s' % error)
		except pymongo.errors.ConnectionFailure as error:
			pass
			#print ('Could not connect to MongoDB: %s' % error)

		return client


	def __update_status(self, status, field, connection, database, ip):
		db_name = self.__set_database(database,connection)
		db_name[self.MONGODB_COLLECTION].update_one({'IP_server':ip},{'$set':{field:status}})

	def __set_database(self, name_database, connection):
		return connection[name_database]

	def __get_ip(self):
		with open('/home/'+getuser()+'/nombre/nombre.txt','r') as proxy:
			ip = (proxy.readline()).replace(' ','').replace('\n','')
			#ip = 'X_0'
			return ip

	def __set_error(self, text, name_file):
		file = open(name_file, 'a+')
		file.write(text)
		file.close()

	def __setUsers(self, n):
		dictTmp = {}
		for i in range(10):
			if i < n:
				dictTmp[str(i)] = 'Recurrente'
			else:
				dictTmp[str(i)] = 'Nuevo'

		return dictTmp

	def __getUsers(self):

		return self.DICTIONARY_USERS[str(randrange(0,10))]



if __name__ == '__main__':
	timeMinutes = sys.argv[1]
	recurrents = sys.argv[2]

	gu = GestorUsuarios(int(recurrents))
	# gu.setProxies()
	gu.createUsers(int(timeMinutes))




