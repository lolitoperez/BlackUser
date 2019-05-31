
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


def obtener_ssh(ip):

    #Usuario 1 : ubuntu2
    ssh = paramiko.SSHClient()
    # key = paramiko.RSAKey.from_private_key_file('/Users/bernardoriveracamacho/.ssh/')
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip, username='ubuntu2', timeout=10)

    #Usuario 2 : ubuntu3
    ssh2 = paramiko.SSHClient()
    # key = paramiko.RSAKey.from_private_key_file('/Users/bernardoriveracamacho/.ssh/')
    ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh2.connect(hostname=ip, username='ubuntu3', timeout=10)

    
    return ssh,ssh2 


def ejecutar_gestor_usuarios(ip):
    try:
        ssh,ssh2= obtener_ssh(ip)
        
        #Usuario 1 : ubuntu2
        stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2; cd superusercloud; python3 GestorUsuarios.py 5 30')
        #Usuario 2 : ubuntu3
        stdin2, stdout2, stderr2 = ssh2.exec_command('export DISPLAY=:3; cd superusercloud; python3 GestorUsuarios.py 5 30')

        #ssh2.close()
        #ssh.close()
        return True
    except:
        return False


def gestor_esta_ejecutandose_en_ip(ip):

    try:
        ssh,ssh2= obtener_ssh(ip)
        #Usuario 1 : ubuntu2
        stdin, stdout, stderr = ssh.exec_command('pgrep -af "python3 GestorUsuarios.py"')
        #Usuario 2 : ubuntu3
        stdin2, stdout2, stderr2 = ssh2.exec_command('pgrep -af "python3 GestorUsuarios.py"')
        #ssh.close()
    except:
        return False

    salida = list(stdout)
    salida2 = list(stdout2)

    if len(salida) == 0 and len(salida2)==0:
        return False
    else:
        # print(salida)
        primer_salida = salida[0]
        primer_salida2 = salida2[0]
        if primer_salida.find('python3 GestorUsuarios.py') == -1 and primer_salida2.find('python3 GestorUsuarios.py') ==-1:
            return False
        else:
            return True


def detener_superuser(ip):

    ssh,ssh2 = obtener_ssh(ip)

    stdin, stdout, stderr = ssh.exec_command('pkill -9 python3')
    stdin, stdout, stderr = ssh.exec_command('pkill -9 firefox')
    stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2; cd superusercloud; python3 cerrador_ventanas.py')

    stdin2, stdout2, stderr2 = ssh2.exec_command('pkill -9 python3')
    stdin2, stdout2, stderr2 = ssh2.exec_command('pkill -9 firefox')
    stdin2, stdout2, stderr2 = ssh2.exec_command('export DISPLAY=:3; cd superusercloud; python3 cerrador_ventanas.py')
    #ssh.close()
    print("Deteniendo", ip)


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


