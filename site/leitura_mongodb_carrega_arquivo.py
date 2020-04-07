import pymongo

client = pymongo.MongoClient("localhost",27017)

db = client.AULA

albuns = db.albuns.find()

file_out = open("C:\\Temp\\albuns.TXT","a")

for item in albuns:
    id_nome=item["id"+" - "+"nome"]
    file_out.write(id_nome+'\n')

 file_out.close()

albuns1 = db.albuns.find({"duracao":{"$gte":0}})

 for item1 in albuns1:
    nome = item1["nome"]
    dur = str(item1["duracao"])
    n_d = nome+ " - "+dur
    file_saida = open("C:\\Temp\\saida_temp.txt","a")
    file_saida.write(n_d+'\n')
    file_saida.close()