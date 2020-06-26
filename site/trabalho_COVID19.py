# brincadeira do COVID19

# comando no MongoDb para carregar a base do governo

# mongoimport --authenticationDatabase=admin -u admin -p admin -d COVID19 -c covid19_brasil --type csv --file c:\Temp\covid19.csv --headerline
# mongoimport --authenticationDatabase=admin -u admin -p admin -d COVID19 -c localidade --type csv --file c:\Temp\RELATORIO_DTB_BRASIL_MUNICIPIO_tratada_LONG_LAT_FINAL.csv --headerline
# mongoimport --db=users --collection=contacts --file=contacts.json
# mongoimport --authenticationDatabase=admin -u admin -p admin -d YOUTUBE -c youtube_kind --type json --file C:\Users\rolivei5\coursera-test\PowerBI\BaseYoutube\datasets_4549_466349_US_category_id.json


import operator as op

import pymongo as pm
from datetime import datetime

cliente = pm.MongoClient("localhost",27017,username="admin",password="admin")

db = cliente.COVID19

# Chamada do estado
v_ESTADO = input("Digite o estado para ver a quantidade confirmada: ")
v_DATA_FIM = input("DATA NO FORMATO = YYYY-MM-DD: EX:.2020-04-02: ")

## v_DATA_MAXIMA = db_uf.covid19_brasil.find({$max:"date"}{"state":v_ESTADO,"place_type":"state"})

# recepciona valores da consulta para o state
v_RECEPCIONA = db.covid19_brasil.find({"state":v_ESTADO,"place_type":"state"})

# seta valor padrao de inicializacao da variavel
v_DATA_MAXIMA = datetime.strptime("1601-01-01",'%Y-%m-%d').date()

# printa apenas para saber se esta corretamente
print(v_DATA_MAXIMA,type(v_DATA_MAXIMA))

# for para identifica a data maxima
for y in v_RECEPCIONA:
    v_DATA_TEMP = y["date"]
    v_TEMP = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
    print(v_TEMP,type(v_TEMP))
    if v_DATA_MAXIMA < v_TEMP:
        v_DATA_MAXIMA = v_TEMP

# print da data mais atual
print("Data maxima {}".format(str(v_DATA_MAXIMA)))

# efetua o filtro pela data mais atual na base
v_CAMPO_CONFIRMADOS = db.covid19_brasil.find({"date":str(v_DATA_MAXIMA),"state":v_ESTADO,"place_type":"state"})

v_VALOR = 0


# Somatorio do valor de confirmados
for i in v_CAMPO_CONFIRMADOS:
    v_VALOR = i["last_available_confirmed"]+v_VALOR

print("Total contabilizado do estado do {} foi: {} ".format(v_ESTADO,v_VALOR))

##### trabalhando a nivel de municipios:

## api ajudou muito
## https://api.mongodb.com/python/current/tutorial.html

# mongoimport --authenticationDatabase=admin -u admin -p admin -d COVID19 -c localidade --type csv --file c:\Temp\Sedes_Coordenadas_Municipios.csv --headerline
# mongoimport --authenticationDatabase=admin -u admin -p admin -d COVID19 -c localidade --type csv --file c:\Temp\RELATORIO_DTB_BRASIL_MUNICIPIO_tratada_LONG_LAT_FINAL.csv --headerline

v_RECEPCIONA_2 = db.covid19_brasil.find({"place_type":"city"})

v_CONT = 0

## criação de uma nova collection

nova_col = db["covid19_localidade"]
col_list = db.list_collection_names()
print(col_list)

if "covid19_localidade" in col_list:
    print("Collection já existe, dropando!!")
    db.covid19_localidade.drop()
    print("Collection sendo criada!!")
    nova_col = db["covid19_localidade"]


for v_CURSOR in v_RECEPCIONA_2:
    v_LOC = db.localidade.find({"Codigo_Municipio_Completo":v_CURSOR["city_ibge_code"]})
    for v_CURSOR_2 in v_LOC:
        v_CONT = v_CONT + 1
        #v_NOVA_COLECAO = v_CURSOR[""]
        ##print(v_CURSOR_2["CODIGO_MUNICIPIO"])
        v_PREPARANDO_INSERT = {
                                "id_controle" : v_CURSOR["_id"],
                                "epidemiological_week" : v_CURSOR["epidemiological_week"],
                                "date" : v_CURSOR["date"],
                                "order_for_place" : v_CURSOR["order_for_place"],
                                "state" : v_CURSOR["state"],
                                "city" : v_CURSOR["city"],
                                "city_ibge_code" : v_CURSOR["city_ibge_code"],
                                "place_type" : v_CURSOR["place_type"],
                                "last_available_confirmed" : v_CURSOR["last_available_confirmed"],
                                "last_available_confirmed_per_100k_inhabitants" : v_CURSOR["last_available_confirmed_per_100k_inhabitants"],
                                "new_confirmed" : v_CURSOR["new_confirmed"],
                                "last_available_deaths" : v_CURSOR["last_available_deaths"],
                                "new_deaths" : v_CURSOR["new_deaths"],
                                "last_available_death_rate" : v_CURSOR["last_available_death_rate"],
                                "estimated_population_2019" : v_CURSOR["estimated_population_2019"],
                                "is_last" : v_CURSOR["is_last"],
                                "is_repeated" : v_CURSOR["is_repeated"],
                                "longitude":v_CURSOR_2["LONGITUDE"],
                                "latitude":v_CURSOR_2["LATITUDE"]
                            }
        ## v_INSERT_RESULT = {"longitude":v_CURSOR_2["LONGITUDE"],"latitude":v_CURSOR_2["LATITUDE"]}
        ## v_QUEM = {"$set":{"_id":v_CURSOR["_id"]}}
        nova_col.insert_one(v_PREPARANDO_INSERT)

