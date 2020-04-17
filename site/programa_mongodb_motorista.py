import pymongo

cliente = pymongo.MongoClient("localhost",27017)

db_estudo = cliente.ESTUDO

truck = db_estudo.truck.find({"eventType" : {$ne:"Normal"}}) --não reconheceu o $ne

truck = db_estudo.truck.find()

lista_nomes = []

for temp in truck:
	evento = temp["eventType"]
	if evento != "Normal":
		dr = temp["driverId"]
		print(str(dr)+'\n')
		cam = db_estudo.driver.find({"driverId" : dr})
		nome_rota = temp["routeName"]
		id_truck = temp["truckId"]
		for temp2 in cam:
			id_driver = temp2["driverId"]
			ssn = temp2["ssn"]
			nome_piloto = temp2["name"]
			lista_nomes.append(nome_piloto+" - "+str(id_driver)+" - "+str(ssn))

file = open("C:\\Temp\\INFO_PILOTO.txt","a")
lista=list(set(lista_nomes))
fim=sorted(lista_nomes)

for t in lista:
    saida = t
    file.write(saida+'\n')
    
file.close()

