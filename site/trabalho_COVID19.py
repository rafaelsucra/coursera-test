# brincadeira do COVID19

# comando no MongoDb para carregar a base do governo

# mongoimport --authenticationDatabase=admin -u admin -p admin -d COVID19 -c covid19_brasil --type csv --file c:\Temp\covid19.csv --headerline
# mongoimport --authenticationDatabase=admin -u admin -p admin -d COVID19 -c localidade --type csv --file c:\Temp\RELATORIO_DTB_BRASIL_MUNICIPIO_tratada_LONG_LAT_FINAL.csv --headerline

import pymongo as pm
from datetime import datetime

cliente = pm.MongoClient("localhost",27017,username="admin",password="admin")

db = cliente.COVID19

# Chamada do estado
v_ESTADO = input("Digite o estado para ver a quantidade confirmada: ")

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
