
import paramiko
import multiprocessing
import numpy as np
from pymongo import MongoClient
from time import sleep
from traceback import print_exc
from datetime import datetime
from pytz import timezone



def obtener_ssh(ip,n):

    if n==1:

        #Usuario 1 : ubuntu2
        ssh = paramiko.SSHClient()
        # key = paramiko.RSAKey.from_private_key_file('/Users/bernardoriveracamacho/.ssh/')
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, username='ubuntu2', timeout=20)
        return ssh
    elif n==2:

        #Usuario 2 : ubuntu3
        ssh2 = paramiko.SSHClient()
        # key = paramiko.RSAKey.from_private_key_file('/Users/bernardoriveracamacho/.ssh/')
        ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh2.connect(hostname=ip, username='ubuntu3', timeout=20)
        return ssh2

    elif n==3:
        #Usuario 3 : ubuntu4
        ssh3 = paramiko.SSHClient()
        # key = paramiko.RSAKey.from_private_key_file('/Users/bernardoriveracamacho/.ssh/')
        ssh3.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh3.connect(hostname=ip, username='ubuntu4', timeout=20)
        return ssh3
    
    else:
        return None



def ejecutar_gestor_usuarios(ip,n,ssh):
    try:
        if n==1:

            #Usuario 1 : ubuntu2
            stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2; cd superusercloud; python3 GestorUsuarios.py 14 3')

        elif n==2:

        
            #Usuario 2 : ubuntu3
            stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:3; cd superusercloud; python3 GestorUsuarios.py 14 3')

        elif n==3:

            #usuario 3 : ubuntu4
            stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:4; cd superusercloud; python3 GestorUsuarios.py 14 3')
            print("Se ejecuto Gestor {} {} {}".format(n,ip,ssh))
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
                    #print("Ejecutando",ip)
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
                    print("Ejecutando",ip)
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
                    print("Ejecutando",ip)
                    return True
        except:
            print ("Error en conexion ssh usuario",n,"IP: ",ip)
    else:
        pass


def detener_superuser(ip,n,ssh):

    if n==1:

        stdin, stdout, stderr = ssh.exec_command('pkill -9 firefox')
        stdin, stdout, stderr = ssh.exec_command('pkill -9 python3')
        stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2; cd superusercloud; python3 cerrador_ventanas.py')
        stdin, stdout, stderr = ssh.exec_command('pkill -9 firefox')
        stdin, stdout, stderr = ssh.exec_command('pkill -9 python3')

    elif n==2:


        stdin, stdout, stderr = ssh.exec_command('pkill -9 firefox')
        stdin, stdout, stderr = ssh.exec_command('pkill -9 python3')
        stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:3; cd superusercloud; python3 cerrador_ventanas.py')
        stdin, stdout, stderr = ssh.exec_command('pkill -9 firefox')
        stdin, stdout, stderr = ssh.exec_command('pkill -9 python3')
    elif n==3:

        
        stdin, stdout, stderr = ssh.exec_command('pkill -9 firefox')
        stdin, stdout, stderr = ssh.exec_command('pkill -9 python3')
        stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:4; cd superusercloud; python3 cerrador_ventanas.py')
        stdin, stdout, stderr = ssh.exec_command('pkill -9 firefox')
        stdin, stdout, stderr = ssh.exec_command('pkill -9 python3')
        print("deteniendo pythonfirefox {} {}".format(n,ip))
    else:
        pass



def debo_detener_superuser():
    db = MongoClient('mongodb://Scraper%2Fops:R3vim3x5o5%2F%2F@104.199.125.135:27017/admin').XLamudi
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
                detener_superuser(ip_instancia)
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

def obtener_randinstancias(i,maxi):
    a=int(round(np.random.normal(i,int(5*maxi/100))))
    if a>maxi:
        return maxi
    elif a<1:
        return 1
    else:
        return a

# def rendimiento_bajo_pagina():
#     try:
#         ti=time()
#         results=requests.get('https://www.letshome.mx/robots.txt')
#         td=time()-ti
#         print(td,results.status_code)
#         if td>15 and results.status_code!=200:
#             print("Esto se va a descontrola")
#             return True
#         else:
#             print("Todo chido")
#             return False
#     except:
#         print("time Out")

def SUinstancias(activa,usuario,instan,ip,lock):

    try:
        err=False
        ssh = obtener_ssh(ip,2) #usuario+1

        detener_superuser(ip,2,ssh)

        sleep(10)
    except :
        print("Usuario no se inicia -- IP:",ip)
        err=True

    while not err:
        try:
            #print(3,instan,activa[usuario][instan])
            if activa[usuario][instan]:
            
                if gestor_esta_ejecutandose_en_ip(ip,2,ssh):
                    sleep(60)
                else:
                    
                    detener_superuser(ip,2,ssh)

                    sleep(30)
                    ejecutar_gestor_usuarios(ip,2,ssh)
                    sleep(30)
                    

            else:
        
                if gestor_esta_ejecutandose_en_ip(ip,2,ssh):
                 
                    detener_superuser(ip,2,ssh)
                    
                    sleep(60)
                else:
                    sleep(60)
        except:
            print("Se cerro el proceso {} {} -- {}".format(usuario,instan,ip))
            detener_superuser(ip,2,ssh)
            if ssh:
                ssh.close()
            break
    
    if ssh:
        ssh.close()




