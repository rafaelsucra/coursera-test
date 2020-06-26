import operator as op
##from subprocess import Popen
import subprocess as sp
import os
import pymongo as pm
from datetime import datetime

cliente = pm.MongoClient("localhost",27017,username="admin",password="admin")

db = cliente.AMAZONIA

##criacao da tabela final
"""
## criando novas collection:
nova_col_1 = db["amazonia_satelite"]
nova_col_2 = db["amazonia_satelite_controle_diario"]

nova_col_3 = db["amazonia_satelite_diario"]
col_list = db.list_collection_names()
print(col_list)

## checagem de das collection
if "amazonia_satelite" in col_list:
    print("Collection já existe, dropando - amazonia_satelite!!")
    db.amazonia_satelite.drop()
    print("Collection sendo criada - amazonia_satelite!!")
    nova_col_1 = db["amazonia_satelite"]

if "amazonia_satelite_controle_diario" in col_list:
    print("Collection já existe, dropando - amazonia_satelite_controle_diario!!")
    db.amazonia_satelite_controle_diario.drop()
    print("Collection sendo criada - amazonia_satelite_controle_diario!!")
    nova_col_2 = db["amazonia_satelite_controle_diario"]

if "amazonia_satelite_diario" in col_list:
    print("Collection já existe, dropando - amazonia_satelite_diario!!")
    db.amazonia_satelite_diario.drop()
    print("Collection sendo criada - amazonia_satelite_diario!!")
    nova_col_3 = db["amazonia_satelite_diario"]

def carga_amazonia (nome):
    for v_nome in nome:
        nova_col_1.insert_one(v_nome)
    return nome

v_CARGA_20200512 = db.CARGA_20200512.find({}) 
v_CARGA_20200513 = db.CARGA_20200513.find({})
v_CARGA_20200514 = db.CARGA_20200514.find({})
v_CARGA_20200515 = db.CARGA_20200515.find({})
v_CARGA_20200516 = db.CARGA_20200516.find({})
v_CARGA_20200519 = db.CARGA_20200519.find({})
v_CARGA_20200520 = db.CARGA_20200520.find({})
v_CARGA_20200521 = db.CARGA_20200521.find({})
v_CARGA_20200522 = db.CARGA_20200522.find({})
v_CARGA_20200523 = db.CARGA_20200523.find({})
v_CARGA_20200526 = db.CARGA_20200526.find({})
v_CARGA_20200527 = db.CARGA_20200527.find({})
v_CARGA_20200528 = db.CARGA_20200528.find({})
v_CARGA_20200529 = db.CARGA_20200529.find({})
v_CARGA_20200530 = db.CARGA_20200530.find({})
v_CARGA_20200602 = db.CARGA_20200602.find({})
v_CARGA_20200603 = db.CARGA_20200603.find({})
v_CARGA_20200604 = db.CARGA_20200604.find({})
v_CARGA_20200605 = db.CARGA_20200605.find({})
v_CARGA_20200606 = db.CARGA_20200606.find({})
v_CARGA_20200609 = db.CARGA_20200609.find({})
v_CARGA_20200610 = db.CARGA_20200610.find({})
v_CARGA_20200611 = db.CARGA_20200611.find({})
v_CARGA_20200612 = db.CARGA_20200612.find({})

carga_amazonia(v_CARGA_20200512)
carga_amazonia(v_CARGA_20200513)
carga_amazonia(v_CARGA_20200514)
carga_amazonia(v_CARGA_20200515)
carga_amazonia(v_CARGA_20200516)
carga_amazonia(v_CARGA_20200519)
carga_amazonia(v_CARGA_20200520)
carga_amazonia(v_CARGA_20200521)
carga_amazonia(v_CARGA_20200522)
carga_amazonia(v_CARGA_20200523)
carga_amazonia(v_CARGA_20200526)
carga_amazonia(v_CARGA_20200527)
carga_amazonia(v_CARGA_20200528)
carga_amazonia(v_CARGA_20200529)
carga_amazonia(v_CARGA_20200530)
carga_amazonia(v_CARGA_20200602)
carga_amazonia(v_CARGA_20200603)
carga_amazonia(v_CARGA_20200604)
carga_amazonia(v_CARGA_20200605)
carga_amazonia(v_CARGA_20200606)
carga_amazonia(v_CARGA_20200609)
carga_amazonia(v_CARGA_20200610)
carga_amazonia(v_CARGA_20200611)
carga_amazonia(v_CARGA_20200612)

"""

def del_arq (nome_pasta,nome_arq):
    pasta = nome_pasta
    arquivo = nome_arq
    diretorio = os.listdir(pasta)
    if arquivo in diretorio:
        print('---removendo arquivo----')
        os.remove('{}/{}'.format(pasta, arquivo))
        print('%s removido da pasta %s' % (pasta, arquivo))
    else:
        print('este arquivo nao existe')
    return nome_pasta,nome_arq

v_SETA_VALORES = db.amazonia_satelite.find({})

v_dir_arq = "C:\\Temp\\"
v_nome_arq = "FF_AMAZONIA_SATELITE.csv"

