from neo4jrestclient.client import GraphDatabase
#db = GraphDatabase("http://localhost:7474", username="Graph1", password="sucra")

#db = GraphDatabase("http://localhost:7474")

db = GraphDatabase("http://localhost:11008/", username=None, password=None, cert_file=None, key_file=None)

#, username="neo4j", password="sucra")
#db = GraphDatabase("http://127.0.0.1:7474/db/data/") #, username="neo4j", password="SUCRA")
#db = GraphDatabase("http://127.0.0.1:7474/C:\app brad\Ciencia de Dados e Big Data\BD - Unidade 4\Caminho_Aplicacao_neo4j\neo4jDatabases\database-dbdee6fc-0eed-4656-a0b2-ae81cddd016e\installation-4.0.3\data\databases\neo4j", username="Graph", password="SUCRA")
#db = GraphDatabase("http://localhost:11004/neo4j", username="Graph1", password="sucra",cert_file="C:\\Program Files\\Neo4j Desktop\\resources\\static\\certificates\\neo4j.cert",key_file="C:\\Program Files\\Neo4j Desktop\\resources\\static\\certificates\\neo4j.key")
#criando nós com labels
user = db.labels.create("Usuario")
u1 = db.nodes.create(name="Bob")
u2 = db.nodes.create(name="Alice")
u3 = db.nodes.create(name="Lea")
u4 = db.nodes.create(name="Ana")
u5 = db.nodes.create(name="Joel")
u6 = db.nodes.create(name="Rafael")
u7 = db.nodes.create(name="Lara")
#bloco de insert
user.add(u1,u2,u3,u4,u5,u6,u7)
#bloco de relacionamento
u1.relationships.create("follows",u2)
u4.relationships.create("follows",u1)
u2.relationships.create("follows",u3)
u2.relationships.create("follows",u5)
u5.relationships.create("follows",u6)
u5.relationships.create("follows",u7)