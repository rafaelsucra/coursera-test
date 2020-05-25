show dbs

// comando de criacao de usuário
use admin

// comando de criacao de usuario
db.createUser(
    {
    user: "admin",
    pwd: "admin",
    roles: [ "userAdminAnyDatabase",
             "dbAdminAnyDatabase",
             "readWriteAnyDatabase"]
    }
   )

// apos criar o ambiente:
use admin

db.auth("admin", "admin" )

mongo admin -u admin -p admin
// colocar auth=banco admin -u=usuario e -p=password
mongoimport --authenticationDatabase=admin -u admin -p admin -d COVID19 -c localidade --type csv --file c:\Temp\Sedes_Coordenadas_Municipios.csv --headerline


use AULA

db.albuns.insert({})

db.albuns.insert({"nome": "The Dark Side of the Moon", "data": new Date(1973, 3, 29)})
db.albuns.insert({"nome": "Master of Puppets", "dataLancamento": new Date(1986, 2, 3), "duracao": 3286})
db.albuns.insert({"nome": "...And Justice for All", "dataLancamento": new Date(1988, 7, 25), "duracao": 3929})
db.albuns.insert({"nome": "Among the Living", "produtor": "Eddie Kramer"})
db.albuns.insert({"nome": "Nevermind", "artista": "Nirvana", "estudioGracavao": ["Sound City Studios", "Smart Studios (Madison)"], "dataLancamento": new Date(1992, 0, 11)})
db.albuns.insert({"nome": "Reign in Blood", "dataLancamento": new Date(1986, 9, 7), "artista": "Larry Carroll", "duracao": 1738})
db.albuns.insert({"nome": "Seventh Son of a Seventh Son", "artista": "Iron Maiden", "produtor": "Martin Birch", "estudioGracavao": "Musicland Studios", "dataLancamento": new Date(1988, 3, 11)})

db.albuns.find().pretty()

db.albuns.find({"nome": "Seventh Son of a Seventh Son"}).pretty()

db.albuns.find({"artista": "Nirvana"}).pretty()

db.albuns.find({"dataLancamento":{ $gt:new Date(1986, 9, 8)}}).pretty()

db.albuns.find({"dataLancamento":{ $gte:new Date(1986, 9, 8)}}).pretty()

db.albuns.find({"dataLancamento":{ $lt:new Date(1986, 9, 8)}}).pretty()

db.albuns.find({"dataLancamento":{ $lte:new Date(1986, 9, 8)}}).pretty()

db.albuns.find({"nome": /of/}).pretty()

db.albuns.remove({"_id" : ObjectId("5e873dea5a05df5ef2ac6acf")})

show dbs

show collections

db.albuns.update({"nome":"Among the Living"}, {$set : {"duracao": 3013}})

db.albuns.find({"nome" : /Among/}).pretty()

db.albuns.find({"duracao": {"$in":[1738,3286]}}).pretty()

db.albuns.find( { artista: "IRON MAIDEN" } ).collation( { locale: "en_US", strength: 1 } ).pretty()

db.albuns.find({$and : [{"dataLancamento" : {$gte : new Date(1986, 0, 1)}},{"dataLancamento" : {$lt : new Date(1987, 0, 1)}}]}).pretty()

db.artista.insert([{"nome": "Metallica","id": "1"},{"nome": "Megadeath","id":"2"},{"nome": "Slayer","id":"3"},{"nome": "Anthrax","id":"4"},
{"nome": "Iron Maiden","id":"5"},{"nome": "Nirvana","id":"6"},{"nome": "Pink Floyed","id":"7"}])

db.albuns.update({"nome":"Master of Puppets"},{$set:{"artista_id":"1"}})
db.albuns.update({"nome":"Among the Living"},{$set:{"artista_id":"4"}})
db.albuns.update({"nome":"Nevermind"},{$set:{"artista_id":"6"}})
db.albuns.update({"nome":"Reign in Blood"},{$set:{"artista_id":"3"}})
db.albuns.update({"nome":"Seventh Son of a Seventh Son"},{$set:{"artista_id":"5"}})
db.albuns.update({"nome":"...And Justice for All"},{$set:{"artista_id":"1"}})
db.albuns.update({"nome":"The Dark Side of the Moon"},{$set:{"artista_id":"7"}})

var artista = db.artista.findOne({"nome" : "Metallica"})

artista

var albuns = db.albuns.find({"artista_id" : artista.id})

albuns

db.albuns.insert({"nome":"Somewhere far Beyond", "dataLancamento": new Date(1992, 5, 30),"duracao": 3328, "artista":{"nome":"Blind Guardian"}})

db.albuns.insert({"nome":"Imagination from the Other Side", "dataLancamento": new Date(1995, 3, 4),"duracao": 2958, "artista":{"nome":"Blind Guardian"}})

db.albuns.update({"nome":"Imagination from the Other Side"}, {$set : {"artista":{"artista_id": "8"}})

db.artista.insert({"nome":"Blind Guardian", "id":"8"})

db.albuns.find({"artista": {"nome":"Blind Guardian"}})

db.albuns.find({"duracao":{"$range":[0,9999]}})

--pacote de instalacao do Python no MongoDB
pip install pymongo

db.albuns.find({$and:[{"duracao": {$gte : 0}},{"duracao":{$lte : 9999}}]}).pretty()

db.albuns.find({"duracao":{"$gte":0}})

--importando csv
-- estudo -> BD
-- driver -> collections

mongoimport -d estudo -c driver --type csv --file c:\Temp\drivers.csv --headerline

use estudo

show collections

mongoimport -d estudo -c timesheet --type csv --file c:\Temp\timesheet.csv --headerline

mongoimport -d estudo -c truck --type csv --file c:\Temp\truck_event_text_partition.csv --headerline

1) nome das rotas que estão com Overspeed

db.truck.find({"eventType":"Overspeed"}).pretty()

-- programa Python
programa_mongodb_caminhao.py

2) nome da rota, caminhao, motorista e CNH

--programa Python
programa_mongodb_rota_caminhao_motorista.py

3) ID motorista, name, ssn, sendo q eventos diferentes de Normal

