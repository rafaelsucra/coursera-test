##Programa de identificacao da media movel para analise de possivel melhoria ou piora em determinada regiao
##Estado e Municipio
##REGRA:
## - O DIA DEVERÁ TER A MÉDIA DE 7 DIAS ATRAS CONTANDO COM ELE
## - 14  DIAS ATRAS E SUA MÉDIA
##COMPARATIVO:
## - SE DIA > DIA-14 E %DIA > 15% => RED
## - SE DIA > DIA-14 E %DIA ENTRE 0% E 15% => YELLOW
## - SE DIA < DIA-14 => GREEN

import subprocess as sp
import operator as op
import pymongo as pm
from datetime import datetime
from datetime import date
import bson
from bson.son import SON

cliente = pm.MongoClient("localhost",27017,username="admin",password="admin")

db = cliente.COVID19

## criando novas collection:
nova_col_est_med_movel = db["covid19_estado_med_movel"]
nova_col_mun_med_movel = db["covid19_municipio_med_movel"]
col_list = db.list_collection_names()
print(col_list)

if "covid19_estado_med_movel" in col_list:
    print("Collection já existe, dropando - covid19_estado_med_movel!!")
    db.covid19_estado_med_movel.drop()
    print("Collection sendo criada - covid19_estado_med_movel!!")
    nova_col_est_med_movel = db["covid19_estado_med_movel"]

if "covid19_municipio_med_movel" in col_list:
    print("Collection já existe, dropando - covid19_municipio_med_movel!!")
    db.covid19_municipio_med_movel.drop()
    print("Collection sendo criada - covid19_municipio_med_movel!!")
    nova_col_mun_med_movel = db["covid19_municipio_med_movel"]

##como mudar string para data
## site onde encontrei comando:
## https://www.tutorialspoint.com/how-to-convert-from-string-to-date-data-type-in-mongodb
## Site abaixo com agregacoes mais dificeis
## https://www.it-swarm.dev/pt/date/agrupar-por-datas-em-mongodb/971920804/
# $gt       => GREATER THEN (maior que). Símbolo tradicional: >
# $gte     => GREATER THEN OR EQUAL (maior ou igual). Símbolo tradicional: >=
# $lt        => LESS THEN (menor). Símbolo tradicional:  < 
# $lte      => LESS THEN OR EQUAL (menor ou igual). Símbolo tradicional: <=
# $ne      => NOT EQUAL (diferente). Símbolos tradicionais: != ou <>
#
# chamar script, para comando mongoDB
"""
db.getCollection('covid19_estado').find().forEach(
    function(data){
        data.DATE = ISODate(data.date);
        db.getCollection('covid19_estado').save(data);}
        );

db.getCollection('covid19_estado').find().forEach(
    function(data){
        data.DT_OCORRENCIA = ISODate(data.date);
        db.getCollection('covid19_estado').save(data);}
        );

db.getCollection('covid19_estado').find().forEach(
    function (elem) {
        db.getCollection('covid19_estado').update(
            {
                _id: elem._id
            },
            {
                $set: {
                    DT_OCORRENCIA_7DIAS: new Date(elem.DT_OCORRENCIA.getTime() - 7*24*60*60000),
                    DT_OCORRENCIA_14DIAS: new Date(elem.DT_OCORRENCIA.getTime() - 14*24*60*60000)
                }
            }
        );
    }
);
"""
#db.getCollection('covid19_estado').find({"_id":ObjectId("5f08779bd88eced0c6b279aa")})

cursor_principal = db.covid19_estado.find({"state":"RJ","date":"2020-07-03"})

for v_CUR_1 in cursor_principal:
    cursor = db.covid19_estado.aggregate_raw_batches({"$match":{"$and":[{ "DATE": {"$gte": v_CUR_1["DATE"] } },{"DATE": {"$lte": v_CUR_1["DT_OCORRENCIA_7DIAS"] } }]} },{"$group": { "_id" : "$state", "sum" : {"$sum": "$last_available_confirmed" } } })
    for v_CUR_2 in cursor:
        print(v_CUR_1["state"]+v_CUR_1["date"]+v_CUR_1["last_available_confirmed"]+v_CUR_2["_id"]+str(v_CUR_2["sum"]))

