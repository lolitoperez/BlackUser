from SuperUser import SuperUser
from Usuario import Usuario
from Profile import Profile
from ValueProxies import ValueProxies
from Log import Log
import logging
from getpass import getuser
from os import popen, system
from re import search

from random import randint, randrange

class UsuarioWeb(SuperUser):
    """docstring for UsuarioWeb"""
    def __init__(self, userType, proxie, newOrRecurrent,Log=None):
        super(UsuarioWeb, self).__init__()
        
        self.USER_TYPE = userType
        self.proxies = ValueProxies()
        self.profile = Profile(newOrRecurrent)
        self.proxie = proxie
        self.LogObject = Log
        self.userType = Usuario(userType,self.LogObject)
        self.newOrRecurrent = newOrRecurrent
        self.local_logger = logging.getLogger('super_logger')
        self.local_logger.setLevel(logging.DEBUG)

    def getUserParameters(self):
        a = self.userType.getUser()
        return a

    def getProxie(self):
        return self.proxies

    def setParameters(self, urlSite=None):
        self.local_logger.info('Colocando tipo de usuario')
        parameters = self.getUserParameters()
        if self.newOrRecurrent == 'Recurrente':
            useragent = self.profile.loadProfile(self.USER_TYPE)
        else:
            useragent = parameters['userAgent']
        self.local_logger.info('Fin colocando tipo de usuario')
        ip = self.proxie.split(':')[0]
        port = int(self.proxie.split(':')[1])
        #print('[X] -- Proxy',ip)
        ruta = ''
        self.local_logger.info('Inicia configuracion firefox con datos: '
                               + ip + ' '
                               + str(port) + ' '
                               + useragent)
        self.configProfile(ip, port, useragent)
        self.local_logger.info('Finaliza configuracion firefox con datos')
        if urlSite:
            # if self.LogObject:
            #   self.LogObject.setKeyword('urlSite')
            self.local_logger.info('Navegaremos al link: ', urlSite)
            self.navigateToLink(urlSite, 'adlfy','google')
            self.local_logger.info('Termina navegación al link', urlSite)
        else:
            # if self.LogObject:
            #   self.LogObject.setKeyword(parameters['palabrasClave'])
            self.local_logger.info('Navegaremos al sitio: letshome')
            statusS=self.navigateToPage(parameters['palabrasClave'], 'letshome', 'google')
            self.local_logger.info('Termina navegación al sitio: letshome')
            self.LogObject.setStatus(statusS)
        # if self.LogObject:
        #   self.LogObject.endCookie()

        self.__setLog(useragent, parameters['palabrasClave'] if not urlSite else urlSite, ruta)
        self.closeSession(useragent, self.USER_TYPE)


    def setProfile(self, key, value):
        self.profile.setParameters(key, value)


    def getProfile(self):
        self.profile.getProfile()


    def deleteProfile(self, key):
        self.profile.deleteParameter(key)


    def configProfile(self, ip, port, userAgent):
        self.getProfile()

        # self.deleteProfile('print.macosx.pagesetup-2')
        self.setProfile('network.proxy.ftp', '')
        self.setProfile('network.proxy.http', '')
        self.setProfile('network.proxy.socks', '127.0.0.1')
        self.setProfile('network.proxy.ssl', '')

        self.setProfile('network.proxy.ftp_port', None)
        self.setProfile('network.proxy.http_port', None)
        self.setProfile('network.proxy.socks_port', 9050)
        self.setProfile('network.proxy.ssl_port', None)

        self.setProfile('network.proxy.type', 1)
        self.setProfile("browser.sessionstore.resume_from_crash",False)
        #print('[X] -- Useragent ',userAgent)
        self.setProfile('general.useragent.override', userAgent)
        self.setProfile('intl.accept_languages', 'es-mx')

        self.profile.saveFile()

    def closeSession(self, userAgent, userType):

        system('pkill -9 firefox')
        self.getProfile()
        self.setProfile('network.proxy.type', 0)
        self.deleteProfile('general.useragent.override')
        self.profile.saveFile(close=True, userAgent=userAgent, userType=userType)

    #comenetario inutil
    def navigateToPage(self, keyword, site, browser):
        self.local_logger.info('Iniciando sesion en el proxy')
        if self.search(keyword, browser):#if self.search(keyword+ ' '+ site, browser):
            self.local_logger.info('Pude iniciar sesión en el proxy y realizé la búsqueda: ' + keyword)
            self.local_logger.info('Inicio busqueda de letshome en los resultados de google')
            return self.findSite(site,self.LogObject)
            
            

        else:
            self.local_logger.info('No pude iniciar sesion en el proxy o no pude realizar la búsqueda de google')
            return 'no exitosa search Key Board'

    def navigateToLink(self, link, site, browser):
        if self.visitWebSite(link, browser):
            self.findSiteDirect(site)

    def __setLog(self, userAgent, keyWord, ruta):

        if self.LogObject:
            self.LogObject.setUserAgent(userAgent)
            self.LogObject.setKeyword(keyWord)
            self.LogObject.camino(ruta)
            self.LogObject.endCookie()

        