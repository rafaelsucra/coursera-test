import operator as op
##from subprocess import Popen
import subprocess as sp
import pymongo as pm
from datetime import datetime

cliente = pm.MongoClient("localhost",27017,username="admin",password="admin")

db = cliente.AMAZONIA

"""2020-05"""
db.CARGA_20200512.drop()
db.CARGA_20200513.drop()
db.CARGA_20200514.drop()
db.CARGA_20200515.drop()
db.CARGA_20200516.drop()
db.CARGA_20200519.drop()
db.CARGA_20200520.drop()
db.CARGA_20200521.drop()
db.CARGA_20200522.drop()
db.CARGA_20200523.drop()
db.CARGA_20200526.drop()
db.CARGA_20200527.drop()
db.CARGA_20200528.drop()
db.CARGA_20200529.drop()
db.CARGA_20200530.drop()
db.CARGA_20200602.drop()
db.CARGA_20200603.drop()
db.CARGA_20200604.drop()
db.CARGA_20200605.drop()
db.CARGA_20200606.drop()
db.CARGA_20200609.drop()
db.CARGA_20200610.drop()
db.CARGA_20200611.drop()
db.CARGA_20200612.drop()


"""executa o arquivo .BAT"""
##p = Popen("Executa_carga_AMAZONIA.bat",cwd=r"C:\Temp\AMAZONIA")
##stdout, stderr = p.communicate()
##print(p.returncode) # is 0 if success

##params = [r"C:\Temp\AMAZONIA\Executa_carga_AMAZONIA.bat"]
##saida = sp.list2cmdline(params)
##print(saida)
file = open("C:\\Temp\\INFO_AMAZONIA.txt","a")
program = r'"C:\Temp\AMAZONIA\Executa_carga_AMAZONIA.bat"'
saida = sp.Popen(program)
file.write(saida+'\n')
file.close()

print("Fim da Carga BAT")

##criacao da tabela final

## criando novas collection:
nova_col_1 = db["amazonia_satelite"]
col_list = db.list_collection_names()
print(col_list)

## checagem de das collection
if "amazonia_satelite" in col_list:
    print("Collection já existe, dropando - amazonia_satelite!!")
    db.amazonia_satelite.drop()
    print("Collection sendo criada - amazonia_satelite!!")
    nova_col_1 = db["amazonia_satelite"]

def carga_amazonia (nome):
    for v_nome in nome:
        db.nova_col_1.insert(v_nome)
    return nome

v_CARGA_20200512 = db.CARGA_20200512.find({}) 

carga_amazonia(v_CARGA_20200512)




