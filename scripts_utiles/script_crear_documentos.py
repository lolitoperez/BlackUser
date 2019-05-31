from pymongo import MongoClient


MONGODB_HOST_HUMAN = '13.52.11.40'
MONGODB_PORT_HUMAN = '27017'
MONGODB_TIMEOUT_HUMAN = 60000
MONGODB_DATABASE_HUMAN = 'XLamudi'
MONGODB_USER_HUMAN = 'Scraper%2Fops'
MONGODB_PASS_HUMAN = 'R3vim3x5o5%2F%2F'
URI_CONNECTION_HUMAN = "mongodb://" + MONGODB_USER_HUMAN + ":" \
                                    + MONGODB_PASS_HUMAN + "@" + MONGODB_HOST_HUMAN \
                                    + ":" + MONGODB_PORT_HUMAN + "/admin"

cliente = MongoClient(URI_CONNECTION_HUMAN)

base_datos = cliente[MONGODB_DATABASE_HUMAN]

coleccion_superuser_cloud_listas = base_datos['superuser_cloud_listas']
coleccion_instancias_cloud = base_datos['instancias_cloud']


#primeros nombres
"""
ids = [
        'global-super-user-03sg',
        'global-super-user-2mm',
        'global-super-user-3d1m',
        'global-super-user-3dk5',
        'global-super-user-3gqs',
        'global-super-user-594l',
        'global-super-user-5sg2',
        'global-super-user-66ft',
        'global-super-user-6ppk',
        'global-super-user-6rh3',
        'global-super-user-7fb6',
        'global-super-user-88hx',
        'global-super-user-8cfl',
        'global-super-user-8crk',
        'global-super-user-8h02',
        'global-super-user-b05k',
        'global-super-user-cdr0',
        'global-super-user-k3v1',
        'global-super-user-kqd8',
        'global-super-user-kt4k',
        'global-super-user-mmr5',
        'global-super-user-ns2h',
        'global-super-user-pjt4',
        'global-super-user-rkrx',
        'global-super-user-t7n3',
        'global-super-user-w8f7',
        'global-super-user-xk2l',
        'global-super-user-xv6b',
        'global-super-user-ztc9',
        'global-super-user-xv8p',
]
"""
#primeras ips
"""
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
        '35.247.68.201',
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
        '35.199.154.92',
        '104.196.250.210',
        '35.247.9.126',
        '35.233.164.149',
    ]
"""


ips = [
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


ids = [
      "intance-group-1js0",
      "intance-group-3fz0",
      "intance-group-3r4z",
      "intance-group-3v53",
      "intance-group-49n6",
      "intance-group-6jjk",
      "intance-group-6vqr",
      "intance-group-74w0",
      "intance-group-75bj",
      "intance-group-7p7b",
      "intance-group-9k2k",
      "intance-group-bw3s",
      "intance-group-cbjt",
      "intance-group-dknd",
      "intance-group-dlf4",
      "intance-group-dpb6",
      "intance-group-f9hf",
      "intance-group-frnq",
      "intance-group-fw69",
      "intance-group-fxns",
      "intance-group-g2s4",
      "intance-group-g3l6",
      "intance-group-gfx5",
      "intance-group-hm49",
      "intance-group-msr6",
      "intance-group-ntg5",
      "intance-group-nwbj",
      "intance-group-rkbg",
      "intance-group-rtnk",
      "intance-group-rwws",
      "intance-group-srd0",
      "intance-group-v2lm",
      "intance-group-wsq2",
      "intance-group-xr59",
]
for indice, ip in enumerate(ips):
    id = ids[indice]
    nombre = 'X_' + str(indice+30)
    documento_listas = {
                    'IP_server': nombre,
                    '22': [],
                    'status2': '',
                    'status22': '',
                    'history': [],
                 }
    documento_instancias = {
            'Nombre': nombre,
            'Ip': ip,
            'status': 'activa',
            'ram': 144.0,
            'cpu': 5.0,
            'trabajos': [],
            'id_google': id,
            'cuenta': 1
    }
    coleccion_superuser_cloud_listas.insert_one(documento_listas)
    coleccion_instancias_cloud.insert_one(documento_instancias)
