import pymongo

cliente = pymongo.MongoClient("localhost",27017)

bd = client.AULA

album1 = bd.albuns.find_one({"nome":"Somewhere Far Beyond"})

album1 = bd.albuns.find_one({"nome":"November rain"})

name = album1["artista"]["nome"]

print(name)

name_id = album1["artista"]["artista_id"]

print(name_id)