del_arq(v_dir_arq,v_nome_arq)

file = open("C:\\Temp\\FF_AMAZONIA_SATELITE.csv","a")

file.write("uf;municipali;classname;view_date;sensor;satellite;uc;created_at;image_date;areamunkm;areatotalk")

for v_CURSOR_1 in v_SETA_VALORES:
    if v_CURSOR_1["view_date"] == "":
        data_1 = "1900-01-01"
    else: 
        data_1 = v_CURSOR_1["view_date"]
    if  v_CURSOR_1["created_at"] == "":
        data_3 = "1900-01-01"
    else: 
        data_3 = v_CURSOR_1["created_at"]
    if  v_CURSOR_1["image_date"] == "":
        data_5 = "1900-01-01"
    else: 
        data_5 = v_CURSOR_1["image_date"]
    data_2 = datetime.strptime(data_1,'%Y-%m-%d').date()
    data_4 = datetime.strptime(data_3,'%Y-%m-%d').date()
    data_6 = datetime.strptime(data_5,'%Y-%m-%d').date()
    v_saida_area_mun_km = v_CURSOR_1["areamunkm"]
    saida_area_mun_km = str(v_saida_area_mun_km).replace(".",",")
    v_saida_area_de_inicio = v_CURSOR_1["areatotalk"]
    saida_area_de_inicio = str(v_saida_area_de_inicio).replace(".",",")
    file.write('\n'+v_CURSOR_1["uf"]+";"+v_CURSOR_1["municipali"]+";"+v_CURSOR_1["classname"]+";"+str(data_2)+";"+v_CURSOR_1["sensor"]+";"+v_CURSOR_1["satellite"]+";"+v_CURSOR_1["uc"]+";"+str(data_4)+";"+str(data_6)+";"+saida_area_mun_km+";"+saida_area_de_inicio)
file.close()

v_EXTRAI_INDIO = db.AREA_INDIGENA.find({})

v_dir_arq = "C:\\Temp\\"
v_nome_arq = "FF_AMAZONIA_AREA_INDIGENA.csv"

del_arq(v_dir_arq,v_nome_arq)

file = open("C:\\Temp\\FF_AMAZONIA_AREA_INDIGENA.csv","a")

file.write("gid;terrai_cod;terrai_nom;etnia_nome;municipio_;uf_sigla;superficie;fase_ti;modalidade;reestudo_t;cr;faixa_fron;undadm_cod;undadm_nom;undadm_sig")

for v_CURSOR_IND in v_EXTRAI_INDIO:
    file.write('\n'+str(v_CURSOR_IND["gid"])+";"+str(v_CURSOR_IND["terrai_cod"])+";"+v_CURSOR_IND["terrai_nom"]+";"+v_CURSOR_IND["etnia_nome"]+";"+v_CURSOR_IND["municipio_"]+";"+v_CURSOR_IND["uf_sigla"]+";"+str(v_CURSOR_IND["superficie"])+";"+v_CURSOR_IND["fase_ti"]+";"+v_CURSOR_IND["modalidade"]+";"+v_CURSOR_IND["reestudo_t"]+";"+v_CURSOR_IND["cr"]+";"+v_CURSOR_IND["faixa_fron"]+";"+str(v_CURSOR_IND["undadm_cod"])+";"+v_CURSOR_IND["undadm_nom"]+";"+v_CURSOR_IND["undadm_sig"])
file.close()



