##Nuevo esuema de cerebro

import paramiko
import multiprocessing
import numpy as np
from pymongo import MongoClient
from time import sleep
#from traceback import print_exc
from datetime import datetime

from pytz import timezone
import warnings

warnings.filterwarnings(action='ignore',module='.*paramiko.*')



def obtener_ssh(ip,n):

    if n==1:
        #Usuario 1 : ubuntu2
        ssh = paramiko.SSHClient()
        # key = paramiko.RSAKey.from_private_key_file('/Users/bernardoriveracamacho/.ssh/')
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, username='ubuntu2', timeout=30)
        return ssh
    elif n==2:

        #Usuario 2 : ubuntu3
        ssh2 = paramiko.SSHClient()
        # key = paramiko.RSAKey.from_private_key_file('/Users/bernardoriveracamacho/.ssh/')
        ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh2.connect(hostname=ip, username='ubuntu3', timeout=30)
        return ssh2

    elif n==3:
        #Usuario 3 : ubuntu4
        ssh3 = paramiko.SSHClient()
        # key = paramiko.RSAKey.from_private_key_file('/Users/bernardoriveracamacho/.ssh/')
        ssh3.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh3.connect(hostname=ip, username='ubuntu4', timeout=30)
        return ssh3
    
    else:
        return None



def ejecutar_gestor_usuarios(ip,n,ssh):
    try:
        if n==1:

            #Usuario 1 : ubuntu2
            stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2; cd superusercloud; python3 GestorUsuarios.py 15 3')
            print("Se ejecuto SU en IP",ip, "Usuario: ",n)
        elif n==2:

        
            #Usuario 2 : ubuntu3
            stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:3; cd superusercloud; python3 GestorUsuarios.py 15 3')
            print("Se ejecuto SU en IP",ip, "Usuario: ",n)
        elif n==3:

            #usuario 3 : ubuntu4
            stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:4; cd superusercloud; python3 GestorUsuarios.py 15 3')
            print("Se ejecuto SU en IP",ip, "Usuario: ",n)

        else:
            print("Ningun usuario ",n)
            

        return True
    except:
        return False


def gestor_esta_ejecutandose_en_ip(ip,n,ssh):

    if n==1:

        try:

            #Usuario 1 : ubuntu2
            stdin, stdout, stderr = ssh.exec_command('pgrep -af "python3 GestorUsuarios.py" -u ubuntu2')

            salida = list(stdout)

            if len(salida) == 0:
                return False
            else:
                # print(salida)
                primer_salida = salida[0]

                if primer_salida.find('python3 GestorUsuarios.py') == -1:
                    return False
                else:
                    #print("Se esta ejecutando SU en",ip, "Usuario: ",n)
                    return True

        except:
            print ("Error en conexion ssh usuario",n,"IP: ",ip)

    elif n==2:

        try:
            #Usuario 1 : ubuntu2
            stdin, stdout, stderr = ssh.exec_command('pgrep -af "python3 GestorUsuarios.py" -u ubuntu3')
    
            
            salida = list(stdout)

            if len(salida) == 0 :
                return False
            else:
                # print(salida)
                primer_salida = salida[0]

                if primer_salida.find('python3 GestorUsuarios.py') == -1 :
                    return False
                else:
                    #print("Se esta ejecutando SU en",ip, "Usuario: ",n)
                    return True
        except:
            print ("Error en conexion ssh usuario",n,"IP: ",ip)

        

    elif n==3:
        try:
            #Usuario 1 : ubuntu2
            stdin, stdout, stderr = ssh.exec_command('pgrep -af "python3 GestorUsuarios.py" -u ubuntu4')
    
            
            salida = list(stdout)

            if len(salida) == 0 :
                return False
            else:
                # print(salida)
                primer_salida = salida[0]

                if primer_salida.find('python3 GestorUsuarios.py') == -1 :
                    return False
                else:
                    #print("Se esta ejecutando SU en",ip, "Usuario: ",n)
                    return True
        except:
            print ("Error en conexion ssh usuario",n,"IP: ",ip)
    else:
        pass


