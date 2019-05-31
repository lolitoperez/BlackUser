import paramiko
from time import sleep
from datetime import datetime
import multiprocessing
import random
from pathlib import Path
import time
from pymongo import *

#recomendacion cerrar ssh depues de cada uso

class Guardian(object):
	"""docstring for Guardian"""
	def __init__(self, arg):
		super(Guardian, self).__init__()
		self.arg = arg

	def obtener_ips_base_datos(self):
		db = MongoClient('mongodb://Scraper%2Fops:R3vim3x5o5%2F%2F@104.199.125.135:27017/admin').XLamudi
		IPS = [x['Ip'] for x in db['instancias_2'].find({'status': 'inactiva'})] + [y['Ip'] for y in db['instancias_cloud'].find({'status': 'activa'})]	

	def vigilar_ram(self,ssh):
		stdin, stdout, stderr = ssh.exec_command('free -m')
		int(list(stdout)[-2].split('        ')[-1].replace('\n','').strip())
		pass
	def vigilar_cpu(self):
		pass
	def aniquilador_firefox(self):
		pass 
	def aniquilador_python(self):
		pass
	def obtener_ssh(self):
		ssh=paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		pass
		int(list(stdout)[-2].split('        ')[-1].replace('\n','').strip())


print(ip," : ","Usuario",us,int(list(stdout)[-2].split('        ')[-1].replace('\n','').strip()))



db = MongoClient('mongodb://Scraper%2Fops:R3vim3x5o5%2F%2F@104.199.125.135:27017/admin').XLamudi
collection = db['superuser_cloud_listas']
IPS = [x['Ip'] for x in db['instancias_2'].find({'status': 'inactiva'})] + [y['Ip'] for y in db['instancias_cloud'].find({'status': 'activa'})]


grupos=100 #grupos de 'n' 
IPS_seccionada=[IPS[i:i+grupos] for i in range(0,len(IPS),grupos)]
print(IPS)

def enviar_comandos(num_hilo,ip,usuarios):
	for us in usuarios:
		ssh = None

		if us==1:

			ssh = paramiko.SSHClient()
			#key = paramiko.RSAKey.from_private_key_file('/Users/bernardoriveracamacho/.ssh/')
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			try:
				ssh.connect(hostname=ip, username='ubuntu2', timeout=20)


				#stdin, stdout, stderr = ssh.exec_command('git clone https://gitlab.com/RVMXGlobalScraper/superusercloud.git')
				#stdin, stdout, stderr = ssh.exec_command('cd superusercloud; git pull')
				stdin, stdout, stderr = ssh.exec_command('pkill -9 firefox; pkill -9 python3')
				#stdin, stdout, stderr = ssh.exec_command('pwd; cat /home/ubuntu2/nombre/nombre.txt')
				#stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:2;firefox https://www.wikipedia.org/')
				#stdin, stdout, stderr = ssh.exec_command('firefox --version')


				print(ip," : ","Usuario",us," ".join(list(stdout)))


			except Exception as e:
				print(e)
				print('error ',"hilo",num_hilo,"usuario :",us,'ip--->', ip)
				ssh.close()
				del ssh
			finally:
				if ssh:
					ssh.close()
					del ssh

		elif us==2:
			ssh = paramiko.SSHClient()
			#key = paramiko.RSAKey.from_private_key_file('/Users/bernardoriveracamacho/.ssh/')
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			try:
				ssh.connect(hostname=ip, username='ubuntu3', timeout=20)


				#stdin, stdout, stderr = ssh.exec_command('cd superusercloud; git pull')
				#stdin, stdout, stderr = ssh.exec_command('git clone https://gitlab.com/RVMXGlobalScraper/superusercloud.git')
				stdin, stdout, stderr = ssh.exec_command('pkill -9 firefox; pkill -9 python3')
				#stdin, stdout, stderr = ssh.exec_command('pwd; cat /home/ubuntu2/nombre/nombre.txt')
				#stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:3 ; firefox https://www.wikipedia.org/')
				#stdin, stdout, stderr = ssh.exec_command('firefox --version')
				print(ip," : ","Usuario",us," ".join(list(stdout)))




			except Exception as e:
				print(e)
				print('error ',"hilo",num_hilo,"usuario :",us,'ip--->', ip)
				ssh.close()
				del ssh
			finally:
				if ssh:
					ssh.close()
					del ssh

		elif us==3:
			ssh = paramiko.SSHClient()
			#key = paramiko.RSAKey.from_private_key_file('/Users/bernardoriveracamacho/.ssh/')
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			try:
				ssh.connect(hostname=ip, username='ubuntu4', timeout=20)
	



				#stdin, stdout, stderr = ssh.exec_command('cd /home/ubuntu4/superusercloud ; git pull')
				#stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:4 ; firefox https://www.wikipedia.org/')
				#stdin, stdout, stderr = ssh.exec_command('cat /home/ubuntu4/nombre/nombre.txt')
				#stdin, stdout, stderr = ssh.exec_command('firefox --version')
				#stdin, stdout, stderr = ssh.exec_command('pkill -9 firefox; pkill -9 python3')
				#stdin, stdout, stderr = ssh.exec_command('cd /home/ubuntu4/superusercloud ; git pull')
				#stdin, stdout, stderr = ssh.exec_command('pwd; cat /home/ubuntu2/nombre/nombre.txt')
				stdin, stdout, stderr = ssh.exec_command('ps aux | grep python3')
				#stdin, stdout, stderr = ssh.exec_command('export DISPLAY=:4 ; firefox https://www.wikipedia.org/')

				print(ip," : ","Usuario",us," ".join(list(stdout)))
				if ssh:
					ssh.close()


			except Exception as e:
				print(e)
				print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
				print('error ',"hilo",num_hilo,"usuario :",us,'ip--->', ip)
				print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
				ssh.close()
				del ssh
			


def main():
	print(IPS)
	print("Numero de instancias :",len(IPS))
	# for num_hilo,ip in enumerate(IPS):  # del 0 al NUM_HILOS-1
 #        hilos.append(multiprocessing.Process(name=str(num_hilo), target=comandosChido, args=(ip,),
 #                                             daemon=False))  # Nosete que el NOMBRE del hilo corresponde a su número

	usuarios=[3]
	for seccion_IPS in IPS_seccionada:
		hilos=[]
		for num_hilo,ip in enumerate(seccion_IPS):
			hilo=multiprocessing.Process(name=str(num_hilo), target=enviar_comandos, args=(num_hilo,ip,usuarios,),daemon=False)
			hilo.start()
			hilos.append(hilo)
			
		for hilo in hilos:
			hilo.join()

	






if __name__ == '__main__':
	main()


# print('enumerados:'+str(threading.enumerate()))
# for i in range(1):
#     ahora = datetime.now()
#     vigila()
#     #print(len(Check.keys()))
#     #pprint(Check)
#     despues = datetime.now()
#     #print(despues - ahora)
#     print(IPS)