"""    v_INSERT_NOVA_COLECTION_1 = {
                    "uf" : v_CURSOR_1["uf"],
                    "municipali" : v_CURSOR_1["municipali"],
                    "classname" : v_CURSOR_1["classname"],
                    "view_date" : data_2,
                    "sensor" : v_CURSOR_1["sensor"],
                    "satellite" : v_CURSOR_1["satellite"],
                    "uc" : v_CURSOR_1["uc"],
                    "created_at" : data_4,
                    "image_date" : data_6,
                    "areamunkm" : v_CURSOR_1["areamunkm"],
                    "areatotalk" : v_CURSOR_1["areatotalk"]
                }
    nova_col_3.insert_one(v_INSERT_NOVA_COLECTION_1)   


v_ORDENA_CONSULTA = db.amazonia_satelite.find({}).sort({"uf":1,"municipali":1,"classname":1,"view_date":1,"sensor":1,"satellite":1,"uc":1,"created_at":1,"image_date":1})

v_date_generico="1600-01-01"
v_uf=""
v_municipali=""
v_classname=""
v_view_date=datetime.strptime(v_date_generico,'%Y-%m-%d').date()
v_sensor=""
v_satellite=""
v_uc=""
v_created_at=datetime.strptime(v_date_generico,'%Y-%m-%d').date()
v_image_date=datetime.strptime(v_date_generico,'%Y-%m-%d').date()
areamunkm = 0
areatotalk = 0
areamunkm_ant = 0
areatotalk_ant = 0

for v_CURSOR_ORDENADO in v_ORDENA_CONSULTA:
    areamunkm = v_CURSOR_ORDENADO["areamunkm"]
    areatotalk = v_CURSOR_ORDENADO["areatotalk"]
    if (v_CURSOR_ORDENADO["uf"] == v_uf and v_CURSOR_ORDENADO["municipali"] == v_municipali and v_CURSOR_ORDENADO["classname"] == v_classname and v_CURSOR_ORDENADO["view_date"] ==  v_view_date and v_CURSOR_ORDENADO["sensor"] == v_sensor and v_CURSOR_ORDENADO["satellite"] == v_satellite and v_CURSOR_ORDENADO["uc"] == v_uc and v_CURSOR_ORDENADO["created_at"] == v_created_at and v_CURSOR_ORDENADO["image_date"]==v_image_date):
        areamunkm_ant = areamunkm_ant + areamunkm
        areatotalk_ant = areatotalk_ant + areatotalk
    elif (v_uf == "" and v_CURSOR_ORDENADO["uf"] != v_uf and v_CURSOR_ORDENADO["municipali"] != v_municipali and v_CURSOR_ORDENADO["classname"] != v_classname and v_CURSOR_ORDENADO["view_date"] !=  v_view_date and v_CURSOR_ORDENADO["sensor"] != v_sensor and v_CURSOR_ORDENADO["satellite"] != v_satellite and v_CURSOR_ORDENADO["uc"] != v_uc and v_CURSOR_ORDENADO["created_at"] != v_created_at and v_CURSOR_ORDENADO["image_date"]!=v_image_date):
            v_uf=v_CURSOR_ORDENADO["uf"]
            v_municipali=v_CURSOR_ORDENADO["municipali"]
            v_classname=v_CURSOR_ORDENADO["classname"]
            v_view_date=v_CURSOR_ORDENADO["view_date"]
            v_sensor=v_CURSOR_ORDENADO["sensor"]
            v_satellite=v_CURSOR_ORDENADO["satellite"]
            v_uc=v_CURSOR_ORDENADO["uc"]
            v_created_at=v_CURSOR_ORDENADO["created_at"]
            v_image_date=v_CURSOR_ORDENADO["image_date"]
            areamunkm_ant = areamunkm
            areatotalk_ant = areatotalk
    elif (v_uf != "" and v_CURSOR_ORDENADO["uf"] != v_uf and v_CURSOR_ORDENADO["municipali"] != v_municipali and v_CURSOR_ORDENADO["classname"] != v_classname and v_CURSOR_ORDENADO["view_date"] !=  v_view_date and v_CURSOR_ORDENADO["sensor"] != v_sensor and v_CURSOR_ORDENADO["satellite"] != v_satellite and v_CURSOR_ORDENADO["uc"] != v_uc and v_CURSOR_ORDENADO["created_at"] != v_created_at and v_CURSOR_ORDENADO["image_date"]!=v_image_date):
        v_INSERT_NOVA_COLECTION = {
                    "uf" : v_CURSOR_ORDENADO["uf"],
                    "municipali" : v_CURSOR_ORDENADO["municipali"],
                    "classname" : v_CURSOR_ORDENADO["classname"],
                    "view_date" : v_CURSOR_ORDENADO["view_date"],
                    "sensor" : v_CURSOR_ORDENADO["sensor"],
                    "satellite" : v_CURSOR_ORDENADO["satellite"],
                    "uc" : v_CURSOR_ORDENADO["uc"],
                    "created_at" : v_CURSOR_ORDENADO["created_at"],
                    "image_date" : v_CURSOR_ORDENADO["image_date"],
                    "areamunkm" : areamunkm_ant,
                    "areatotalk" : areatotalk_ant
                }
        nova_col_2.insert(v_INSERT_NOVA_COLECTION)
        v_uf=v_CURSOR_ORDENADO["uf"]
        v_municipali=v_CURSOR_ORDENADO["municipali"]
        v_classname=v_CURSOR_ORDENADO["classname"]
        v_view_date=v_CURSOR_ORDENADO["view_date"]
        v_sensor=v_CURSOR_ORDENADO["sensor"]
        v_satellite=v_CURSOR_ORDENADO["satellite"]
        v_uc=v_CURSOR_ORDENADO["uc"]
        v_created_at=v_CURSOR_ORDENADO["created_at"]
        v_image_date=v_CURSOR_ORDENADO["image_date"]
        areamunkm = 0
        areatotalk = 0
        areamunkm_ant = 0
        areatotalk_ant = 0
    else:
        v_uf=v_CURSOR_ORDENADO["uf"]
        v_municipali=v_CURSOR_ORDENADO["municipali"]
        v_classname=v_CURSOR_ORDENADO["classname"]
        v_view_date=v_CURSOR_ORDENADO["view_date"]
        v_sensor=v_CURSOR_ORDENADO["sensor"]
        v_satellite=v_CURSOR_ORDENADO["satellite"]
        v_uc=v_CURSOR_ORDENADO["uc"]
        v_created_at=v_CURSOR_ORDENADO["created_at"]
        v_image_date=v_CURSOR_ORDENADO["image_date"]

"""