def detener_superuser(ip,n,ssh):

    if n==1:

        stdin, stdout, stderr = ssh.exec_command('pkill -9 python3')
        stdin, stdout, stderr = ssh.exec_command('pkill -9 firefox')
        #stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2; cd superusercloud; python3 cerrador_ventanas.py')
        #stdin, stdout, stderr = ssh.exec_command('pkill -9 firefox')
        #stdin, stdout, stderr = ssh.exec_command('pkill -9 python3')

    elif n==2:


        stdin, stdout, stderr = ssh.exec_command('pkill -9 python3')
        stdin, stdout, stderr = ssh.exec_command('pkill -9 firefox')
        #stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:3; cd superusercloud; python3 cerrador_ventanas.py')
        #stdin, stdout, stderr = ssh.exec_command('pkill -9 firefox')
        #stdin, stdout, stderr = ssh.exec_command('pkill -9 python3')
    elif n==3:

        
        stdin, stdout, stderr = ssh.exec_command('pkill -9 python3')
        stdin, stdout, stderr = ssh.exec_command('pkill -9 firefox')
        #stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:4; cd superusercloud; python3 cerrador_ventanas.py')
        #stdin, stdout, stderr = ssh.exec_command('pkill -9 firefox')
        #stdin, stdout, stderr = ssh.exec_command('pkill -9 python3')
    else:
        pass



def debo_detener_superuser():
    db = MongoClient('mongodb://Scraper%2Fops:R3vim3x5o5%2F%2F@104.199.125.135:27017/admin').XLamudi
    coleccion_status = db['status_superuser_cloud']
    documento_status = coleccion_status.find_one({'name': 'detener'})
    return documento_status['detener']


def hora_dia(hora,minutos):
    print("Ejecutando hora_dia")
    while True:
        hora.value=int(datetime.now(timezone('Mexico/General')).hour)
        minutos.value=int(datetime.now(timezone('Mexico/General')).minute)
        sleep(900)

def obtener_randinstancias(i,maxi):
    a=int(round(np.random.normal(i,int(5*maxi/100))))
    if a>maxi:
        return maxi
    elif a<1:
        return 1
    else:
        return a

def SUinstancias(activa,usuario,ip,):
    #print(usuario)
    try:
        ssh = obtener_ssh(ip,usuario+1) #usuario+1
        if activa:
            
    
            if gestor_esta_ejecutandose_en_ip(ip,usuario+1,ssh):
                pass
            else:
        
                detener_superuser(ip,usuario+1,ssh)
                ejecutar_gestor_usuarios(ip,usuario+1,ssh)
        else:


            if gestor_esta_ejecutandose_en_ip(ip,usuario+1,ssh):
                detener_superuser(ip,usuario+1,ssh)
            else:
                pass
        if ssh:
            ssh.close()
            del ssh
    except :
        print("Usuario no se inicia")
        print("Se cerro el proceso {} {}".format(usuario,ip))
	