# def asignacion_intancias(hora,minutos,instancias,lista_ips):

#     print("Ejecutando asignacion_intancias")
#     numeroUsuariosXinstancia=3
#     numero_intancias=len(lista_ips)

#     MaximoUsuarios=numero_intancias*numeroUsuariosXinstancia

#     manager=multiprocessing.Manager()

#     aTF=[[False for i in range(numero_intancias)] for j in range(numeroUsuariosXinstancia)]
#     lstaux=[[False for i in range(numero_intancias)] for j in range(numeroUsuariosXinstancia)]

#     Activa=manager.list(aTF)

#     hilos=[]

#     for j in range(numeroUsuariosXinstancia):
#         for nn,ip in enumerate(lista_ips):
#             ##cada usuario de la instancias tiene su propio hilo
#             h=multiprocessing.Process(name="{}-{}".format(j,nn),target=SUinstancias, args=(Activa,j,nn,ip,))
#             h.start()
#             hilos.append(h)



#     while True:

#         #print(int(hora.value),int(minutos.value/15))

#         if debo_detener_superuser():
#             Activa[:]=[[False for i in range(numero_intancias)] for j in range(numeroUsuariosXinstancia)]
#             sleep(900)
#             break
#         # elif rendimiento_bajo_pagina():
#         #     NumeroInstancias=instancias[int(hora.value)][int(minutos.value/15)]
#         #     print(NumeroInstancias)
#         #     for i in range(MaximoUsuarios):
#         #         if i<NumeroInstancias*2:
#         #             a=True
#         #             lstaux[i//61][i%61] = a

#         #         else:
#         #             a=False
#         #             lstaux[i//61][i%61] = a
                     
#         #     Activa[:]=lstaux
#         #     sleep(60)
#         #     pass
#         else:
#             NumeroInstancias=instancias[int(hora.value)][int(minutos.value/15)]
#             print(NumeroInstancias)
#             for i in range(MaximoUsuarios):
#                 if i<NumeroInstancias*numeroUsuariosXinstancia:
#                     a=True
#                     lstaux[i//numero_intancias][i%numero_intancias] = a

#                 else:
#                     a=False
#                     lstaux[i//numero_intancias][i%numero_intancias] = a
                    
#             Activa[:]=lstaux
#             print(lstaux)
#             sleep(900)

#     for i in hilos:
#         i.join()