print(str(v_CONT))

##covid19 - indice de transmissao por estado e cidade:
## 1% significa alarmante
## total geral UF=> confirmados por estados/confirmados geral Pais
## total geral Cidade=> confirmados por municipio/confirmados geral no Estado

## criando base por UF
# recepciona valores da consulta para o state
## tentei com: v_RECEPCIONA_4 = db.covid19_localidade.distinct("state") 
v_RECEPCIONA_4 = db.UF.find({})


## criando novas collection:
nova_col_1 = db["covid19_geral_pais"]
nova_col_2 = db["covid19_geral_estado"]
nova_col_3 = db["covid19_geral_municipio"]
col_list = db.list_collection_names()
print(col_list)

## checagem de das collection
if "covid19_geral_pais" in col_list:
    print("Collection já existe, dropando - covid19_geral_pais!!")
    db.covid19_geral_pais.drop()
    print("Collection sendo criada - covid19_geral_pais!!")
    nova_col_1 = db["covid19_geral_pais"]

if "covid19_geral_estado" in col_list:
    print("Collection já existe, dropando - covid19_geral_estado!!")
    db.covid19_geral_estado.drop()
    print("Collection sendo criada - covid19_geral_estado!!")
    nova_col_2 = db["covid19_geral_estado"]

if "covid19_geral_municipio" in col_list:
    print("Collection já existe, dropando - covid19_geral_municipio!!")
    db.covid19_geral_municipio.drop()
    print("Collection sendo criada - covid19_geral_municipio!!")
    nova_col_3 = db["covid19_geral_municipio"]

col_list_uf = db.list_collection_names()

nova_col_RJ = db["covid19_estado_RJ"]

## checagem de das collection
if "covid19_estado_RJ" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_RJ!!")
    db.covid19_estado_RJ.drop()
    print("Collection sendo criada - covid19_estado_RJ!!")
    nova_col_RJ = db["covid19_estado_RJ"]
	
nova_col_SP = db["covid19_estado_SP"]

if "covid19_estado_SP" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_SP!!")
    db.covid19_estado_SP.drop()
    print("Collection sendo criada - covid19_estado_SP!!")
    nova_col_SP = db["covid19_estado_SP"]

nova_col_MG = db["covid19_estado_MG"]

if "covid19_estado_MG" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_MG!!")
    db.covid19_estado_MG.drop()
    print("Collection sendo criada - covid19_estado_MG!!")
    nova_col_MG = db["covid19_estado_MG"]
	
nova_col_AC = db["covid19_estado_AC"]

if "covid19_estado_AC" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_AC!!")
    db.covid19_estado_AC.drop()
    print("Collection sendo criada - covid19_estado_AC!!")
    nova_col_AC = db["covid19_estado_AC"]

nova_col_AL = db["covid19_estado_AL"]

if "covid19_estado_AL" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_AL!!")
    db.covid19_estado_AL.drop()
    print("Collection sendo criada - covid19_estado_AL!!")
    nova_col_AL = db["covid19_estado_AL"]
	
nova_col_AM = db["covid19_estado_AM"]    

if "covid19_estado_AM" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_AM!!")
    db.covid19_estado_AM.drop()
    print("Collection sendo criada - covid19_estado_AM!!")
    nova_col_AM = db["covid19_estado_AM"]
	
nova_col_AP = db["covid19_estado_AP"]    

if "covid19_estado_AP" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_AP!!")
    db.covid19_estado_AP.drop()
    print("Collection sendo criada - covid19_estado_AP!!")
    nova_col_AP = db["covid19_estado_AP"]
	
nova_col_BA = db["covid19_estado_BA"]

if "covid19_estado_BA" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_BA!!")
    db.covid19_estado_BA.drop()
    print("Collection sendo criada - covid19_estado_BA!!")
    nova_col_BA = db["covid19_estado_BA"]
	
nova_col_CE = db["covid19_estado_CE"]

if "covid19_estado_CE" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_CE!!")
    db.covid19_estado_CE.drop()
    print("Collection sendo criada - covid19_estado_CE!!")
    nova_col_CE = db["covid19_estado_CE"]
	
nova_col_DF = db["covid19_estado_DF"]

if "covid19_estado_DF" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_DF!!")
    db.covid19_estado_DF.drop()
    print("Collection sendo criada - covid19_estado_DF!!")
    nova_col_DF = db["covid19_estado_DF"]
	
