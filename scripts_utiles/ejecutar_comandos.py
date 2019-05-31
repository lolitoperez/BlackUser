# Se debe de correr enter.py previamente

import paramiko

from datetime import datetime
import multiprocessing
from pprint import pprint
import random
from pathlib import Path
import time
from pymongo import *

db = MongoClient('mongodb://Scraper%2Fops:R3vim3x5o5%2F%2F@13.52.11.40:27017/admin').XLamudi
collection = db['superuser_cloud_listas']

home = str(Path.home())
presto = False
respuestaA = 0
NUM_HILOS = 11  # 145 para archivos,40 para comandos, ejecutar solo un hilo cuado se quiera ver ips erradas
hilos = []

IPS = [x['Ip'] for x in db['instancias_cloud'].find({'status': 'activa'})]

# random.shuffle(IPS)
# IPS=IPS[:100]

# IPS=['54.164.123.133'] #poner aqui los faltantes :P

# indice1 = len(IPS) // NUM_HILOS  #
# indice2 = (len(IPS) % NUM_HILOS)  #
# sublistaip = []
# for i in range(NUM_HILOS):
#     sublistaip.append(IPS[indice1 * i:indice1 * (i + 1)])

# for i in range(int(indice2)):
#     sublistaip[i].append(IPS[indice1 * (NUM_HILOS) + i])

# print(sublistaip, len(sublistaip), len(IPS))


def funcionA(entrada):
    IPS = entrada
    # print(len(IPS[0]))
    contador = 1
    for ip in IPS:
        # os.system('scp /Users/mq45/Downloads/icasas1.py ubuntu2@'+ip+':/home/ubuntu2/icasas/')
        #os.system('scp /Users/mq45/Downloads/rentasyventas1.py ubuntu2@' + ip + ':/home/ubuntu2/rentasyventas/')
        # os.system('scp /Users/mq45/Downloads/rentasyventas2.py ubuntu2@'+ip+':/home/ubuntu2/rentasyventas/')
        # os.system('scp /Users/mq45/Downloads/rentasyventas3.py ubuntu2@'+ip+':/home/ubuntu2/rentasyventas/')
        # os.system('scp /Users/mq45/Downloads/easyaviso1.py ubuntu2@'+ip+':/home/ubuntu2/easyaviso/')
        # os.system('scp /Users/mq45/Downloads/easyaviso2.py ubuntu2@'+ip+':/home/ubuntu2/easyaviso/')
        # os.system('scp /Users/mq45/Downloads/easyaviso3.py ubuntu2@'+ip+':/home/ubuntu2/easyaviso/')
        # os.system('scp /Users/mq45/Downloads/human5.py ubuntu2@'+ip+':/home/ubuntu2/human/')
        # os.system('scp /Users/mq45/Downloads/rediak2.py ubuntu2@'+ip+':/home/ubuntu2/rediak/')
        # os.system('scp /Users/mq45/Downloads/rediak3.py ubuntu2@'+ip+':/home/ubuntu2/rediak/')
        # os.system('scp /Users/mq45/Downloads/m3_1.py ubuntu2@'+ip+':/home/ubuntu2/metroscubicos/')
        # os.system('scp /Users/mq45/Downloads/m3_3.py ubuntu2@'+ip+':/home/ubuntu2/metroscubicos/')
        # os.system('scp /Users/mq45/Downloads/rediak2.py ubuntu2@'+ip+':/home/ubuntu2/rediak/')
        # os.system('scp /Users/mq45/Downloads/silovendes3.py ubuntu2@'+ip+':/home/ubuntu2/silovendes/')
        # os.system('scp /Users/mq45/Downloads/scrips\ finales/properati/properati3.py ubuntu2@'+ip+':/home/ubuntu2/properati/')
        # os.system('scp /Users/mq45/Downloads/anuncio2.py ubuntu2@'+ip+':/home/ubuntu2/anuncioshoy/')
        # os.system('scp /Users/mq45/Downloads/geocoder1.py ubuntu2@'+ip+':/home/ubuntu2/geocoder/')
        # os.system('scp /Users/mq45/Downloads/geocoder1.py ubuntu2@'+ip+':/home/ubuntu2/inmuebles24/')
        # os.system('scp /Users/mq45/Downloads/silovendes3.py ubuntu2@'+ip+':/home/ubuntu2/silovendes/')
        # os.system('scp /Users/mq45/Downloads/captcha.png ubuntu2@'+ip+':/home/ubuntu2/lamudi/')
        # os.system('scp /Users/mq45/Downloads/lamu3.py ubuntu2@'+ip+':/home/ubuntu2/lamudi/')
        # os.system('scp /Users/mq45/Downloads/lamu3x.py ubuntu2@'+ip+':/home/ubuntu2/lamudi/')
        # os.system('scp /Users/mq45/Downloads/propiedades_3.py ubuntu2@'+ip+':/home/ubuntu2/propiedades/')
        # os.system('scp /Users/mq45/Downloads/pardon.png ubuntu2@'+ip+':/home/ubuntu2/lamudi/')
        # os.system('scp /Users/mq45/Downloads/lamu3.py ubuntu2@'+ip+':/home/ubuntu2/lamudi/')
        # os.system('scp -r /Users/mq45/Downloads/human ubuntu2@'+ip+':/home/ubuntu2/')
        # time.sleep(1)
        # print(threading.current_thread(), contador,'ip--->',ip)
        print(multiprocessing.current_process(), contador, 'ip--->', ip)
        contador += 1
    # print(threading.current_thread())


