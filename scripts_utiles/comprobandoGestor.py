import paramiko
import multiprocessing
import numpy as np
from pymongo import MongoClient
from time import sleep
from traceback import print_exc
from datetime import datetime
from random import randint
import random
from pytz import timezone


def obtener_ssh(ip,n):

    if n==1:

        #Usuario 1 : ubuntu2
        ssh = paramiko.SSHClient()
        # key = paramiko.RSAKey.from_private_key_file('/Users/bernardoriveracamacho/.ssh/')
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, username='ubuntu2', timeout=10)
        return ssh
    elif n==2:

        #Usuario 2 : ubuntu3
        ssh2 = paramiko.SSHClient()
        # key = paramiko.RSAKey.from_private_key_file('/Users/bernardoriveracamacho/.ssh/')
        ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh2.connect(hostname=ip, username='ubuntu3', timeout=10)
        return ssh2

    elif n==3:
        pass
        # #Usuario 3 : ubuntu4
        # ssh3 = paramiko.SSHClient()
        # # key = paramiko.RSAKey.from_private_key_file('/Users/bernardoriveracamacho/.ssh/')
        # ssh3.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh3.connect(hostname=ip, username='ubuntu4', timeout=10)
        # return ssh3
    
    else:
        return None



def ejecutar_gestor_usuarios(ip,n):
    try:
        if n==1:
            ssh=obtener_ssh(ip,n)

            #Usuario 1 : ubuntu2
            stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2; cd superusercloud; python3 GestorUsuarios.py 5 30')
            #ssh.close()
        elif n==2:

            ssh=obtener_ssh(ip,n)
        
            #Usuario 2 : ubuntu3
            stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:3; cd superusercloud; python3 GestorUsuarios.py 5 30')
            #ssh.close()
        elif n==3:
            pass
            # ssh=obtener_ssh(ip,n)
            # #usuario 3 : ubuntu4
            # stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:3; cd superusercloud; python3 GestorUsuarios.py 5 30')
        
        else:
            #print("Ningun usuario ",n)
            pass

        return True
    except:
        return False


def gestor_esta_ejecutandose_en_ip(ip,n):

    if n==1:

        try:
            ssh = obtener_ssh(ip,n)
            #Usuario 1 : ubuntu2
            stdin, stdout, stderr = ssh.exec_command('pgrep -af "python3 GestorUsuarios.py"')
    
            #ssh.close()
        except:
            print("Error conectandose ssh")

        salida = list(stdout)

        if len(salida) == 0:
            print("NO se esta ejecutando Gestor en usuario :",n,"IP : ",ip)
            
        else:
            # print(salida)
            primer_salida = salida[0]

            if primer_salida.find('python3 GestorUsuarios.py') == -1:
                print("NO se esta ejecutando Gestor en usuario :",n,"IP : ",ip)
            else:
                print("SI se esta ejecutando Gestor en usuario :",n,"IP : ",ip)

    elif n==2:

        try:
            ssh = obtener_ssh(ip,n)
            #Usuario 1 : ubuntu2
            stdin, stdout, stderr = ssh.exec_command('pgrep -af "python3 GestorUsuarios.py"')
    
            #ssh.close()
        except:
            print("Error conectandose ssh")

        salida = list(stdout)
        if len(salida) == 0 :
            print("NO se esta ejecutando Gestor en usuario :",n,"IP : ",ip)
        else:
            # print(salida)
            primer_salida = salida[0]

            if primer_salida.find('python3 GestorUsuarios.py') == -1 :
                print("NO se esta ejecutando Gestor en usuario :",n,"IP : ",ip)
            else:
                print("SI se esta ejecutando Gestor en usuario :",n,"IP : ",ip)

    elif n==3:
        pass
        # try:
        #     ssh = obtener_ssh(ip,n)
        #     #Usuario 1 : ubuntu3
        #     stdin, stdout, stderr = ssh.exec_command('pgrep -af "python3 GestorUsuarios.py"')
        #     #ssh.close()
        # except:
        #     return False

        # salida = list(stdout)
        # if len(salida) == 0 :
        #     return False
        # else:
        #     # print(salida)
        #     primer_salida = salida[0]

        #     if primer_salida.find('python3 GestorUsuarios.py') == -1 :
        #         return False
        #     else:
        #         return True
    else:
        pass


def detener_superuser(ip,n):

    if n==1:

        ssh = obtener_ssh(ip,n)

        stdin, stdout, stderr = ssh.exec_command('pkill -9 python3')
        stdin, stdout, stderr = ssh.exec_command('pkill -9 firefox')
        stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2; cd superusercloud; python3 cerrador_ventanas.py')
        #ssh.close()
        print("Deteniendo Usuario",n," IP:",ip)

    elif n==2:

        ssh = obtener_ssh(ip,n)

        stdin, stdout, stderr = ssh.exec_command('pkill -9 python3')
        stdin, stdout, stderr = ssh.exec_command('pkill -9 firefox')
        stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:3; cd superusercloud; python3 cerrador_ventanas.py')
        #ssh.close()
        print("Deteniendo Usuario",n," IP:",ip)
    elif n==3:

        ssh = obtener_ssh(ip,n)

        stdin, stdout, stderr = ssh.exec_command('pkill -9 python3')
        stdin, stdout, stderr = ssh.exec_command('pkill -9 firefox')
        stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:4; cd superusercloud; python3 cerrador_ventanas.py')
        #ssh.close()
        print("Deteniendo Usuario",n," IP:",ip)
    else:
        pass



def debo_detener_superuser():
    db = MongoClient('mongodb://Scraper%2Fops:R3vim3x5o5%2F%2F@13.52.11.40:27017/admin').XLamudi
    coleccion_status = db['status_superuser_cloud']
    documento_status = coleccion_status.find_one({'name': 'detener'})
    return documento_status['detener']


