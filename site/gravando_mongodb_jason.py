import pymongo
import json

cliente = pymongo.MongoClient("localhost",27017)

bd = client.AULA

json_texto = '{"nome":"November rain","dataLancamento":"1982-10-07","duracao":"3328","artista":{"nome":"Guns and Roses","artista_id":"10"}}'

ins_album = json.loads(json_texto)

bd.albuns.insert(ins_album)

 