from pyautogui import hotkey
import pyautogui as pya
from os import system

pya.FAILSAFE = False

system('pkill firefox')
system('firefox -p default')

hotkey('ctrl', 'w')
hotkey('ctrl', 'w')
hotkey('ctrl', 'w')
hotkey('ctrl', 'w')
hotkey('ctrl', 'w')
hotkey('ctrl', 'w')
hotkey('ctrl', 'w')
hotkey('ctrl', 'w')
hotkey('ctrl', 'w')
hotkey('ctrl', 'w')

system('pkill -9 firefox')