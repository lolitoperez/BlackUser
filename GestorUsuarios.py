from datetime import datetime
from UsuarioWeb import UsuarioWeb
from ValueProxies import ValueProxies
from random import randrange
from traceback import format_exc
from os import system
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
        self.local_logger = logging.getLogger('super_logger')
        self.local_logger.setLevel(logging.DEBUG)
        self.local_logger.setLevel(logging.INFO)
        self.local_logger.setLevel(logging.WARNING)
        handler = handlers.TimedRotatingFileHandler('/home/'+getuser()+'/BlackUser/logs_superuser.txt', when='midnight')
        formater = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
        handler.setFormatter(formater)
        self.local_logger.addHandler(handler)
        self.proxy_manager = ValueProxies()
        self.listProxies = []
        self.users = {'padreSonador': {'rangeTime':range(0,24), 'typeUser':'padreSonador'}, 'solteraPlanificadora': {'rangeTime':range(0,24), 'typeUser':'solteraPlanificadora'},'mamaPrimeriza': {'rangeTime':range(0,24), 'typeUser':'mamaPrimeriza'},'inversionista2': {'rangeTime':range(0,24), 'typeUser':'inversionista2'},'solteroAfterOffice': {'rangeTime':range(0,24), 'typeUser':'solteroAfterOffice'},'padreAbuelo': {'rangeTime':range(0,24), 'typeUser':'padreAbuelo'}}

    def createUsers(self, timeMinutes):
        ip = self.__get_ip()
        startTime = datetime.now()
        timeSeconds = int(timeMinutes*60)
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
                    system('nohup tor &')
                    print("aaaa")
                    logObject = Log(proxy,dictproxy,ip)
                    #este usuario tiene la proxy cargada como campo, la cargará en firefox
                    self.local_logger.info('Instanciando usuario')
                    userWeb = UsuarioWeb(typeUser, proxy, self.__getUsers(), logObject)
                    self.local_logger.info('Fin instancia objeto')
                    self.local_logger.info('Iniciando processUser')
                    self.proccessUser(userWeb)
                    self.local_logger.info('Iniciando usuario')
                    hotkey('ctrl', 'w')
                    hotkey('ctrl', 'w')
                    system('pkill -9 firefox')
                    system('killall tor')
                    system('echo "DarkUser5" | sudo -S pkill mongod')
                    system('rm -r nohup.out')
                    system('rm -r mongo.out')
                    # userWebTmp = copy(userWeb)
                    # del userWeb
                    
                else:
                    timesExecute = timesExecute + 1
                    system('echo "DarkUser5" | sudo -S pkill mongod')
                    system('rm -r mongo.out')

                if timesExecute == 4:
                    break
                timeRest = datetime.now() - startTime
                timeRest = timeRest.seconds


        except Exception as e:
            print(e)
            self.__set_error(format_exc(), 'E_superuser.txt')
            
            hotkey('ctrl', 'w')
            hotkey('ctrl', 'w')
            system('pkill -9 firefox')
            system('killall tor')
            system('echo "DarkUser5" | sudo -S pkill mongod')

        # Finalizado
    def proccessUser(self, user):
        user.setParameters()
        
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
    timeMinutes = sys.argv[1] # 1 a 60
    recurrents = sys.argv[2] # 1 a 10. Porcentaje de usuarios recrrentes
    system('export DISPLAY=:4')
    gu = GestorUsuarios(int(recurrents))
    gu.createUsers(int(timeMinutes))

