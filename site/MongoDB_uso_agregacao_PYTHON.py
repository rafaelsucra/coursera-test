import operator as op

import pymongo as pm
from datetime import datetime

from bson.son import SON
import pprint as pp

cliente = pm.MongoClient("localhost",27017,username="admin",password="admin")

db = cliente.COVID19

## trecho abaixo testando:

nova_col_mun_est = db["covid19_mun_est"]
col_list = db.list_collection_names()
print(col_list)

if "covid19_mun_est" in col_list:
    print("Collection já existe, dropando - covid19_mun_est!!")
    db.covid19_mun_est.drop()
    print("Collection sendo criada - covid19_mun_est!!")
    nova_col_mun_est = db["covid19_mun_est"]



## v_RECEBE = db.covid19_geral_municipio.aggregate([{"$lookup": {"from" : "covid19_estado","localField" : ("state","date"),"foreignField" : ("state","date"),"as" : "municipio_estado" }},{"$out": "covid19_mun_est"}])

v_RECEBE = db.covid19_geral_municipio.aggregate([{"$match":{"date": "2020-06-06","state":"RJ"}},{"$lookup":{"from" : "covid19_estado","localField" : ("state","date"),"foreignField" : ("state","date"),"as" : "municipio_estado"}}])

print("FEZ")