def asignacion_intancias(hora,minutos,instancias,lista_ips):

    print("Ejecutando asignacion_intancias2")
    numeroUsuariosXinstancia=2
    numero_intancias=len(lista_ips)
    grupos=50 #grupos de 'n' 
    IPS_seccionada=[lista_ips[i:i+grupos] for i in range(0,len(lista_ips),grupos)]


    MaximoUsuarios=numero_intancias*numeroUsuariosXinstancia
    Activa=[[False for i in range(numero_intancias)] for j in range(numeroUsuariosXinstancia)]
	
    for usuario in range(numeroUsuariosXinstancia):
        for num_bloque_ips,bloque_ips in enumerate(IPS_seccionada):
            hilos=[]
            for num_ip,ip in enumerate(bloque_ips):
                h=multiprocessing.Process(target=SUinstancias,daemon=True,args=(Activa[usuario][num_bloque_ips*grupos+num_ip],usuario,ip,))
                h.start()
                hilos.append(h)

            for h in hilos:
                h.join()
            
            del hilos
			
    try:
        while True:
            if debo_detener_superuser():
                Activa=[[False for i in range(numero_intancias)] for j in range(numeroUsuariosXinstancia)]
                for usuario in range(numeroUsuariosXinstancia):
                    for num_bloque_ips,bloque_ips in enumerate(IPS_seccionada):
                        hilos=[]
                        for num_ip,ip in enumerate(bloque_ips):
                            h=multiprocessing.Process(target=SUinstancias,daemon=True,args=(Activa[usuario][num_bloque_ips*grupos+num_ip],usuario,ip,))
                            h.start()
                            hilos.append(h)
                        for h in hilos:
                            h.join()
                        del hilos
                sleep(30)
                break

            else:
                NumeroInstancias=obtener_randinstancias(instancias[int(hora.value)][int(minutos.value/15)],numero_intancias) #instancias[int(hora.value)][int(minutos.value/15)] ##intancias cada 15 min
                print(NumeroInstancias)
                for i in range(MaximoUsuarios):
                    if i<NumeroInstancias*numeroUsuariosXinstancia:
                        a=True
                        Activa[i//numero_intancias][i%numero_intancias] = a
                    else:
                        a=False
                        Activa[i//numero_intancias][i%numero_intancias] = a
                print(Activa)

                for usuario in range(numeroUsuariosXinstancia):
                    for num_bloque_ips,bloque_ips in enumerate(IPS_seccionada):
                        hilos=[]
                        for num_ip,ip in enumerate(bloque_ips):
                            h=multiprocessing.Process(target=SUinstancias,daemon=True,args=(Activa[usuario][num_bloque_ips*grupos+num_ip],usuario,ip,))
                            h.start()
                            hilos.append(h)
                        for h in hilos:
                            h.join()
                        del hilos
				#print("Tiempo en ejecutar SU o no las intancias = ",datetime.now()-xtime)
                sleep(30)
    except:
        print("Deteniendo Superuser por corte de programa")
        Activa=[[False for i in range(numero_intancias)] for j in range(numeroUsuariosXinstancia)]
        for usuario in range(numeroUsuariosXinstancia):
            for num_bloque_ips,bloque_ips in enumerate(IPS_seccionada):
                hilos=[]
                for num_ip,ip in enumerate(bloque_ips):
                    h=multiprocessing.Process(target=SUinstancias,daemon=True,args=(Activa[usuario][num_bloque_ips*grupos+num_ip],usuario,ip,))
                    h.start()
                    hilos.append(h)
                for h in hilos:
                    h.join()
                del hilos


def obtener_lista_ips():
    db = MongoClient('mongodb://Scraper%2Fops:R3vim3x5o5%2F%2F@104.199.125.135:27017/admin').XLamudi
    lista_ips = [x['Ip'] for x in db['instancias_2'].find({'status': 'inactiva'})]
    return lista_ips

def obtener_lista_ips_cloud():
    db = MongoClient('mongodb://Scraper%2Fops:R3vim3x5o5%2F%2F@104.199.125.135:27017/admin').XLamudi
    lista_ips = [x['Ip'] for x in db['instancias_cloud'].find({'status': 'activa'})]
    return lista_ips


def vigila():  # Esta funcion dentro de un hilo inicia los hilos y los termina
    
    lista_ips = obtener_lista_ips()+obtener_lista_ips_cloud()#[0:-1]
    print(lista_ips)
    print(len(lista_ips))
    lista_ips2=lista_ips




    #Datos compartidos por procesos
    hora=multiprocessing.Value('d',0)
    minuto=multiprocessing.Value('d',0)



    #num=100
    #instancias=[[num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num]]
    instancias=[[84, 73, 68, 65], [62, 58, 54, 49], [44, 40, 36, 33], [31, 29, 29, 29], [29, 30, 32, 34], [36, 38, 41, 43], [46, 49, 52, 55], [58, 61, 64, 66], [69, 72, 75, 78], [80, 83, 86, 88], [91, 93, 95, 96], [98, 99, 100, 100], [100, 99, 98, 97], [96, 94, 92, 91], [90, 89, 88, 88], [89, 90, 92, 94], [97, 100, 104, 107], [110, 113, 116, 118], [120, 120, 120, 120], [119, 117, 115, 113], [110, 108, 106, 105], [103, 101, 100, 98], [96, 94, 92, 91], [90, 90, 89, 85]]
    #instancias=[[283, 247, 231, 222], [212, 201, 187, 172], [157, 142, 130, 120], [113, 108, 106, 106], [108, 111, 116, 122], [129, 136, 145, 153], [162, 171, 180, 190], [199, 208, 218, 227], [236, 245, 254, 263], [271, 280, 288, 296], [304, 311, 317, 323], [327, 331, 333, 333], [333, 331, 328, 325], [320, 315, 310, 305], [301, 298, 297, 297], [299, 302, 308, 315], [325, 335, 345, 357], [367, 377, 386, 393], [397, 400, 400, 398], [394, 388, 382, 375], [368, 361, 354, 349], [343, 338, 333, 328], [322, 316, 310, 305], [302, 301, 299, 287]]
    #instancias=[[142, 124, 116, 111], [107, 101, 94, 86], [79, 72, 66, 61], [57, 55, 54, 53], [54, 56, 58, 61], [65, 69, 73, 77], [82, 86, 91, 95], [100, 105, 109, 114], [118, 123, 127, 132], [136, 140, 145, 149], [152, 156, 159, 162], [164, 166, 167, 167], [167, 166, 165, 163], [160, 158, 156, 153], [151, 150, 149, 149], [150, 152, 155, 158], [163, 168, 173, 179], [184, 189, 193, 197], [199, 200, 200, 199], [197, 195, 191, 188], [184, 181, 178, 175], [172, 170, 167, 164], [161, 158, 155, 153], [152, 151, 150, 144]]
    #instancias=[[41, 35, 33, 31], [30, 28, 26, 24], [21, 19, 17, 16], [14, 14, 13, 13], [14, 14, 15, 16], [17, 18, 19, 21], [22, 23, 25, 26], [28, 29, 31, 32], [34, 35, 36, 38], [39, 41, 42, 43], [44, 45, 46, 47], [48, 48, 49, 49], [49, 49, 48, 48], [47, 46, 45, 44], [44, 43, 43, 43], [43, 44, 45, 46], [48, 50, 52, 54], [56, 57, 59, 60], [60, 60, 60, 60], [60, 59, 58, 56], [55, 54, 52, 51], [51, 50, 49, 48], [47, 46, 45, 44], [44, 44, 43, 42]]
    #instancias=[[7, 6, 5, 5], [5, 5, 4, 4], [3, 3, 3, 2], [2, 2, 2, 2], [2, 2, 2, 2], [2, 3, 3, 3], [3, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6], [7, 7, 7, 7], [8, 8, 8, 8], [8, 8, 8, 8], [8, 8, 8, 8], [8, 8, 8, 8], [7, 7, 7, 7], [7, 7, 8, 8], [8, 9, 9, 9], [10, 10, 10, 10], [11, 11, 11, 11], [10, 10, 10, 10], [9, 9, 9, 9], [9, 9, 8, 8], [8, 8, 8, 8], [7, 7, 7, 7]]
    #instancias=[[22, 19, 17, 16],[16, 15, 13, 12],[11, 10, 9, 8],[7, 7, 7, 7],[7, 7, 7, 8],[8, 9, 10, 11],[11, 12, 13, 14],[15, 15, 16, 17],[18, 18, 19, 20],[21, 21, 22, 23],[24, 24, 25, 25],[26, 26, 26, 26],[26, 26, 26, 25],[25, 24, 24, 24],[23, 23, 23, 23],[23, 23, 24, 25],[26, 27, 28, 29],[30, 31, 32, 32],[33, 33, 33, 33],[32, 32, 31, 30],[29, 29, 28, 27],[27, 27, 26, 26],[25, 25, 24, 24],[23, 23, 23, 22]]
    #instancias = [[7, 6, 5, 5],[5, 5, 4, 4],[3, 3, 3, 2],[2, 2, 2, 2],[2, 2, 2, 2],[2, 3, 3, 3],[3, 4, 4, 4],[5, 5, 5, 5],[6, 6, 6, 6],[7, 7, 7, 7],[8, 8, 8, 8],[8, 8, 8, 8],[8, 8, 8, 8],[8, 8, 8, 8],[7, 7, 7, 7],[7, 7, 8, 8],[8, 9, 9, 9],[10, 10, 10, 10],[11, 11, 11, 11],[10, 10, 10, 10],[9, 9, 9, 9],[9, 9, 8, 8],[8, 8, 8, 8],[7, 7, 7, 7]]
    Asigancion = multiprocessing.Process(target=asignacion_intancias,daemon=False,args=(hora,minuto,instancias,lista_ips2,))
    Dia = multiprocessing.Process(target=hora_dia,daemon=True,args=(hora,minuto))
    Dia.start()
    sleep(1)#evitar el cero en hora y en minuto 
    Asigancion.start()
    ##h





    Dia.join()
    Asigancion.join()

    


vigila()