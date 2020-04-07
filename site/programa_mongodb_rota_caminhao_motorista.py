import pymongo

cliente = pymongo.MongoClient("localhost",27017)

db_estudo = cliente.ESTUDO

truck = db_estudo.truck.find({"eventType" : "Overspeed"})

for temp in truck:
    print("inicio")
    dr = temp["driverId"]
    print(str(dr)+'\n')
    cam = db_estudo.driver.find({"driverId" : dr})
    file = open("C:\\Temp\\ROTA_CAMINHAO_PILOTO.txt","a")
    nome_rota = temp["routeName"]
    id_truck = temp["truckId"]
    for temp2 in cam:
        id_driver = temp2["driverId"]
        ssn = temp2["ssn"]
        final=nome_rota+" - "+str(id_truck)+" - "+str(id_driver)+" - "+str(ssn)
        print(final)
        file.write(final+'\n')
        

