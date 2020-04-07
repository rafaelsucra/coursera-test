import pymongo

cliente = pymongo.MongoClient("localhost",27017)

db_estudo = cliente.ESTUDO

truck = db_estudo.truck.find({"eventType":"Overspeed"})

file_truck = open("C:\\Temp\\ROUTE_NAME.txt","a")

for t in truck:
	nome_rota = t["routeName"]
	file_truck.write(nome_rota+'\n')

file_truck.close()

teste = db_estudo.truck.find({"eventType" : "Overspeed"})

for temp in teste:
    file = open("C:\\Temp\\ROTA_SAIDA.txt","a")
    nome_rota = temp["routeName"]
    print(nome_rota)
    file.write(nome_rota+'\n')
    file.close()