nova_col_ES = db["covid19_estado_ES"]

if "covid19_estado_ES" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_ES!!")
    db.covid19_estado_ES.drop()
    print("Collection sendo criada - covid19_estado_SP!!")
    nova_col_ES = db["covid19_estado_ES"]
	
nova_col_GO = db["covid19_estado_GO"]

if "covid19_estado_GO" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_GO!!")
    db.covid19_estado_GO.drop()
    print("Collection sendo criada - covid19_estado_GO!!")
    nova_col_GO = db["covid19_estado_GO"]
	
nova_col_MA = db["covid19_estado_MA"]

if "covid19_estado_MA" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_MA!!")
    db.covid19_estado_MA.drop()
    print("Collection sendo criada - covid19_estado_MA!!")
    nova_col_MA = db["covid19_estado_MA"]
	
nova_col_MS = db["covid19_estado_MS"]

if "covid19_estado_MS" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_MS!!")
    db.covid19_estado_MS.drop()
    print("Collection sendo criada - covid19_estado_MS!!")
    nova_col_MS = db["covid19_estado_MS"]
	
nova_col_MT = db["covid19_estado_MT"]

if "covid19_estado_MT" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_MT!!")
    db.covid19_estado_MT.drop()
    print("Collection sendo criada - covid19_estado_MT!!")
    nova_col_MT = db["covid19_estado_MT"]
	
nova_col_PA = db["covid19_estado_PA"]

if "covid19_estado_PA" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_PA!!")
    db.covid19_estado_PA.drop()
    print("Collection sendo criada - covid19_estado_PA!!")
    nova_col_PA = db["covid19_estado_PA"]
	
nova_col_PB = db["covid19_estado_PB"]

if "covid19_estado_PB" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_PB!!")
    db.covid19_estado_PB.drop()
    print("Collection sendo criada - covid19_estado_PB!!")
    nova_col_PB = db["covid19_estado_PB"]
	
nova_col_PE = db["covid19_estado_PE"]

if "covid19_estado_PE" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_PE!!")
    db.covid19_estado_PE.drop()
    print("Collection sendo criada - covid19_estado_PE!!")
    nova_col_PE = db["covid19_estado_PE"]
	
nova_col_PI = db["covid19_estado_PI"]

if "covid19_estado_PI" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_PI!!")
    db.covid19_estado_PI.drop()
    print("Collection sendo criada - covid19_estado_PI!!")
    nova_col_PI = db["covid19_estado_PI"]
	
nova_col_PR = db["covid19_estado_PR"]

if "covid19_estado_PR" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_PR!!")
    db.covid19_estado_PR.drop()
    print("Collection sendo criada - covid19_estado_PR!!")
    nova_col_PR = db["covid19_estado_PR"]
	
nova_col_RN = db["covid19_estado_RN"]

if "covid19_estado_RN" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_RN!!")
    db.covid19_estado_RN.drop()
    print("Collection sendo criada - covid19_estado_RN!!")
    nova_col_RN = db["covid19_estado_RN"]

nova_col_RO = db["covid19_estado_RO"]

if "covid19_estado_RO" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_RO!!")
    db.covid19_estado_RO.drop()
    print("Collection sendo criada - covid19_estado_RO!!")
    nova_col_RO = db["covid19_estado_RO"]
	
nova_col_RR = db["covid19_estado_RR"]

if "covid19_estado_RR" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_RR!!")
    db.covid19_estado_RR.drop()
    print("Collection sendo criada - covid19_estado_RR!!")
    nova_col_RR = db["covid19_estado_RR"]
	
nova_col_RS = db["covid19_estado_RS"]

if "covid19_estado_RS" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_RS!!")
    db.covid19_estado_RS.drop()
    print("Collection sendo criada - covid19_estado_RS!!")
    nova_col_RS = db["covid19_estado_RS"]
	
nova_col_SC = db["covid19_estado_SC"]

if "covid19_estado_SC" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_SC!!")
    db.covid19_estado_SC.drop()
    print("Collection sendo criada - covid19_estado_SC!!")
    nova_col_SC = db["covid19_estado_SC"]

nova_col_SE = db["covid19_estado_SE"]

if "covid19_estado_SE" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_SE!!")
    db.covid19_estado_SE.drop()
    print("Collection sendo criada - covid19_estado_SE!!")
    nova_col_SE = db["covid19_estado_SE"]

nova_col_TO = db["covid19_estado_TO"]

if "covid19_estado_TO" in col_list_uf:
    print("Collection já existe, dropando - covid19_estado_TO!!")	
    db.covid19_estado_TO.drop()
    print("Collection sendo criada - covid19_estado_TO!!")
    nova_col_TO = db["covid19_estado_TO"]

if "covid19_geral_municipio" in col_list:
    print("Collection já existe, dropando - covid19_geral_municipio!!")
    db.covid19_municipio.drop()
    print("Collection sendo criada - covid19_geral_municipio!!")
    nova_col_3 = db["covid19_geral_municipio"]

v_RECEPCIONA_3 = db.covid19_localidade.find({})