pipeline = [
...     {"$unwind": "$tags"},
...     {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
...     {"$sort": SON([("count", -1), ("_id", -1)])}
... ]
>>> import pprint
>>> pprint.pprint(list(db.things.aggregate(pipeline)))
[{u'_id': u'cat', u'count': 3},
 {u'_id': u'dog', u'count': 2},
 {u'_id': u'mouse', u'count': 1}]

"""
var dt_ini="2020-07-03";
var dt_14="2020-07-10";

db.getCollection('covid19_estado').aggregate({ $match: {
    $and: [
        { ShippingDate: { $gte: ISODate(dt_ini.valueOf()) } },
        { ShippingDate: { $lte: ISODate(dt_14.valueOf()) } }
    ]
} },
{ $group: { _id : "$state", sum : { $sum: "$last_available_confirmed" } } });

db.getCollection('covid19_estado').aggregate({ $match: {
    $and: [
        { ShippingDate: { $gte: ISODate("2020-07-03") } },
        { ShippingDate: { $lte: ISODate("2020-07-10") } },
        { state: "RJ"}
    ]
} },
{ $group: { _id : "$state", sum : { $sum: "$last_available_confirmed" } } });



v_IND_EST_MED_MOVEL = db.covid19_estado.find({"state":"RJ"})


last_available_confirmed=0

for v_IND_1 in v_IND_EST_MED_MOVEL:
    v_SELETOR = db.covid19_estado.find({"ShippingDate": {"$gte": v_IND_1["DT_OCORRENCIA_7DIAS"],"$lte": v_IND_1["DT_OCORRENCIA"]},"city":v_IND_1["city"]})
    for v_SEL in v_SELETOR:
        #v_DATA_OCORRENCIA = v_IND_1["date"]
        #print(type(v_DATA_OCORRENCIA))
        #v_DATA_OCORRENCIA=v_IND_1["date"]+" 00:00:00"
        #v_DATA_OCORRENCIA_SAIDA=datetime.strptime(v_DATA_OCORRENCIA,'%Y-%m-%d %H:%m:%s').datetime()
        #print(type(v_DATA_OCORRENCIA_SAIDA))
        #v_DATA_OCORRENCIA=dt.date.strftime(v_IND_1["date"], "%Y-%m-%d").date()

        last_available_confirmed = v_SEL["last_available_confirmed"]
        v_PREPARANDO_INSERT_EST_MUN = {
                                        "epidemiological_week" : v_IND_1["epidemiological_week"],
                                        "date" : v_DATA_OCORRENCIA_SAIDA,
                                        "state" : v_IND_1["state"],
                                        "last_available_confirmed" : v_IND_1["last_available_confirmed"],
                                        "confirmados_pais" : v_IND_1["confirmados_pais"],
                                        "indice_confirmado_anterior" : v_IND_1["indice_confirmado_anterior"],
                                        "new_confirmed" : v_IND_1["new_confirmed"],
                                        "confirmados_novo_pais" : v_IND_1["confirmados_novo_pais"],
                                        "indice_novo_confirmado" : v_IND_1["indice_novo_confirmado"],
                                        "last_available_deaths" : v_IND_1["last_available_deaths"],
                                        "mortos_pais" : v_IND_1["mortos_pais"],
                                        "indice_mortes_anterior" : v_IND_1["indice_mortes_anterior"],
                                        "new_deaths" : v_IND_1["new_deaths"],
                                        "mortos_novo_pais" : v_IND_1["mortos_novo_pais"],
                                        "indice_mortes_novas" : v_IND_1["indice_mortes_novas"]
                                    }
        nova_col_est_med_movel.insert_one(v_PREPARANDO_INSERT_EST_MUN)
"""