Check = {}
ipserradas = []


def comandos(IPS):
    global Check, ipserradas
    contador = 1
    for ip in IPS:
        # print(len(IPS[0]))
        ssh = None
        try:
            ssh = paramiko.SSHClient()
            #key = paramiko.RSAKey.from_private_key_file('/Users/bernardoriveracamacho/.ssh/')
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=ip, username='ubuntu2', timeout=10)

            ssh2 = paramiko.SSHClient()
            #key = paramiko.RSAKey.from_private_key_file('/Users/bernardoriveracamacho/.ssh/')
            ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh2.connect(hostname=ip, username='ubuntu3', timeout=10)

            ssh3 = paramiko.SSHClient()
            ssh3.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh3.connect(hostname=ip, username='ubuntu4', timeout=10)
            
            #stdin, stdout, stderr = ssh.exec_command('crontab /home/ubuntu2/Reinicio.cron')
            #stdin, stdout, stderr = ssh.exec_command('vncserver :2')
            #stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2; cd superusercloud; python3 GestorUsuarios.py 1 3')
            stdin, stdout, stderr = ssh.exec_command('cd superusercloud; git pull')
            stdin2, stdout2, stderr2 = ssh2.exec_command('cd superusercloud; git pull')
            stdin3, stdout3, stderr3 = ssh3.exec_command('cd superusercloud; git pull')

            #stdin, stdout, stderr = ssh.exec_command('ls')
            #stdin, stdout, stderr = ssh.exec_command('cd .ssh; printf "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDSoeeOvZAPWhxHqVfoPB9Eaa7ypjrsirgR4Z0lwjvXkDYaQ7JPKkoP1S1U5uIdCheh6nUIENs6tMojuiS8v2533S/4ymd+XX/K4zbFfenYxJZNAAzO7C0fdaUQHjxWn2S6xN+blL63TXdROYdoSCnSlVjTq7zBlf/XriVu9UI9/NCUrY4wI4Ciu5OT2cI6k91scV1+KaS+p/mSQdw8R0c6Rud0GG/3FUCLJ/qw/pkC3m2NtlfvcVLXVEuoRRlv412J5N8OxWOSCNBtok0AA9owAbzZwC8xYJMZT7csze9mZxfHYoZLK0qa48kAZ4IDIme/V8UvxV90f7QfSSaVOxXH ubuntu2@vm-global-cerebrito\n">>authorized_keys')
            # stdin, stdout, stderr = ssh.exec_command('cd century21 ; export DISPLAY=:2 ; Century21_3.py')
            # stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2 ; cd metroscubicos ; python3 m3_2.py')
            # stdin, stdout, stderr = ssh.exec_command("cd /home/ubuntu2/XAAJ/MRRCv/easyaviso; export DISPLAY=:2 ; python3 easyaviso")
            # stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2 ; cd anuncioshoy ; python3 anuncio3.py')
            #stdin, stdout, stderr = ssh.exec_command(
            #    'cd /home/ubuntu2/XAAJ/MRRCv/superuser; export DISPLAY=:2 ;python3 GestorUsuarios.py 60 6')
            # stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2 ; cd lamudi ; python3 lamu3x.py')
            # stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2; cd propiedades ;python3 propiedades_3.py')
            # stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2; cd easyaviso ;python3 easyaviso3.py')
            # stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2; cd inmuebles24 ;python3 geocoder1.py')
            # stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2 ; cd rediak ; python3 rediak3.py')
            # stdin, stdout, stderr = ssh.exec_command('cd lamudi ; export DISPLAY=:2 ; python3 lamu3.py')
            # stdin, stdout, stderr = ssh.exec_command('cd metroscubicos ; export DISPLAY=:2 ; python3 m3_3.py')
            # stdin, stdout, stderr = ssh.exec_command('cd human ; export DISPLAY=:2 ; python3 human5.py 360 20')
            # stdin, stdout, stderr = ssh.exec_command('cd geocoder ; export DISPLAY=:2 ; python3 geocoder1.py')
            
            # stdin, stdout, stderr = ssh.exec_command('firefox https://es.wikipedia.org/wiki/Wikipedia:Portada')
            # stdin2, stdout2, stderr2 = ssh2.exec_command('firefox https://es.wikipedia.org/wiki/Wikipedia:Portada')

            #sleep(10)

            # stdin, stdout, stderr = ssh.exec_command('pkill firefox ; pkill python3')
            # stdin2, stdout2, stderr2 = ssh2.exec_command('pkill firefox ; pkill python3')

            #stdin2, stdout2, stderr2 = ssh2.exec_command('pkill -9 firefox')
            # stdin, stdout, stderr = ssh.exec_command('ls')
            # stdin, stdout, stderr = ssh.exec_command(""" cd .ssh ; printf "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDYjjBsWsZ+N2CORNTUct4tWhD6S7Xh3LjUfcdIUgXDA+u+GV23GDm5zGlO/G9Prcn9irKKPANtfmnar/U1VutVJ0tu/NzTa1Rh7h0LZh3GOhmyi0J5d8OnpXf/5n+tJNpxanBLsJTVEaB0lDNSHiOs9ENzLUAwN0XpUVMCSHOGhPIMVLi77mtDa6QWggHcyP32YIAj0dNEgycUrxOv6EhvlM39c1CzO4tqoKsRfT6zEcMxaI47f3h2VQq/+2Le8vk0Ypcx9UdrjhDg5QESe0i75aHE3EUe7njIpY12Rg5Zz6mD7IWcd8Muz86Dse1LW52v3Y2UP2bLuYcBrrDW9fNZ mq12@iMac-5.local\n">>authorized_keys""")
            # stdin, stdout, stderr = ssh.exec_command("echo 'revimex5'|sudo -S reboot")
            # stdin, stdout, stderr = ssh.exec_command(" export DISPLAY=:2")
            # stdin, stdout, stderr = ssh.exec_command('cd icasas ; export DISPLAY=:2 ; python3 icasas3.py')
            # stdin, stdout, stderr = ssh.exec_command('cd anuncioshoy ; pill python3 anuncio2.py')
            # stdin, stdout, stderr = ssh.exec_command("vncserver :2 ; cd geocoder ; export DISPLAY=:2 ; python3 geocoder1.py")
            Check[ip]=list(map(lambda x: x.replace('\n',''),list(stdout)))
            print(ip, Check[ip])

            Check[ip]=list(map(lambda x: x.replace('\n',''),list(stdout2)))
            print(ip, Check[ip])

            Check[ip]=list(map(lambda x: x.replace('\n',''),list(stdout3)))
            print(ip, Check[ip])
            
            # print(multiprocessing.current_process(),contador,'ip--->',ip,Check[ip])
            print(multiprocessing.current_process(), contador, 'ip--->', ip)
            contador += 1
        except Exception as e:
            print(e)
            print('error: ', multiprocessing.current_process(), contador, 'ip--->', ip)
            ipserradas.append(ip)
        finally:
            if ssh:
                ssh.close()
            if ssh2:
                ssh2.close()
            if ssh2:
                ssh3.close()