for v_CURSOR_4 in v_RECEPCIONA_3:
        v_PREPARANDO_INSERT_MUNICIPIO = {
                                "epidemiological_week" : v_CURSOR_4["epidemiological_week"],
                                "date" : v_CURSOR_4["date"],
                                "order_for_place" : v_CURSOR_4["order_for_place"],
                                "state" : v_CURSOR_4["state"],
                                "city" : v_CURSOR_4["city"],
                                "last_available_confirmed" : v_CURSOR_4["last_available_confirmed"],
                                "new_confirmed" : v_CURSOR_4["new_confirmed"],
                                "last_available_deaths" : v_CURSOR_4["last_available_deaths"],
                                "new_deaths" : v_CURSOR_4["new_deaths"],
                                "longitude":v_CURSOR_4["longitude"],
                                "latitude":v_CURSOR_4["latitude"]
                            }
        nova_col_3.insert_one(v_PREPARANDO_INSERT_MUNICIPIO)

##v_LIST = []

##for v_CURSOR_5 in v_RECEPCIONA_4:
##        v_REP_1 = db.covid19_localidade.find({"state":v_CURSOR_5["state"]})
##        for v_CURSOR_LISTA in v_REP_1:
##            v_LIST.append(v_CURSOR_LISTA)
            ##print(str(v_LIST))
            
##v_LIST_ORDER = sorted(v_LIST, key=op.attrgetter('state','date','epidemiological_week'))
##print(str(v_LIST_ORDER))

for v_CURSOR_5 in v_RECEPCIONA_4:
    v_VALOR = db.covid19_localidade.find({"state":v_CURSOR_5["state"]})
    for v_CARREGA in v_VALOR:
        v_UF = v_CARREGA["state"]
        if v_UF == "RJ":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_RJ.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "SP":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_SP.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "MG":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_MG.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "AC":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_AC.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "AL":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_AL.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "AM":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_AM.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "AP":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_AP.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "BA":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_BA.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "CE":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_CE.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "DF":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_DF.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "ES":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_ES.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "GO":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_GO.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "MA":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_MA.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "MS":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_MS.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "MT":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_MT.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "PA":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_PA.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "PB":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_PB.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "PE":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_PE.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "PI":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_PI.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "PR":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_PR.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "RN":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_RN.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "RO":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_RO.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "RR":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_RR.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "RS":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_RS.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "SC":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_SC.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "SE":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_SE.insert_one(v_PREPARANDO_INSERT_ESTADOS)
        elif v_UF == "TO":
            v_PREPARANDO_INSERT_ESTADOS = {
                                        "epidemiological_week" : v_CARREGA["epidemiological_week"],
                                        "date" : v_CARREGA["date"],
                                        "state" : v_CARREGA["state"],
                                        "last_available_confirmed" : v_CARREGA["last_available_confirmed"],
                                        "new_confirmed" : v_CARREGA["new_confirmed"],
                                        "last_available_deaths" : v_CARREGA["last_available_deaths"],
                                        "new_deaths" : v_CARREGA["new_deaths"]
                                    }
            nova_col_TO.insert_one(v_PREPARANDO_INSERT_ESTADOS)

