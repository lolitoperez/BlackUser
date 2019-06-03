from pyautogui import PAUSE,FAILSAFE,typewrite, keyDown,keyUp,size,moveTo,press, locateCenterOnScreen, scroll, center, click, hotkey
from time import sleep
from sys import platform
from os import getcwd
import random
from datetime import datetime
import logging
import pyperclip as clipboard

class KeyBoard(object):
    """docstring for KeyBoard"""
    def __init__(self):
        super(KeyBoard, self).__init__()
        self.PATH_IMAGE = self.__getPathSystem()
        PAUSE = 3
        FAILSAFE = False
        self.local_logger = logging.getLogger('super_logger')
        self.local_logger.setLevel(logging.DEBUG)


    def writeAndEnter(self, text, verbose=False):

        typewrite(text+'\n', interval=random.uniform(.3,.5))#round(random.uniform(.1,1), 2))
        sleep(random.randint(1,3))
        if verbose:
            print('escribi ', text)

    def get_focus_on_search_bar(self):
        if self.PATH_IMAGE == 'Linux':
            # print('[X] -- Es Linux')
            moveTo(size()[0] / 2, size()[1] / 2)
            click()
            sleep(1)
            hotkey('ctrl', 'k')
        else:
            # print('[X] -- Es Mac')
            moveTo(size()[0] / 2, size()[1] / 2)
            click()
            sleep(1)
            hotkey('command', 'k')

    def searchKeyBoard(self, browser):
        press('enter')
        return True
        isInScreen = False
        location = None
        intentos  = 0
        if browser == 'google': # y es movil
            press('enter')
            self.local_logger.info('Empezando intentos de busqueda del cuadro de inicio de sesión')
            while not isInScreen and intentos < 60:
                self.local_logger.info('Intento ' + str(intentos))
                #print('[X] -- Intentos ', intentos)
                isInScreen, location = self.findImage(self.PATH_IMAGE+'/'+'key' + '.png',True, .8)
                #isInScreen, location = self.findImage(self.PATH_IMAGE+'/'+browser+ '.png',True, .8)
                intentos = intentos + 1
                #print("Estoy aqui HDSPM")

            if intentos == 60 and not isInScreen:
                self.local_logger.info('No encontré la imagen')
                #print('[X].....no encontre la imagen')
                # print('[X] -- No encontré la imagen')
                return False
            else:
                self.local_logger.info('Encontré la imagen')
                #print('[X]----- encontre la imagen')
                typewrite('su') ##usuario

                press('tab')
                typewrite('rre') ##contra
                press('enter')
                self.local_logger.info('Escibrí usuario y contraseña')
                return True

            if self.PATH_IMAGE == 'Linux':
                # print('[X] -- Es Linux')
                moveTo(size()[0]/2, size()[1]/2)
                click()
                sleep(2)
                hotkey('ctrl', 'k')
            else:
                # print('[X] -- Es Mac')
                moveTo(size()[0]/2, size()[1]/2)
                click()
                sleep(2)
                hotkey('command','k')


    def findSiteKeyBoard(self, site):
        self.local_logger.info('Buscando la imagen')
        isInScreen = False
        attempts = 0
        location = None
        proccess = True
        intentos = 0
        attemptsPages = 0
        siguiente= 1
        
        sleep(10)#tiempo que tarda en cargar la pagina

        while proccess:
            #print('[X] -- Buscando imagen')
            attempts = 0
            self.local_logger.info('Iniciando intentos')
            while attempts < 5:
                isInScreen, location = self.findImage(self.PATH_IMAGE+'/'+'propiedadescel' + '.png',True, .9)### find letshome
                #isInScreen, location = self.findImage(self.PATH_IMAGE+'/'+'testing' + '.png',True, .8)### find testingrevimex
                if isInScreen:
                    break
                else:
                    isInScreen, location = self.findImage(self.PATH_IMAGE + '/' + 'propiedades' + '.png', True, .9)
                    if isInScreen:
                        break
                    
                attempts = attempts + 1


            if intentos == 6 and not isInScreen:
                self.local_logger.info('No encontré la imagen')
                return False



            intentos = intentos + 1

            if intentos == 4:
                self.local_logger.info('recargando la página')
                self.reloadPage()

            if isInScreen:
                self.local_logger.info('Encontrada')
                centerImage = location
                click(centerImage)
                click(centerImage)
                self.local_logger.info('Hice click')
                proccess = False

            else:
                self.local_logger.info('Haciendo scroll')
                self.scrollWeb(random.randint(5,7)) #(1,5)

        return True

    def changePage(self, imagen,log_url):
        FAILSAFE = False
        isInScreen = False
        attempts = 0
        location = None
        proccess = True
        intentos = 0
        timepoCP=datetime.now()
        errgl=False
        self.local_logger.info('Buscando la imagen de la pagina ' + imagen)
        while proccess:
            #print('[X] -- Buscando imagen')
            attempts = 0
            self.local_logger.info('Iniciando intentos')
            while attempts < 6:
                press('esc')
                press('esc')
                press('esc')
                self.local_logger.info('Intento ' + str(attempts))
                isInScreen, location = self.findImage(self.PATH_IMAGE+'/'+'regresar'+ '.png',True, .6)
                if isInScreen:
                    break
                
                attempts = attempts + 1

            if intentos == 2 and not isInScreen:
                self.local_logger.info('Recargando página')
                self.reloadPage()
                sleep(5)

            if intentos == 3 and not isInScreen:
                errgl=True
                proccess=False
                break

            intentos = intentos + 1

            if isInScreen:
                #log_url.set_url_clickeado(self.obtener_url_de_barra_de_busqueda())
                self.local_logger.info('Encontrada imagen ' + imagen)
                centerImage = location
                click(centerImage)
                sleep(5)#10
                self.scrollWeb(random.randint(3,12))
                proccess = False
                return 'exitosa'

        self.local_logger.info('No encontrada imagen')
        if errgl:
            return 'exitosa > google, no exitosa > letshome'+'Tiempo:'+str(datetime.now()-timepoCP)

        

    def findYellow(self):
        isInScreen = False
        attempts = 0
        location = None
        proccess = True
        intentos = 0
        
        while proccess:
            #print('[X] -- Buscando imagen')
            attempts = 0
            for i in range(5):      
                isInScreen, location = self.findImage(self.PATH_IMAGE+'/adfly/'+'deny'+ '.png',True, .7)
                if isInScreen:
                    click(location)
                    break
                sleep(2)

            while attempts < 5:
                sleep(1)
                isInScreen, location = self.findImage(self.PATH_IMAGE+'/adfly/saltar.png',True, .9)
                if isInScreen:
                    break
                

                attempts = attempts + 1

            if intentos == 15 and not isInScreen:
                return False

            intentos = intentos + 1

            if isInScreen:
                centerImage = location
                click(centerImage)
                click(centerImage)
                click(centerImage)
                proccess = False



    def findImage(self, image,grayscale,confidence):

        location = None
        isInScreen = False

        try:
            location = locateCenterOnScreen(image,grayscale=grayscale, confidence=confidence)
        except Exception as e:
            location = None

        if location:
            isInScreen = True

        return isInScreen, location

    def scrollWeb(self, clicks, up=False):

        if not up:
            clicks = clicks * -1

        scroll(clicks)

    def __getPathSystem(self):
        """Regresa el sistema operativo en el que se está ejecutando"""

        if platform == "linux" or platform == "linux2":
            return 'Linux'

        elif platform == "darwin":
            return 'Mac'
        # elif platform == "win32":

    def closeTabs(self):

        hotkey('ctrl','w')
        hotkey('ctrl','w')

        
    def reloadPage(self):
        hotkey('ctrl','r')

    def obtener_url_de_barra_de_busqueda(self):

        press('esc')
        press('esc')
        try:
            hotkey('ctrl','l')
        except:
            print("fallo en ctrl + l")
        try:
            hotkey('ctrl','c')
        except:
            print("fallo een ctrl + c")
        try:

            return clipboard.paste()
        except:
            print("fallo clip")

        

    def delAllCharacters(self):

        if self.__getPathSystem() == 'Mac':
            hotkey('command','a')
        else:
            hotkey('ctrl','a')
    
        sleep(1)