def comandosChido(ip):

    # print(len(IPS[0]))
    ssh = None
    try:
        ssh = paramiko.SSHClient()
        #key = paramiko.RSAKey.from_private_key_file('/Users/bernardoriveracamacho/.ssh/')
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, username='ubuntu2', timeout=10)

        ssh2 = paramiko.SSHClient()
        #key = paramiko.RSAKey.from_private_key_file('/Users/bernardoriveracamacho/.ssh/')
        ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh2.connect(hostname=ip, username='ubuntu3', timeout=10)

        ssh3 = paramiko.SSHClient()
        ssh3.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh3.connect(hostname=ip, username='ubuntu4', timeout=10)
        
        #stdin, stdout, stderr = ssh.exec_command('crontab /home/ubuntu2/Reinicio.cron')
        #stdin, stdout, stderr = ssh.exec_command('vncserver :2')
        #stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2; cd superusercloud; python3 GestorUsuarios.py 1 3')
        stdin, stdout, stderr = ssh.exec_command('cd superusercloud; git pull')
        stdin2, stdout2, stderr2 = ssh2.exec_command('cd superusercloud; git pull')
        stdin3, stdout3, stderr3 = ssh3.exec_command('cd superusercloud; git pull')

        #stdin, stdout, stderr = ssh.exec_command('ls')
        #stdin, stdout, stderr = ssh.exec_command('cd .ssh; printf "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDSoeeOvZAPWhxHqVfoPB9Eaa7ypjrsirgR4Z0lwjvXkDYaQ7JPKkoP1S1U5uIdCheh6nUIENs6tMojuiS8v2533S/4ymd+XX/K4zbFfenYxJZNAAzO7C0fdaUQHjxWn2S6xN+blL63TXdROYdoSCnSlVjTq7zBlf/XriVu9UI9/NCUrY4wI4Ciu5OT2cI6k91scV1+KaS+p/mSQdw8R0c6Rud0GG/3FUCLJ/qw/pkC3m2NtlfvcVLXVEuoRRlv412J5N8OxWOSCNBtok0AA9owAbzZwC8xYJMZT7csze9mZxfHYoZLK0qa48kAZ4IDIme/V8UvxV90f7QfSSaVOxXH ubuntu2@vm-global-cerebrito\n">>authorized_keys')
        # stdin, stdout, stderr = ssh.exec_command('cd century21 ; export DISPLAY=:2 ; Century21_3.py')
        # stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2 ; cd metroscubicos ; python3 m3_2.py')
        # stdin, stdout, stderr = ssh.exec_command("cd /home/ubuntu2/XAAJ/MRRCv/easyaviso; export DISPLAY=:2 ; python3 easyaviso")
        # stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2 ; cd anuncioshoy ; python3 anuncio3.py')
        #stdin, stdout, stderr = ssh.exec_command(
        #    'cd /home/ubuntu2/XAAJ/MRRCv/superuser; export DISPLAY=:2 ;python3 GestorUsuarios.py 60 6')
        # stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2 ; cd lamudi ; python3 lamu3x.py')
        # stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2; cd propiedades ;python3 propiedades_3.py')
        # stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2; cd easyaviso ;python3 easyaviso3.py')
        # stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2; cd inmuebles24 ;python3 geocoder1.py')
        # stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2 ; cd rediak ; python3 rediak3.py')
        # stdin, stdout, stderr = ssh.exec_command('cd lamudi ; export DISPLAY=:2 ; python3 lamu3.py')
        # stdin, stdout, stderr = ssh.exec_command('cd metroscubicos ; export DISPLAY=:2 ; python3 m3_3.py')
        # stdin, stdout, stderr = ssh.exec_command('cd human ; export DISPLAY=:2 ; python3 human5.py 360 20')
        # stdin, stdout, stderr = ssh.exec_command('cd geocoder ; export DISPLAY=:2 ; python3 geocoder1.py')
        
        # stdin, stdout, stderr = ssh.exec_command('firefox https://es.wikipedia.org/wiki/Wikipedia:Portada')
        # stdin2, stdout2, stderr2 = ssh2.exec_command('firefox https://es.wikipedia.org/wiki/Wikipedia:Portada')

        #sleep(10)

        # stdin, stdout, stderr = ssh.exec_command('pkill firefox ; pkill python3')
        # stdin2, stdout2, stderr2 = ssh2.exec_command('pkill firefox ; pkill python3')

        #stdin2, stdout2, stderr2 = ssh2.exec_command('pkill -9 firefox')
        # stdin, stdout, stderr = ssh.exec_command('ls')
        # stdin, stdout, stderr = ssh.exec_command(""" cd .ssh ; printf "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDYjjBsWsZ+N2CORNTUct4tWhD6S7Xh3LjUfcdIUgXDA+u+GV23GDm5zGlO/G9Prcn9irKKPANtfmnar/U1VutVJ0tu/NzTa1Rh7h0LZh3GOhmyi0J5d8OnpXf/5n+tJNpxanBLsJTVEaB0lDNSHiOs9ENzLUAwN0XpUVMCSHOGhPIMVLi77mtDa6QWggHcyP32YIAj0dNEgycUrxOv6EhvlM39c1CzO4tqoKsRfT6zEcMxaI47f3h2VQq/+2Le8vk0Ypcx9UdrjhDg5QESe0i75aHE3EUe7njIpY12Rg5Zz6mD7IWcd8Muz86Dse1LW52v3Y2UP2bLuYcBrrDW9fNZ mq12@iMac-5.local\n">>authorized_keys""")
        # stdin, stdout, stderr = ssh.exec_command("echo 'revimex5'|sudo -S reboot")
        # stdin, stdout, stderr = ssh.exec_command(" export DISPLAY=:2")
        # stdin, stdout, stderr = ssh.exec_command('cd icasas ; export DISPLAY=:2 ; python3 icasas3.py')
        # stdin, stdout, stderr = ssh.exec_command('cd anuncioshoy ; pill python3 anuncio2.py')
        # stdin, stdout, stderr = ssh.exec_command("vncserver :2 ; cd geocoder ; export DISPLAY=:2 ; python3 geocoder1.py")
        Check[ip]=list(map(lambda x: x.replace('\n',''),list(stdout)))
        print(ip, Check[ip])

        Check[ip]=list(map(lambda x: x.replace('\n',''),list(stdout2)))
        print(ip, Check[ip])

        Check[ip]=list(map(lambda x: x.replace('\n',''),list(stdout3)))
        print(ip, Check[ip])
        
        # print(multiprocessing.current_process(),contador,'ip--->',ip,Check[ip])
        print(multiprocessing.current_process(), 'ip--->', ip)

    except Exception as e:
        print(e)
        print('error: ', multiprocessing.current_process(), 'ip--->', ip)
        ipserradas.append(ip)
    finally:
        if ssh:
            ssh.close()
        if ssh2:
            ssh2.close()
        if ssh3:
            ssh3.close()

    # if contador%250 ==0:
    # 	print('[X]------------------',contador)
    # 	time.sleep(3600)   #Despues de mandar un comando espera a que se pueda ver reflejado en la BD antes de consultarlo

    # while  True:

    # 	trabajando=collection.find({'status22':'working'}).count()
    # 	#pendientes=collection.find({'status22':'pendiente'}).count()
    # 	#finalizados=collection.find({'status22':'finalizado'}).count()
    # 	#errores=collection.find({'status22':'error'}).count()
    # 	print(trabajando)
    # 	if trabajando<30:
    # 		break
    # 	else:
    # 		time.sleep(10)


# print('errores en:',ipserradas)


def vigila():  # Esta funcion dentro de un hilo inicia los hilos y los termina

    hilos = []

    for num_hilo,ip in enumerate(IPS):  # del 0 al NUM_HILOS-1
        hilos.append(multiprocessing.Process(name=str(num_hilo), target=comandosChido, args=(ip,),
                                             daemon=False))  # Nosete que el NOMBRE del hilo corresponde a su número

    for k in range(NUM_HILOS):
        hilos[k].start()

    for k in range(NUM_HILOS):
        hilos[k].join()


    # while presto==False:
    # print('hilos activos='+str(len(threading.enumerate()) ) )
    # time.sleep(1)



# print('enumerados:'+str(threading.enumerate()))
for i in range(1):
    ahora = datetime.now()
    vigila()
    #print(len(Check.keys()))
    #pprint(Check)
    despues = datetime.now()
    #print(despues - ahora)
    print(IPS)
    #time.sleep(3800)