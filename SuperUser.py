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
                        

    def search(self, key_word, browser):
        self.local_logger.info('Abriendo navegador')
        self.__openBrowser(browser)
        self.local_logger.info('Abrí navegador')
        
        # if movile:
        #   self.keyBoardUser.tab()
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

                if cambiarPagina and timeStart >= 1:#60
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

