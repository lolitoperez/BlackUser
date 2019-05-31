from os import system
from sys import platform
from time import sleep
from datetime import datetime
import random
import logging

from KeyBoard import KeyBoard

import numpy as np
from pytz import timezone

class SuperUser(object):
	"""docstring for SuperUser"""
	def __init__(self):
		super(SuperUser, self).__init__()
		self.OPERATING_SYSTEM = self.__getOperatingSystem()
		self.DICTIONARY_BROWSER = {'google':'https://www.google.com.mx', 'yahoo':'https://espanol.yahoo.com', 'bing':'https://www.bing.com'}
		self.keyBoardUser = KeyBoard()
		self.local_logger = logging.getLogger('super_logger')
		self.local_logger.setLevel(logging.DEBUG)
		# self.sesiones = [80442.0, 88700.3041825095, 93238.12949640288, 96079.81878088963, 98848.22033898305, 102406.40913081651, 107206.70955882354, 113133.75363724539, 120000.92592592593, 127337.2270742358, 134224.28078250863, 140193.38942307694, 144357.5495049505, 146349.9372647428, 145983.60450563204, 144001.11111111112, 140531.2048192771, 136262.7336448598, 131648.87133182844, 126921.54515778019, 122521.95378151261, 118417.1573604061, 114578.48722986247, 111086.57142857143, 107801.20147874307, 104798.65229110511, 102048.03149606299, 99353.40715502555, 96797.42738589211, 94446.07287449393, 92133.41232227489, 90070.19305019305, 88097.35649546827, 86400.66666666667, 84891.48471615721, 83673.52941176471, 82665.41459957477, 81910.74438202247, 81396.30146545709, 81113.28233657859, 81000.625, 81000.625, 81056.91452397499, 81169.72860125262, 81169.72860125262, 81056.91452397499, 80776.24653739612, 80275.91190640055, 79509.81595092025, 78546.06060606061, 77296.81908548708, 75938.0859375, 74435.80089342693, 72946.15384615384, 71558.83435582822, 70265.60240963855, 69223.08605341247, 68451.23239436619, 68012.18658892128, 67972.55244755244, 68370.98475967174, 69223.08605341247, 70563.15789473684, 72402.79329608938, 74769.80769230769, 77605.38922155688, 80832.22453222453, 84339.04555314533, 87964.47963800906, 91411.36363636363, 94369.66019417476, 96477.1712158809, 97363.02170283806, 97039.01830282861, 95372.7718724448, 92572.14285714286, 89106.8754774637, 85263.81578947368, 81339.53974895398, 77708.79413724184, 74578.58056265984, 71956.13818630474, 69970.54589082183, 68652.67804590936, 67932.96447291788, 67735.71428571429, 68051.86697782965, 68693.10954063604, 69594.80906921241, 70605.87167070218, 71690.78057775045, 72809.55056179776, 74057.71428571429, 75495.7281553398, 77092.46530072704, 78125.1841929002]
							
		# self.usuarios = 2000000
		# self.desviaciones = [10.0,10.0,3.0,4.0,4.0,5.0]

	def search(self, key_word, browser):
		self.local_logger.info('Abriendo navegador')
		self.__openBrowser(browser)
		self.local_logger.info('Abrí navegador')
		
		# if movile:
		# 	self.keyBoardUser.tab()
		self.local_logger.info('Buscando iniciar sesion')
		if self.keyBoardUser.searchKeyBoard(browser):
			self.local_logger.info('Pude iniciar sesión')
			self.local_logger.info('Foco en la barra de tareas')
			self.keyBoardUser.get_focus_on_search_bar()
			self.local_logger.info('Escribo las keywords: '+ key_word)
			self.keyBoardUser.writeAndEnter(key_word)

			return True
		else:
			self.local_logger.info('No pude iniciar sesión')
		self.keyBoardUser.closeTabs()
		self.keyBoardUser.closeTabs()
		return False

	def findSite(self, site,log_url):

		# Busca el sitio en la lista del buscador solicitado
		if self.keyBoardUser.findSiteKeyBoard(site):
			self.local_logger.info('Encontrado letshome')
			timeInit = datetime.now()
			timeStart = 0
			exito='exitosa'
			timeEnd = random.randrange(70,75) #self.tiempoRandomTiempoExtra() 
			Images = ['blog','buro',
					  'hipoteca','mapa', 'valua'] #sequito 'publica'
			imagen=Images[random.randrange(0,len(Images))]
			cambiarPagina=True
			self.local_logger.info('Iniciando navegación en la página')
			while timeStart < timeEnd:
				#print('[X] -- En sesión')

				if cambiarPagina and timeStart >= 60:#60
					self.local_logger.info('Cambiaré a la página: ' + imagen)
					exito=self.keyBoardUser.changePage(imagen,log_url)
					self.local_logger.info('Resultado: ' + exito)
					cambiarPagina=False
				
				sleep(1)
				timeStart = datetime.now() - timeInit
				timeStart = timeStart.seconds
			self.local_logger.info('Terminada navevación en la página')
			sleep(1)
			self.keyBoardUser.closeTabs()
			sleep(1)
			self.keyBoardUser.closeTabs()
			#return imagen

			return exito
		else:
			self.local_logger.info('No encontrado letshome')
			return 'no exitosa findSiteKeyBoard'

	def visitWebSite(self, url_site, browser):
		""" Ingresa directamente al sitio solicitado """

		self.__openBrowser(browser)

		if self.OPERATING_SYSTEM == "darwin":
			url_site = url_site.replace('/', '&').replace(':','>')

		if self.keyBoardUser.searchKeyBoard(browser):
			self.keyBoardUser.delAllCharacters()
			self.keyBoardUser.writeAndEnter(url_site)
			return True
		self.keyBoardUser.closeTabs()
		self.keyBoardUser.closeTabs()

		return False

	def findSiteDirect(self, site):
		sleep(60)
		if self.keyBoardUser.findYellow():
			sleep(140)
			self.keyBoardUser.closeTabs()
			self.keyBoardUser.closeTabs()
			return True
		sleep(30)
		self.keyBoardUser.closeTabs()
		self.keyBoardUser.closeTabs()
		return False

	def getPositionList(self):

		# Obtiene la lista de posiciones del buscador solicitado 

		pass

	def interactWebPage(self):
		pass

	def __openBrowser(self, browser):

		if self.OPERATING_SYSTEM == "linux":
			system("firefox -p default " +self.DICTIONARY_BROWSER[browser]+" --safe-mode &")
		elif self.OPERATING_SYSTEM == "darwin":
			system("open -a Firefox '"+self.DICTIONARY_BROWSER[browser]+"'")
		sleep(15)#20

		
	def __getOperatingSystem(self):

		# Regresa el sistema operativo en el que se está ejecutando
		if platform == "linux" or platform == "linux2":
		# linux
			return 'linux'
		elif platform == "darwin":
		# OS X
			return 'darwin'
		# elif platform == "win32":


	# def index(self):
	# 	hora = datetime.now(timezone('Mexico/General'))
	# 	return int(np.floor((hora.hour * 60.0 **2.0 + hora.minute * 60.0 + hora.second)/900.0))

	# def std(self):
	# 	return int(np.floor(self.index()/19))

	# def tiempoSesion(self):
	# 	return self.sesiones[self.index()] * 60.0 * 30.0/ self.usuarios

	# def tiempoSesionTiempoExtra(self):
	# 	return self.tiempoSesion()

	# def tiempoRandomTiempoExtra(self):
	# 	tiempo = np.random.normal(self.tiempoSesionTiempoExtra(), self.desviaciones[self.std()])
	# 	while True:
	# 		if tiempo <= 50:
	# 			if self.tiempoSesionTiempoExtra() <=50:
	# 				tiempo=51
	# 			elif self.tiempoSesionTiempoExtra()<=55:
	# 				tiempo=self.tiempoSesionTiempoExtra()
	# 			tiempo = np.random.normal(self.tiempoSesionTiempoExtra(), self.desviaciones[self.std()])
	# 		else: return tiempo
		


if __name__ == '__main__':
	su = SuperUser()
	# su.search('letshome', 'bing')
	# su.visitWebSite('http://ecleneue.com/TMj', 'google')
	su.search('departamentos en renta letshome','google')