def activacion_desactivacion_intancias(ip_instancia):
	pass

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
                cnt=0
                while cnt<NumeroInstancias:
                    instanciasrand=lista_ips[random.randrange(0,len(lista_ips))]
                    if instanciasrand not in listaIntanciasActivas:
                        listaIntanciasActivas.append(instanciasrand)
                        cnt=cnt+1
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
    
    # Usuarios=[1455.0, 1252.0, 1157.0, 1102.0, 1051.0, 988.0, 912.0, 827.0, 739.0, 656.0, 584.0, 525.0, 483.0, 457.0, 446.0, 448.0, 462.0, 484.0, 513.0, 547.0, 584.0, 624.0, 667.0, 712.0, 760.0, 810.0, 862.0, 916.0, 972.0, 1030.0, 1087.0, 1144.0, 1198.0, 1249.0, 1296.0, 1337.0, 1372.0, 1400.0, 1421.0, 1436.0, 1444.0, 1448.0, 1449.0, 1447.0, 1445.0, 1445.0, 1447.0, 1453.0, 1464.0, 1481.0, 1503.0, 1530.0, 1561.0, 1594.0, 1627.0, 1659.0, 1686.0, 1707.0, 1720.0, 1721.0, 1712.0, 1690.0, 1656.0, 1612.0, 1558.0, 1498.0, 1436.0, 1374.0, 1318.0, 1271.0, 1238.0, 1223.0, 1227.0, 1253.0, 1301.0, 1370.0, 1456.0, 1556.0, 1664.0, 1774.0, 1879.0, 1971.0, 2045.0, 2096.0, 2121.0, 2119.0, 2093.0, 2045.0, 1984.0, 1917.0, 1851.0, 1791.0, 1740.0, 1692.0, 1635.0, 1545.0]
    
    # #Codigo para separar los 96 elementos para que resulte una lista de 24 listas (horas) con cada lista de 4 elementos (15min)
  
    # Instancias=[round(((i/40)+(i/40)*0.15)/6) for i in Usuarios] #se le agrega el 19.6% del errr de las proxies lentas y las intancias
    # print(Instancias)
    # Elementos=4
    # listaR=[Instancias[i:i+Elementos] for i in range(0,len(Instancias),Elementos)]
    # print(listaR)
    
   
    	#Listas de instancias por Hora cada 15 minutos
    #Instancias=[[6, 8, 6, 7], [5, 5, 3, 4], [4, 6, 2, 1], [4, 2, 3, 2], [4, 4, 4, 3], [2, 4, 3, 3], [5, 3, 4, 4], [6, 3, 6, 5], [5, 8, 8, 7], [8, 8, 9, 6], [5, 8, 8, 6], [6, 6, 8, 11], [8, 9, 7, 8], [8, 9, 8, 9], [8, 11, 9, 10], [8, 6, 8, 9], [8, 6, 9, 9], [7, 7, 7, 7], [8, 8, 5, 8], [9, 9, 10, 11], [7, 10, 10, 9], [10, 10, 12, 11], [10, 9, 10, 8], [6, 7, 7, 8]]
    Instancias = [[7, 6, 5, 5],[5, 5, 4, 4],[3, 3, 3, 2],[2, 2, 2, 2],[2, 2, 2, 2],[2, 3, 3, 3],[3, 4, 4, 4],[5, 5, 5, 5],[6, 6, 6, 6],[7, 7, 7, 7],[8, 8, 8, 8],[8, 8, 8, 8],[8, 8, 8, 8],[8, 8, 8, 8],[7, 7, 7, 7],[7, 7, 8, 8],[8, 9, 9, 9],[10, 10, 10, 10],[11, 11, 11, 11],[10, 10, 10, 10],[9, 9, 9, 9],[9, 9, 8, 8],[8, 8, 8, 8],[7, 7, 7, 7]]

    #print(Instancias)


    #Datos compartidos por procesos
    hora=multiprocessing.Value('d',0)
    minuto=multiprocessing.Value('d',0)

    Asigancion = multiprocessing.Process(target=asignacion_intancias,daemon=False,args=(hora,minuto,Instancias,lista_ips))
    Dia = multiprocessing.Process(target=hora_dia,daemon=True,args=(hora,minuto))
    Dia.start()
    sleep(1)#evitar el cero en hora y en minuto 
    Asigancion.start()

		    # hilos = []
		    # total_instancias = len(lista_ips)

		    # for num_instancia, ip_instancia in enumerate(lista_ips):  # del 0 al NUM_HILOS-1

		    #     hilos.append(multiprocessing.Process(name=str(num_instancia), target=vigilar_instancia, args=(ip_instancia, num_instancia,),
		    #                                          daemon=False))  # Notese que el NOMBRE del hilo corresponde a su número

		    # for k in range(total_instancias):
		    #     hilos[k].start()

		    # for k in range(total_instancias):
		    #     hilos[k].join()


    Dia.join()
    Asigancion.join()

    


vigila()