""" bloco RJ """
v_UF_VALOR = db.covid19_estado_RJ.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    """if v_DATA_WEEK == v_DATA_FINALIZACAO:
        print("ENTREI AKI 3")
        v_PREPARANDO_INSERT_RJ = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_RJ["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
        nova_col_2.insert_one(v_PREPARANDO_INSERT_RJ)"""
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "RJ",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco AC """
v_UF_VALOR = db.covid19_estado_AC.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    """if v_DATA_WEEK == v_DATA_FINALIZACAO:
        print("ENTREI AKI 3")
        v_PREPARANDO_INSERT_RJ = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_RJ["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
        nova_col_2.insert_one(v_PREPARANDO_INSERT_RJ)"""
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "AC",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco AL """
v_UF_VALOR = db.covid19_estado_AL.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    """if v_DATA_WEEK == v_DATA_FINALIZACAO:
        print("ENTREI AKI 3")
        v_PREPARANDO_INSERT_RJ = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_RJ["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
        nova_col_2.insert_one(v_PREPARANDO_INSERT_RJ)"""
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "AL",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco AM """
v_UF_VALOR = db.covid19_estado_AM.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "AM",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco AP """
v_UF_VALOR = db.covid19_estado_AP.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "AP",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco BA """
v_UF_VALOR = db.covid19_estado_BA.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "BA",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco CE """
v_UF_VALOR = db.covid19_estado_CE.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "CE",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco DF """
v_UF_VALOR = db.covid19_estado_DF.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "DF",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco ES """
v_UF_VALOR = db.covid19_estado_ES.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "ES",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco GO """
v_UF_VALOR = db.covid19_estado_GO.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "GO",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco MA """
v_UF_VALOR = db.covid19_estado_MA.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "MA",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco MG """
v_UF_VALOR = db.covid19_estado_MG.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "MG",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco MS """
v_UF_VALOR = db.covid19_estado_MS.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "MS",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco MT """
v_UF_VALOR = db.covid19_estado_MT.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "MT",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco PA """
v_UF_VALOR = db.covid19_estado_PA.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "PA",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco PB """
v_UF_VALOR = db.covid19_estado_PB.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "PB",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco PE """
v_UF_VALOR = db.covid19_estado_PE.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "PE",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco PI """
v_UF_VALOR = db.covid19_estado_PI.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "PI",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco PR """
v_UF_VALOR = db.covid19_estado_PR.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "PR",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco RN """
v_UF_VALOR = db.covid19_estado_RN.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "RN",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco RO """
v_UF_VALOR = db.covid19_estado_RO.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "RO",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco RR """
v_UF_VALOR = db.covid19_estado_RR.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "RR",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco RS """
v_UF_VALOR = db.covid19_estado_RS.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "RS",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco SC """
v_UF_VALOR = db.covid19_estado_SC.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "SC",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco SE """
v_UF_VALOR = db.covid19_estado_SE.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "SE",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco SP """
v_UF_VALOR = db.covid19_estado_SP.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "SP",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

""" bloco TO """
v_UF_VALOR = db.covid19_estado_TO.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_UF in v_UF_VALOR:
    v_DATA_WEEK =  v_CURSOR_UF["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_UF["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_CURSOR_UF["state"],
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_UF["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_UF["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_UF["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_UF["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_UF["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_UF["epidemiological_week"]
print("FINAL:")
print(str(v_EPIDEMIA_WEEK_ANT)+"-"+str(v_DATA_WEEK_ANT)+"-"+str(v_SOMA_CURSOR_1)+"-"+str(v_SOMA_CURSOR_2)+"-"+str(v_SOMA_CURSOR_3)+"-"+str(v_SOMA_CURSOR_4))
v_PREPARANDO_INSERT_UF = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : "TO",
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_2.insert_one(v_PREPARANDO_INSERT_UF)

## criando base nivel pais:
print("INICIO DA CARGA DO PAIS:")

v_PAIS = db.covid19_geral_estado.find({}).sort("date",1)

v_DATA_TEMP = "1600-01-01"
v_STATE_ANT = "NI"
v_EPIDEMIA_WEEK_ANT = 0
v_DATA_WEEK_ANT = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_INICIAL = datetime.strptime(v_DATA_TEMP,'%Y-%m-%d').date()
v_DATA_FINALIZACAO = datetime.strptime(v_DATA_FIM,'%Y-%m-%d').date()
v_SOMA_CURSOR_1 = 0
v_SOMA_CURSOR_2 = 0
v_SOMA_CURSOR_3 = 0
v_SOMA_CURSOR_4 = 0
print(v_DATA_WEEK_ANT)

for v_CURSOR_PAIS in v_PAIS:
    v_DATA_WEEK =  v_CURSOR_PAIS["date"]
    print(v_DATA_WEEK)
    print(v_DATA_WEEK_ANT)
    v_EPIDEMIA_WEEK = v_CURSOR_PAIS["epidemiological_week"]
    if  v_DATA_WEEK == v_DATA_WEEK_ANT:
            print("ENTREI AKI")
            v_DATA_WEEK_ANT = v_DATA_WEEK
            v_EPIDEMIA_WEEK_ANT = v_EPIDEMIA_WEEK
            v_SOMA_CURSOR_1 = v_CURSOR_PAIS["last_available_confirmed"]+v_SOMA_CURSOR_1
            v_SOMA_CURSOR_2 = v_CURSOR_PAIS["new_confirmed"]+v_SOMA_CURSOR_2
            v_SOMA_CURSOR_3 = v_CURSOR_PAIS["last_available_deaths"]+v_SOMA_CURSOR_3
            v_SOMA_CURSOR_4 = v_CURSOR_PAIS["new_deaths"]+v_SOMA_CURSOR_4
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT != v_DATA_INICIAL:
                print("ENTREI AKI 2")
                v_PREPARANDO_INSERT_PAIS = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_1.insert_one(v_PREPARANDO_INSERT_PAIS)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_PAIS["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_PAIS["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_PAIS["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_PAIS["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_PAIS["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_PAIS["epidemiological_week"]
    elif v_DATA_WEEK != v_DATA_WEEK_ANT and v_DATA_WEEK_ANT == v_DATA_INICIAL:
                v_SOMA_CURSOR_1 = v_CURSOR_PAIS["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_PAIS["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_PAIS["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_PAIS["new_deaths"]
                v_DATA_WEEK_ANT = v_CURSOR_PAIS["date"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_PAIS["epidemiological_week"]

v_PREPARANDO_INSERT_PAIS = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
nova_col_1.insert_one(v_PREPARANDO_INSERT_PAIS)

print("FIM DA CARGA DA COLLECTION PAIS:")

## montando indice mês:

## criando novas collection:
nova_col_est = db["covid19_estado"]
nova_col_mun = db["covid19_municipio"]
col_list = db.list_collection_names()
print(col_list)

if "covid19_estado" in col_list:
    print("Collection já existe, dropando - covid19_estado!!")
    db.covid19_estado.drop()
    print("Collection sendo criada - covid19_estado!!")
    nova_col_est = db["covid19_estado"]

if "covid19_mun" in col_list:
    print("Collection já existe, dropando - covid19_mun!!")
    db.covid19_municipio.drop()
    print("Collection sendo criada - covid19_geral_mun!!")
    nova_col_mun = db["covid19_municipio"]

v_INDICE_MES = db.covid19_geral_estado.find({})
v_INDICE_MUN = db.covid19_geral_municipio.find({})

for v_IND_MES in v_INDICE_MES:
    v_VAL_IND = db.covid19_geral_pais.find({"date":v_IND_MES["date"]})
    for v_IND_MES_PAIS in v_VAL_IND:
        v_SEMANA = v_IND_MES["epidemiological_week"]
        v_DATA = v_IND_MES["date"]
        if v_IND_MES_PAIS["last_available_confirmed"]==0: 
            v_CONF_ANT = 1 
        else: 
            v_CONF_ANT = v_IND_MES_PAIS["last_available_confirmed"]
        if v_IND_MES_PAIS["new_confirmed"]==0: 
            v_CONF = 1 
        else: 
            v_CONF = v_IND_MES_PAIS["new_confirmed"]
        if v_IND_MES_PAIS["last_available_deaths"]==0: 
            v_MORTE_ANT = 1 
        else: 
            v_MORTE_ANT = v_IND_MES_PAIS["last_available_deaths"]
        if v_IND_MES_PAIS["new_deaths"]==0: 
            v_MORTE = 1 
        else: 
            v_MORTE = v_IND_MES_PAIS["new_deaths"]
        v_CONFIRMADOS_ANT = (v_IND_MES["last_available_confirmed"]*100)/v_CONF_ANT
        v_CONFIRMADOS = (v_IND_MES["new_confirmed"]*100)/v_CONF
        v_MORTOS_ANT = (v_IND_MES["last_available_deaths"]*100)/v_MORTE_ANT
        v_MORTOS = (v_IND_MES["new_deaths"]*100)/v_MORTE
        v_PREPARANDO_INSERT = {
                                "epidemiological_week" : v_SEMANA,
                                "date" : v_DATA,
                                "state" : v_IND_MES["state"],
                                "last_available_confirmed" : v_IND_MES["last_available_confirmed"],
                                "confirmados_pais" : v_IND_MES_PAIS["last_available_confirmed"],
                                "indice_confirmado_anterior" : v_CONFIRMADOS_ANT,
                                "new_confirmed" : v_IND_MES["new_confirmed"],
                                "confirmados_novo_pais" : v_IND_MES_PAIS["new_confirmed"],
                                "indice_novo_confirmado" : v_CONFIRMADOS,
                                "last_available_deaths" : v_IND_MES["last_available_deaths"], 
                                "mortos_pais" : v_IND_MES_PAIS["last_available_deaths"],
                                "indice_mortes_anterior" : v_MORTOS_ANT,
                                "new_deaths" : v_IND_MES["new_deaths"],
                                "mortos_novo_pais" : v_IND_MES_PAIS["new_deaths"],
                                "indice_mortes_novas" : v_MORTOS

                            }
        nova_col_est.insert_one(v_PREPARANDO_INSERT)

v_CONF_ANT = 0
v_CONF = 0
v_MORTE_ANT = 0
v_MORTE = 0
v_CONFIRMADOS_ANT = 0
v_CONFIRMADOS = 0
v_MORTOS_ANT = 0
v_MORTOS = 0

for v_IND_MUN in v_INDICE_MUN:
    v_VAL_IND = db.covid19_estado.find({"date":v_IND_MUN["date"],"state":v_IND_MUN["state"]})
    for v_IND_MUN_EST in v_VAL_IND:
        v_SEMANA = v_IND_MUN["epidemiological_week"]
        v_DATA = v_IND_MUN["date"]
        if v_IND_MUN_EST["last_available_confirmed"]==0: 
            v_CONF_ANT = 1 
        else: 
            v_CONF_ANT = v_IND_MUN_EST["last_available_confirmed"]
        if v_IND_MUN_EST["new_confirmed"]==0: 
            v_CONF = 1 
        else:
            v_CONF = v_IND_MUN_EST["new_confirmed"]
        if v_IND_MUN_EST["last_available_deaths"]==0:
            v_MORTE_ANT = 1 
        else: 
            v_MORTE_ANT = v_IND_MUN_EST["last_available_deaths"]
        if v_IND_MUN_EST["new_deaths"]==0: 
            v_MORTE = 1 
        else: 
            v_MORTE = v_IND_MUN_EST["new_deaths"]
        v_CONFIRMADOS_ANT = (v_IND_MUN["last_available_confirmed"]*100)/v_CONF_ANT
        v_CONFIRMADOS = (v_IND_MUN["new_confirmed"]*100)/v_CONF
        v_MORTOS_ANT = (v_IND_MUN["last_available_deaths"]*100)/v_MORTE_ANT
        v_MORTOS = (v_IND_MUN["new_deaths"]*100)/v_MORTE
        v_PREPARANDO_INSERT = {
                                "epidemiological_week" : v_SEMANA,
                                "date" : v_DATA,
                                "state" : v_IND_MUN["state"],
                                "city" : v_IND_MUN["city"],
                                "last_available_confirmed" : v_IND_MUN["last_available_confirmed"],
                                "confirmados_uf" : v_IND_MUN_EST["last_available_confirmed"],
                                "indice_confirmado_anterior" : v_CONFIRMADOS_ANT,
                                "new_confirmed" : v_IND_MUN["new_confirmed"],
                                "confirmados_novo_uf" : v_IND_MUN_EST["new_confirmed"],
                                "indice_novo_confirmado" : v_CONFIRMADOS,
                                "last_available_deaths" : v_IND_MUN["last_available_deaths"], 
                                "mortos_uf" : v_IND_MUN_EST["last_available_deaths"],
                                "indice_mortes_anterior" : v_MORTOS_ANT,
                                "new_deaths" : v_IND_MUN["new_deaths"],
                                "mortos_novo_uf" : v_IND_MUN_EST["new_deaths"],
                                "indice_mortes_novas" : v_MORTOS

                            }
        nova_col_mun.insert_one(v_PREPARANDO_INSERT)

"""v_RECEPCIONA_5 = sorted(v_REP_1, key=itemgetter(3,4))
        for v_CURSOR_6 in v_RECEPCIONA_5:
            v_STATE = v_CURSOR_6["state"]
            v_DATA_WEEK = v_CURSOR_6["date"]
            v_EPIDEMIA_WEEK = v_CURSOR_6["epidemiological_week"]
            if (v_STATE == v_STATE_ANT and v_DATA_WEEK == v_DATA_WEEK_ANT and v_EPIDEMIA_WEEK_ANT == v_EPIDEMIA_WEEK):
                ##v_EPIDEMIA_WEEK_ANT = v_CURSOR_6["epidemiological_week"]
                ##v_DATA_WEEK_ANT = v_CURSOR_6["date"]
                ##v_STATE_ANT = v_CURSOR_6["state"]
                v_SOMA_CURSOR_1 = v_CURSOR_6["last_available_confirmed"]+v_SOMA_CURSOR_1
                v_SOMA_CURSOR_2 = v_CURSOR_6["new_confirmed"]+v_SOMA_CURSOR_2
                v_SOMA_CURSOR_3 = v_CURSOR_6["last_available_deaths"]+v_SOMA_CURSOR_3
                v_SOMA_CURSOR_4 = v_CURSOR_6["new_deaths"]+v_SOMA_CURSOR_4
            elif (v_STATE != v_STATE_ANT and v_DATA_WEEK != v_DATA_WEEK_ANT and v_EPIDEMIA_WEEK_ANT != v_EPIDEMIA_WEEK):
                v_PREPARANDO_INSERT_ESTADOS = {
                                "epidemiological_week" : v_EPIDEMIA_WEEK_ANT,
                                "date" : v_DATA_WEEK_ANT,
                                "state" : v_STATE_ANT,
                                "last_available_confirmed" : v_SOMA_CURSOR_1,
                                "new_confirmed" : v_SOMA_CURSOR_2,
                                "last_available_deaths" : v_SOMA_CURSOR_3,
                                "new_deaths" : v_SOMA_CURSOR_4
                            }
                nova_col_2.insert_one(v_PREPARANDO_INSERT_ESTADOS)
                ##print(v_PREPARANDO_INSERT_ESTADOS)
                v_SOMA_CURSOR_1 = v_CURSOR_6["last_available_confirmed"]
                v_SOMA_CURSOR_2 = v_CURSOR_6["new_confirmed"]
                v_SOMA_CURSOR_3 = v_CURSOR_6["last_available_deaths"]
                v_SOMA_CURSOR_4 = v_CURSOR_6["new_deaths"]
                v_EPIDEMIA_WEEK_ANT = v_CURSOR_6["epidemiological_week"]
                v_DATA_WEEK_ANT = v_CURSOR_6["date"]
                v_STATE_ANT = v_CURSOR_6["state"]
"""

# exemplo de ordenar: 
# db.getCollection('faculdades').find({},{"sigla":1,"cidade":1}).sort({"cidade":1})

v_EXTRACAO = db.covid19_localidade.find()

## v_LISTA_SAIDA = []

file = open("C:\\Temp\\SAIDA_COVID19_LOCALIDADE.csv","a")

v_HEADER = "id_controle,epidemiological_week,date,order_for_place,state,city,city_ibge_code,place_type,last_available_confirmed,last_available_confirmed_per_100k_inhabitants,new_confirmed,last_available_deaths,new_deaths,last_available_death_rate,estimated_population_2019,is_last,is_repeated,longitude,latitude"

file.write(v_HEADER+'\n')

for v_CURSOR_3 in v_EXTRACAO:
    ## v_LISTA_SAIDA.append(v_CURSOR_3)
    ## v_LISTA_SAIDA = v_CURSOR_3["id_controle","epidemiological_week"]
    v_LISTA_SAIDA_1 = v_CURSOR_3["id_controle"]
    v_LISTA_SAIDA_2 = v_CURSOR_3["epidemiological_week"]
    v_LISTA_SAIDA_3 = v_CURSOR_3["date"]
    v_LISTA_SAIDA_4 = v_CURSOR_3["order_for_place"]
    v_LISTA_SAIDA_5 = v_CURSOR_3["state"]
    v_LISTA_SAIDA_6 = v_CURSOR_3["city"]
    v_LISTA_SAIDA_7 = v_CURSOR_3["city_ibge_code"]
    v_LISTA_SAIDA_8 = v_CURSOR_3["place_type"]
    v_LISTA_SAIDA_9 = v_CURSOR_3["last_available_confirmed"]
    v_LISTA_SAIDA_10 = v_CURSOR_3["last_available_confirmed_per_100k_inhabitants"]
    v_LISTA_SAIDA_11 = v_CURSOR_3["new_confirmed"]    
    v_LISTA_SAIDA_12 = v_CURSOR_3["last_available_deaths"]
    v_LISTA_SAIDA_13 = v_CURSOR_3["new_deaths"]
    v_LISTA_SAIDA_14 = v_CURSOR_3["last_available_death_rate"]
    v_LISTA_SAIDA_15 = v_CURSOR_3["estimated_population_2019"]
    v_LISTA_SAIDA_16 = v_CURSOR_3["is_last"]
    v_LISTA_SAIDA_17 = v_CURSOR_3["is_repeated"]
    v_LISTA_SAIDA_18 = v_CURSOR_3["longitude"]
    v_LISTA_SAIDA_19 = v_CURSOR_3["latitude"]
    v_LISTA_SAIDA = str(v_LISTA_SAIDA_1)+','+str(v_LISTA_SAIDA_2)+','+str(v_LISTA_SAIDA_3)+','+str(v_LISTA_SAIDA_4)+','+str(v_LISTA_SAIDA_5)+','+str(v_LISTA_SAIDA_6)+','+str(v_LISTA_SAIDA_7)+','+str(v_LISTA_SAIDA_8)+','+str(v_LISTA_SAIDA_9)+','+str(v_LISTA_SAIDA_10)+','+str(v_LISTA_SAIDA_11)+','+str(v_LISTA_SAIDA_12)+','+str(v_LISTA_SAIDA_13)+','+str(v_LISTA_SAIDA_14)+','+str(v_LISTA_SAIDA_15)+','+str(v_LISTA_SAIDA_16)+','+str(v_LISTA_SAIDA_17)+','+str(v_LISTA_SAIDA_18)+','+str(v_LISTA_SAIDA_19)
    """v_LISTA_SAIDA = v_CURSOR_3["id_controle"]
    v_LISTA_SAIDA = v_LISTA_SAIDA + ','+v_CURSOR_3["epidemiological_week"]
    v_LISTA_SAIDA = v_LISTA_SAIDA + ','+v_CURSOR_3["date"]
    v_LISTA_SAIDA = v_LISTA_SAIDA + ','+v_CURSOR_3["order_for_place"]
    v_LISTA_SAIDA = v_LISTA_SAIDA + ','+v_CURSOR_3["state"]
    v_LISTA_SAIDA = v_LISTA_SAIDA + ','+v_CURSOR_3["city"]
    v_LISTA_SAIDA = v_LISTA_SAIDA + ','+v_CURSOR_3["city_ibge_code"]
    v_LISTA_SAIDA = v_LISTA_SAIDA + ','+v_CURSOR_3["place_type"]
    v_LISTA_SAIDA = v_LISTA_SAIDA + ','+v_CURSOR_3["last_available_confirmed"]
    v_LISTA_SAIDA = v_LISTA_SAIDA + ','+v_CURSOR_3["last_available_confirmed_per_100k_inhabitants"]
    v_LISTA_SAIDA = v_LISTA_SAIDA + ','+v_CURSOR_3["new_confirmed"]    
    v_LISTA_SAIDA = v_LISTA_SAIDA + ','+v_CURSOR_3["last_available_deaths"]
    v_LISTA_SAIDA = v_LISTA_SAIDA + ','+v_CURSOR_3["new_deaths"]
    v_LISTA_SAIDA = v_LISTA_SAIDA + ','+v_CURSOR_3["last_available_death_rate"]
    v_LISTA_SAIDA = v_LISTA_SAIDA + ','+v_CURSOR_3["estimated_population_2019"]
    v_LISTA_SAIDA = v_LISTA_SAIDA + ','+v_CURSOR_3["is_last"]
    v_LISTA_SAIDA = v_LISTA_SAIDA + ','+v_CURSOR_3["is_repeated"]
    v_LISTA_SAIDA = v_LISTA_SAIDA + ','+v_CURSOR_3["longitude"]
    v_LISTA_SAIDA = v_LISTA_SAIDA + ','+v_CURSOR_3["latitude"]"""
    ##file.write(v_LISTA_SAIDA_1+','+v_LISTA_SAIDA_2+'\n')
    file.write(str(v_LISTA_SAIDA)+'\n')

file.close()


