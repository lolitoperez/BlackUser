import paramiko
import multiprocessing
from pymongo import MongoClient
from time import sleep
from traceback import print_exc
from datetime import datetime
from random import randint


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
        stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2; cd superusercloud; python3 GestorUsuarios.py 60 3')
        #Usuario 2 : ubuntu3
        stdin2, stdout2, stderr2 = ssh2.exec_command('export DISPLAY=:3; cd superusercloud; python3 GestorUsuarios.py 60 3')

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


def obtener_lista_ips():
    db = MongoClient('mongodb://Scraper%2Fops:R3vim3x5o5%2F%2F@13.52.11.40:27017/admin').XLamudi
    lista_ips = [x['Ip'] for x in db['instancias_cloud'].find({'status': 'activa'})]
    return lista_ips


def vigila():  # Esta funcion dentro de un hilo inicia los hilos y los termina
    
    lista_ips = obtener_lista_ips()

    print(lista_ips)
    print(len(lista_ips))
    hilos = []
    total_instancias = len(lista_ips)
    #lista_ips2= [lista_ips[i] for i in range(int(total_instancias/2))]

    for num_instancia, ip_instancia in enumerate(lista_ips):  # del 0 al NUM_HILOS-1

        hilos.append(multiprocessing.Process(name=str(num_instancia), target=vigilar_instancia, args=(ip_instancia, num_instancia,),
                                             daemon=False))  # Notese que el NOMBRE del hilo corresponde a su número

    for k in range(int(total_instancias)):
        hilos[k].start()

    for k in range(int(total_instancias)):
        hilos[k].join()


vigila()