def vigilar_instancia(ip_instancia, num_instancia):
    contador_excepciones = 0
    while True:
        try:
            debo_detenerlo = debo_detener_superuser()
            if debo_detenerlo:
                #print('deteniendo superuser', ip_instancia)
                detener_superuser(ip_instancia,1)

                break
                
            if gestor_esta_ejecutandose_en_ip(ip_instancia):
                #print('está en ejecución', ip_instancia)
                sleep(180)#randint(120, 240))
                continue
            else:
                #print('reinicie el superuser ', ip_instancia)
                detener_superuser(ip_instancia)
                ejecutar_gestor_usuarios(ip_instancia)
        except:
            contador_excepciones += 1
            with open('errores_minicerebro_superuser.txt', 'a+') as ferror:
                print_exc(file=ferror)
                cadena = ' ' + datetime.now().isoformat() + ' ip: ' + ip_instancia + '\n'
                ferror.write(cadena)
            if contador_excepciones == 30:
                break


def hora_dia(hora,minutos):
    print("Ejecutando hora_dia")
    while True:
        hora.value=int(datetime.now(timezone('Mexico/General')).hour)
        minutos.value=int(datetime.now(timezone('Mexico/General')).minute)
        sleep(900)


def asignacion_intancias(hora,minutos,instancias,lista_ips):

    print("Ejecutando asignacion_intancias")
    contador_excepciones=0
    while True:
        #print(int(hora.value),int(minutos.value/15))
        NumeroInstancias=instancias[int(hora.value)][int(minutos.value/15)]

        try:
            debo_detenerlo = debo_detener_superuser()
            if debo_detenerlo:
                #print('deteniendo superuser', ip_instancia
                for i in lista_ips:
                    detener_superuser(i)
                break
            else:
                listaIntanciasActivas=[]

                listaIntanciasActivas=[lista_ips(i) for i in range(NumeroInstancias)]

                # cnt=0
                # while cnt<NumeroInstancias:
                #     instanciasrand=lista_ips[random.randrange(0,len(lista_ips))]
                #     if instanciasrand not in listaIntanciasActivas:
                #         listaIntanciasActivas.append(instanciasrand)
                #         cnt=cnt+1
                hilos=[]
                #print(listaIntanciasActivas)
                for j in listaIntanciasActivas:
                    h=multiprocessing.Process(target=ejecutar_gestor_usuarios, args=(j,),daemon=True)
                    h.start()
                    hilos.append(h)
            
                
        except:
            contador_excepciones += 1
            with open('errores_minicerebro_superuser.txt', 'a+') as ferror:
                print_exc(file=ferror)
                cadena = ' ' + datetime.now().isoformat() + ' ip: ' +''+ '\n'
                ferror.write(cadena)
            if contador_excepciones == 30:
                break


        sleep(360)
        for j in hilos:
            j.terminate()
        hilos=[]
        for j in listaIntanciasActivas:
            h=multiprocessing.Process(target=detener_superuser, args=(j,),daemon=True)
            h.start()
            hilos.append(h)
        for j in hilos:
            j.terminate()

def ejecutar_instancias(hora,minutos,instancias,lista_ips):

    print("Ejecutando asignacion_intancias")
    contador_excepciones=0
    while True:
        #print(int(hora.value),int(minutos.value/15))
        NumeroInstancias=instancias[int(hora.value)][int(minutos.value/15)]

        try:
            debo_detenerlo = debo_detener_superuser()
            if debo_detenerlo:
                #print('deteniendo superuser', ip_instancia
                for i in lista_ips:
                    detener_superuser(i)
                break
            else:
                listaIntanciasActivas=[]

                listaIntanciasActivas=[lista_ips(i) for i in range(NumeroInstancias)]

                # cnt=0
                # while cnt<NumeroInstancias:
                #     instanciasrand=lista_ips[random.randrange(0,len(lista_ips))]
                #     if instanciasrand not in listaIntanciasActivas:
                #         listaIntanciasActivas.append(instanciasrand)
                #         cnt=cnt+1
                hilos=[]
                #print(listaIntanciasActivas)
                for j in listaIntanciasActivas:
                    h=multiprocessing.Process(target=ejecutar_gestor_usuarios, args=(j,),daemon=True)
                    h.start()
                    hilos.append(h)
            
                
        except:
            contador_excepciones += 1
            with open('errores_minicerebro_superuser.txt', 'a+') as ferror:
                print_exc(file=ferror)
                cadena = ' ' + datetime.now().isoformat() + ' ip: ' +''+ '\n'
                ferror.write(cadena)
            if contador_excepciones == 30:
                break


        sleep(360)
        for j in hilos:
            j.terminate()
        hilos=[]
        for j in listaIntanciasActivas:
            h=multiprocessing.Process(target=detener_superuser, args=(j,),daemon=True)
            h.start()
            hilos.append(h)
        for j in hilos:
            j.terminate()


def obtener_lista_ips():
    db = MongoClient('mongodb://Scraper%2Fops:R3vim3x5o5%2F%2F@13.52.11.40:27017/admin').XLamudi
    lista_ips = [x['Ip'] for x in db['instancias_cloud'].find({'status': 'activa'})]
    return lista_ips


def vigila():  # Esta funcion dentro de un hilo inicia los hilos y los termina
    
    lista_ips = obtener_lista_ips()
    print(lista_ips)
    print(len(lista_ips))
    
    

    for num_instancia, ip_instancia in enumerate(lista_ips): 
        gestor_esta_ejecutandose_en_ip(ip_instancia,1)


  

    

vigila()