def asignacion_intancias(hora,minutos,instancias,lista_ips):

    print("Ejecutando asignacion_intancias2")
    numeroUsuariosXinstancia=1
    numero_intancias=len(lista_ips)

    MaximoUsuarios=numero_intancias*numeroUsuariosXinstancia

    manager=multiprocessing.Manager()
    lock=multiprocessing.Lock()

    aTF=[[False for i in range(numero_intancias)] for j in range(numeroUsuariosXinstancia)]
    lstaux=[[False for i in range(numero_intancias)] for j in range(numeroUsuariosXinstancia)]

    Activa=manager.list(aTF)

    hilos=[]


    for j in range(numeroUsuariosXinstancia):
        for nn,ip in enumerate(lista_ips):
            ##cada usuario de la instancias tiene su propio hilo
            h=multiprocessing.Process(name="{}-{}".format(j,nn),target=SUinstancias, args=(Activa,j,nn,ip,lock,))
            h.start()
            hilos.append(h)



    while True:

        #print(int(hora.value),int(minutos.value/15))

        if debo_detener_superuser():
            Activa[:]=[[False for i in range(numero_intancias)] for j in range(numeroUsuariosXinstancia)]
            sleep(900)
            break
   
        else:
            NumeroInstancias=instancias[int(hora.value)][int(minutos.value/15)] #obtener_randinstancias(instancias[int(hora.value)][int(minutos.value/15)],numero_intancias) ##intancias cada 15 min
            print(NumeroInstancias)
            for i in range(MaximoUsuarios):
                if i<NumeroInstancias*numeroUsuariosXinstancia:
                    a=True
                    lstaux[i//numero_intancias][i%numero_intancias] = a

                else:
                    a=False
                    lstaux[i//numero_intancias][i%numero_intancias] = a
                    
            Activa[:]=lstaux
            print(datetime.now())
            #print(lstaux)
            sleep(900) #15 min

    for i in hilos:
        i.join()




def obtener_lista_ips():
    db = MongoClient('mongodb://Scraper%2Fops:R3vim3x5o5%2F%2F@104.199.125.135:27017/admin').XLamudi
    lista_ips = [x['Ip'] for x in db['instancias_2'].find({'status': 'inactiva'})]
    return lista_ips


def vigila():  # Esta funcion dentro de un hilo inicia los hilos y los termina
    
    lista_ips = obtener_lista_ips()
    print(lista_ips)
    print(len(lista_ips))
    lista_ips2=lista_ips

    print(len(lista_ips2))

    #Datos compartidos por procesos
    hora=multiprocessing.Value('d',0)
    minuto=multiprocessing.Value('d',0)
    num=90
    instancias=[[num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num], [num, num, num, num]]
    #instancias=[[142, 124, 116, 111], [107, 101, 94, 86], [79, 72, 66, 61], [57, 55, 54, 53], [54, 56, 58, 61], [65, 69, 73, 77], [82, 86, 91, 95], [100, 105, 109, 114], [118, 123, 127, 132], [136, 140, 145, 149], [152, 156, 159, 162], [164, 166, 167, 167], [167, 166, 165, 163], [160, 158, 156, 153], [151, 150, 149, 149], [150, 152, 155, 158], [163, 168, 173, 179], [184, 189, 193, 197], [199, 200, 200, 199], [197, 195, 191, 188], [184, 181, 178, 175], [172, 170, 167, 164], [161, 158, 155, 153], [152, 151, 150, 144]]
    #instancias=[[84, 73, 68, 65], [62, 58, 54, 49], [44, 40, 36, 33], [31, 29, 29, 29], [29, 30, 32, 34], [36, 38, 41, 43], [46, 49, 52, 55], [58, 61, 64, 66], [69, 72, 75, 78], [80, 83, 86, 88], [91, 93, 95, 96], [98, 99, 100, 100], [100, 99, 98, 97], [96, 94, 92, 91], [90, 89, 88, 88], [89, 90, 92, 94], [97, 100, 104, 107], [110, 113, 116, 118], [120, 120, 120, 120], [119, 117, 115, 113], [110, 108, 106, 105], [103, 101, 100, 98], [96, 94, 92, 91], [90, 90, 89, 85]]
    #instancias=[[41, 35, 33, 31], [30, 28, 26, 24], [21, 19, 17, 16], [14, 14, 13, 13], [14, 14, 15, 16], [17, 18, 19, 21], [22, 23, 25, 26], [28, 29, 31, 32], [34, 35, 36, 38], [39, 41, 42, 43], [44, 45, 46, 47], [48, 48, 49, 49], [49, 49, 48, 48], [47, 46, 45, 44], [44, 43, 43, 43], [43, 44, 45, 46], [48, 50, 52, 54], [56, 57, 59, 60], [60, 60, 60, 60], [60, 59, 58, 56], [55, 54, 52, 51], [51, 50, 49, 48], [47, 46, 45, 44], [44, 44, 43, 42]]
    #instancias=[[7, 6, 5, 5], [5, 5, 4, 4], [3, 3, 3, 2], [2, 2, 2, 2], [2, 2, 2, 2], [2, 3, 3, 3], [3, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6], [7, 7, 7, 7], [8, 8, 8, 8], [8, 8, 8, 8], [8, 8, 8, 8], [8, 8, 8, 8], [7, 7, 7, 7], [7, 7, 8, 8], [8, 9, 9, 9], [10, 10, 10, 10], [11, 11, 11, 11], [10, 10, 10, 10], [9, 9, 9, 9], [9, 9, 8, 8], [8, 8, 8, 8], [7, 7, 7, 7]]
    #instancias=[[22, 19, 17, 16],[16, 15, 13, 12],[11, 10, 9, 8],[7, 7, 7, 7],[7, 7, 7, 8],[8, 9, 10, 11],[11, 12, 13, 14],[15, 15, 16, 17],[18, 18, 19, 20],[21, 21, 22, 23],[24, 24, 25, 25],[26, 26, 26, 26],[26, 26, 26, 25],[25, 24, 24, 24],[23, 23, 23, 23],[23, 23, 24, 25],[26, 27, 28, 29],[30, 31, 32, 32],[33, 33, 33, 33],[32, 32, 31, 30],[29, 29, 28, 27],[27, 27, 26, 26],[25, 25, 24, 24],[23, 23, 23, 22]]
    #instancias = [[7, 6, 5, 5],[5, 5, 4, 4],[3, 3, 3, 2],[2, 2, 2, 2],[2, 2, 2, 2],[2, 3, 3, 3],[3, 4, 4, 4],[5, 5, 5, 5],[6, 6, 6, 6],[7, 7, 7, 7],[8, 8, 8, 8],[8, 8, 8, 8],[8, 8, 8, 8],[8, 8, 8, 8],[7, 7, 7, 7],[7, 7, 8, 8],[8, 9, 9, 9],[10, 10, 10, 10],[11, 11, 11, 11],[10, 10, 10, 10],[9, 9, 9, 9],[9, 9, 8, 8],[8, 8, 8, 8],[7, 7, 7, 7]]
    Asigancion = multiprocessing.Process(target=asignacion_intancias,daemon=False,args=(hora,minuto,instancias,lista_ips2,))
    Dia = multiprocessing.Process(target=hora_dia,daemon=True,args=(hora,minuto))
    Dia.start()
    sleep(1)#evitar el cero en hora y en minuto 
    Asigancion.start()





    Dia.join()
    Asigancion.join()

    


vigila()