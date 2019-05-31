import paramiko
import base64
ips = [
        '35.230.56.152',
        '35.247.18.240',
        '35.247.27.187',
        '35.185.196.197',
        '35.247.12.31',
        '35.230.22.164',
        '35.247.73.212',
        '35.230.54.93',
        '35.197.22.68',
        '35.233.203.147',
        '35.197.14.148',
        '35.247.34.157',
        '35.230.43.26',
        #'35.247.68.201',
        '35.185.197.106',
        '35.197.109.6',
        '35.197.32.91',
        '35.197.95.212',
        '35.185.231.182',
        '35.247.12.66',
        '35.197.64.121',
        '35.227.153.14',
        '35.230.76.23',
        '35.247.18.250',
        '35.230.62.177',
        '35.247.36.135',
        #'35.199.154.92',
        '104.196.250.210',
        #'35.247.9.126',
        #'35.233.164.149',
        "35.230.28.219",
        "35.247.108.226",
        "35.233.241.171",
        "35.230.29.111",
        "35.247.53.212",
        "35.230.29.91",
        "35.233.245.109",
        "35.247.101.200",
        "35.247.85.187",
        "35.247.86.189",
        "35.197.96.85",
        "35.203.184.227",
        "35.227.181.66",
        "35.203.189.197",
        "35.233.166.22",
        "35.185.204.152",
        "35.233.232.179",
        "35.230.83.128",
        "35.233.215.48",
        "35.203.149.6",
        "35.247.26.66",
        "35.197.51.212",
        "104.198.3.10",
        "35.233.244.224",
        "35.197.25.249",
        "35.199.152.27",
        "35.197.86.183",
        "35.203.147.33",
        "35.230.65.211",
        "104.198.103.17",
        "104.199.125.135",
        "35.199.179.48",
        "35.185.211.22",
        "35.203.143.60",
    ]
#ip de la instancia padre
#ips = [
#    '35.235.92.97'
#]





def probar_instancias_gestor():
    total_errores = 0
    for ip in ips:
        ssh = paramiko.SSHClient()
        #key = paramiko.RSAKey(data=base64.b64decode(b"""AAAAB3Nza..."""), password='my key password')
        #key = paramiko.RSAKey.from_private_key_file('/Users/bernardoriveracamacho/.ssh/')
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, username='ubuntu2', timeout=10)
        stdin, stdout, stderr = ssh.exec_command('pgrep -af "python3 GestorUsuarios.py"')
        #stdin, stdout, stderr = ssh.exec_command(
        #    'cd .ssh; printf "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDSoeeOvZAPWhxHqVfoPB9Eaa7ypjrsirgR4Z0lwjvXkDYaQ7JPKkoP1S1U5uIdCheh6nUIENs6tMojuiS8v2533S/4ymd+XX/K4zbFfenYxJZNAAzO7C0fdaUQHjxWn2S6xN+blL63TXdROYdoSCnSlVjTq7zBlf/XriVu9UI9/NCUrY4wI4Ciu5OT2cI6k91scV1+KaS+p/mSQdw8R0c6Rud0GG/3FUCLJ/qw/pkC3m2NtlfvcVLXVEuoRRlv412J5N8OxWOSCNBtok0AA9owAbzZwC8xYJMZT7csze9mZxfHYoZLK0qa48kAZ4IDIme/V8UvxV90f7QfSSaVOxXH ubuntu2@vm-global-cerebrito\n">>authorized_keys')
        #stdin, stdout, stderr = ssh.exec_command('pkill -9 firefox')
        #stdin, stdout, stderr = ssh.exec_command('ls')

        salida = list(stdout)
        if len(salida) == 0:
            total_errores += 1
            print('error en la peticion de la ip: ', ip)
        else:
            #print(salida)
            primer_salida = salida[0]

            if primer_salida.find('python3 GestorUsuarios.py') == -1:
                total_errores += 1
                print('error en la peticion de la ip: ', ip)
    print(total_errores)


def detener_superuser():

    for ip in ips:
        ssh = paramiko.SSHClient()
        # key = paramiko.RSAKey(data=base64.b64decode(b"""AAAAB3Nza..."""), password='my key password')
        # key = paramiko.RSAKey.from_private_key_file('/Users/bernardoriveracamacho/.ssh/')
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, username='ubuntu2', timeout=10)
        stdin, stdout, stderr = ssh.exec_command('pkill -9 python3')
        stdin, stdout, stderr = ssh.exec_command('pkill -9 firefox')
        stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2; cd superusercloud; python3 cerrador_ventanas.py')
        #stdin, stdout, stderr = ssh.exec_command('ls')




from pymongo import MongoClient


def enviar_comando():
    db = MongoClient('mongodb://Scraper%2Fops:R3vim3x5o5%2F%2F@13.52.11.40:27017/admin').XLamudi
    collection = db['instancias_cloud']

    for ip in ips:
        nombre = collection.find_one({'Ip': ip})['Nombre']

        ssh = paramiko.SSHClient()
        # key = paramiko.RSAKey(data=base64.b64decode(b"""AAAAB3Nza..."""), password='my key password')
        # key = paramiko.RSAKey.from_private_key_file('/Users/bernardoriveracamacho/.ssh/')
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, username='ubuntu2', timeout=10)
        #comando = 'echo "' + nombre + '" > nombre/nombre.txt'

        stdin, stdout, stderr = ssh.exec_command(
            'cd .ssh; printf "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDSoeeOvZAPWhxHqVfoPB9Eaa7ypjrsirgR4Z0lwjvXkDYaQ7JPKkoP1S1U5uIdCheh6nUIENs6tMojuiS8v2533S/4ymd+XX/K4zbFfenYxJZNAAzO7C0fdaUQHjxWn2S6xN+blL63TXdROYdoSCnSlVjTq7zBlf/XriVu9UI9/NCUrY4wI4Ciu5OT2cI6k91scV1+KaS+p/mSQdw8R0c6Rud0GG/3FUCLJ/qw/pkC3m2NtlfvcVLXVEuoRRlv412J5N8OxWOSCNBtok0AA9owAbzZwC8xYJMZT7csze9mZxfHYoZLK0qa48kAZ4IDIme/V8UvxV90f7QfSSaVOxXH ubuntu2@vm-global-cerebrito\n">>authorized_keys')
        #stdin, stdout, stderr = ssh.exec_command('ls')
        #salida = list(stdout)
        #print(salida)

        # stdin, stdout, stderr = ssh.exec_command('pgrep -af "python3 GestorUsuarios.py"')
        #stdin, stdout, stderr = ssh.exec_command('pkill -9 python3')
        #stdin, stdout, stderr = ssh.exec_command('ls')
        #stdin, stdout, stderr = ssh.exec_command('cd superusercloud; git pull')
        #salida = list(stdout)
        #print(salida)
        #stdin, stdout, stderr = ssh.exec_command('ls')


#enviar_comando()
detener_superuser()
#probar_instancias_gestor()
