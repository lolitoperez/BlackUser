import os
import webbrowser as wb
import pyautogui
import time
import random
import re
import sys
import datetime
import pymongo
import traceback
import requests as rq
from bs4 import BeautifulSoup
from pprint import pprint



IPS,Puerto=[],[]
profileDirectory=['/home/ubuntu2/firefoxprofiles/profile'+str(i) for i in range(0,44)]

def profileCreator():
    os.system('mkdir /home/ubuntu2/firefoxprofiles/')
    for i in range (0,44):
        os.system('firefox -CreateProfile "profile'+str(i)+' /home/ubuntu2/firefoxprofiles/profile'+str(i)+'"')

def buscarIp():
    soup = BeautifulSoup(open('Ips.html'), "html.parser")
    for x in soup.find_all('tbody'):
        for y in x.find_all('td',class_='tdl'):
            yield y.getText()

def buscarPuertos():
    soup = BeautifulSoup(open('Ips.html'), "html.parser")
    for x in soup.find_all('tbody'):
        for y in x.find_all_next('td',class_='tdl'):
            y=y.find_next_sibling("td")
            yield y.getText()

def recabarIPs():
    os.system('rm Ips.html')

    wb.open('https://hidemyna.me/es/proxy-list/?country=MX#list')
    time.sleep(7)

    for i in range(0,44):
        pyautogui.press('up')
        time.sleep(.3)

    pyautogui.press('enter')
    time.sleep(7)
    pyautogui.rightClick(201,200)

    for i in range(0,7):
        pyautogui.press('down')
        time.sleep(1)

    pyautogui.press('enter')
    time.sleep(1)

    pyautogui.hotkey('ctrl','a')
    time.sleep(1)

    pyautogui.hotkey('ctrl','c')
    time.sleep(1)

    os.system('gedit &')
    time.sleep(0.3)

    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('v')
    pyautogui.keyUp('v')
    pyautogui.keyUp('ctrl')
    time.sleep(0.3)

    pyautogui.hotkey('ctrl','s')
    time.sleep(0.2)

    pyautogui.typewrite('Ips.html',interval=0.1)
    pyautogui.hotkey('enter')
    time.sleep(0.2)

    pyautogui.hotkey('ctrl', 'w')
    time.sleep(0.2)

    pyautogui.hotkey('ctrl', 'w')
    time.sleep(0.2)

    os.system('pkill gedit')
    time.sleep(1)

    os.system('pkill firefox')

    return [elementos for elementos in buscarIp()],[elementos for elementos in buscarPuertos()]

def proceso():
    #inicio=datetime.datetime.now()
    #fin=datetime.datetime.now()

    #duracion=float(sys.argv[1])
    #duracion=duracion*3600

    #resultado=fin-inicio

    #os.system('firefox')
    #wb.open('https://www.google.com')
    #time.sleep(5)
    global IPS,Puerto

    if pyautogui.locateCenterOnScreen('max.png',grayscale=True)!=None:
        maxx,maxy=pyautogui.locateCenterOnScreen('max.png',grayscale=True)                
        pyautogui.click(maxx,maxy)
        time.sleep(1)

    menux,menuy=pyautogui.locateCenterOnScreen('Menu.png')
    pyautogui.click(menux,menuy)
    time.sleep(1)

    prefx,prefy=pyautogui.locateCenterOnScreen('Preferencias.png')
    pyautogui.click(prefx,prefy)
    time.sleep(1)

    pyautogui.scroll(-30)
    time.sleep(.3)
    config=pyautogui.locateCenterOnScreen('Configuracion.png')
    configx,configy=config
    pyautogui.click(configx,configy)
    time.sleep(1)

    #print(pyautogui.locateCenterOnScreen('ProxyActivado.png'))
    #print(pyautogui.locateCenterOnScreen('Proxy.png'))
    pyautogui.click(201,200)

    if pyautogui.locateCenterOnScreen('ProxyActivado.png',grayscale=True)==None:
        proxyx,proxyy=pyautogui.locateCenterOnScreen('Proxy.png',grayscale=True)
        pyautogui.click(proxyx,proxyy)
        time.sleep(1)

    #pyautogui.click(201,337)

    pyautogui.press('tab')
    time.sleep(1)

    indice=random.randint(0,len(IPS)-1)
    pyautogui.typewrite(IPS[indice],interval=0.25)
    time.sleep(1)

    pyautogui.press('tab')
    time.sleep(1)

    pyautogui.typewrite(Puerto[indice],interval=0.25)
    time.sleep(1)

    if pyautogui.locateCenterOnScreen('CheckBox.png',grayscale=True)!=None:
        pyautogui.press('tab')
        time.sleep(1)

        pyautogui.press('space')
        time.sleep(1)

    pyautogui.press('enter')
    time.sleep(1)

    pyautogui.hotkey('ctrl','w')
    time.sleep(2)

    pyautogui.hotkey('ctrl','w')
    time.sleep(2)

if os.path.exists('/home/ubuntu2/firefoxprofiles')==False:
    profileCreator()

IPS,Puerto=recabarIPs()
time.sleep(1)

pprint(IPS)
pprint(Puerto)

for i in range (1,44):

    os.system('firefox &')
    time.sleep(2)

    pyautogui.press('down')
    time.sleep(.3)

    pyautogui.press('enter')
    time.sleep(4)
    proceso()
