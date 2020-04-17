--comandos Neo4j

--Craindo Nós

CREATE(dylan:Musico {nome : "Bob Dylan", data_de_nascimento : '1941-05-24'})

CREATE(b:Musico{nome:"Bob Marley", data_de_nascimento:'1945-02-06'})

CREATE(hendrix:Musico {nome : "Jimmy Hendrix"})

CREATE(al_along:Musica{ nome : "All Along the Watchtower"})

create(bm:Musica{nome : 'Is this Love'})

create(bm:Musica{nome : 'One Love'})

create(f:festivel{nome : "rock in rio"})

create(f:festivel{nome : "Festival of Unity no Harvard Stadium in Boston"})

--Criando Arestas
MATCH(hendrix:Musico{nome : "Jimmy Hendrix"}),(al_along:Musica {"All Along the Watchtower"})

MATCH (hendrix:Musico{nome : "Jimmy Hendrix"}),(al_along:Musica {nome : "All Along the Watchtower"})
CREATE(hendrix)-[r:GRAVOU]->(al_along)


MATCH (bob:Musico{nome : "Bob Dylan"}),(al_along:Musica {nome : "All Along the Watchtower"})
CREATE(bob)-[r:GRAVOU]->(al_along)
CREATE(bob)-[s:COMPOS]->(al_along)


--CONSULTA
MATCH(m:Musico) RETURN m.nome

MATCH(m:Musico) RETURN m

MATCH(m) RETURN m

MATCH(m) WHERE m.nome = "Bob Dylan" RETURN m

MATCH(m:Musico{nome : "Bob Dylan"}) RETURN m

MATCH(m) WHERE m.nome = "Bob Dylan" RETURN m.nome

MATCH(n1)-[]-() RETURN (n1)

MATCH(n1)-[]->() RETURN (n1)

MATCH()-[]-(n1) RETURN (n1)

MATCH()-[]->(n1) RETURN COUNT(n1)

MATCH(n1:Musico)-[r]->(n2:Musica) RETURN n1, Type(r), n2

MATCH(n1:Musico)-[r:GRAVOU]->(n2:Musica) RETURN n1, Type(r), n2

MATCH (b:Musico{nome : "Bob Marley"}),(m:Musica {nome : "One Love"})
CREATE(b)-[r:GRAVOU]->(m)
CREATE(b)-[s:COMPOS]->(m)

MATCH (b:Musico{nome : "Bob Marley"}),(m:Musica {nome : "Is this Love"})
CREATE(b)-[r:GRAVOU]->(m)
CREATE(b)-[s:COMPOS]->(m)

MATCH (b:Musico{nome : "Bob Marley"}),(m:festivel {nome : "rock in rio"})
CREATE(b)-[r:COMPARECEU]->(m)

MATCH (b:Musico{nome : "Bob Marley"}),(m:festivel {nome : "Festival of Unity no Harvard Stadium in Boston"})
CREATE(b)-[r:COMPARECEU]->(m)
CREATE(b)-[t:CANTOU]->(m)
CREATE(b)<-[s:RECEBEU_PREMIO]-(m)

MATCH (b:Musico{nome : "Jimmy Hendrix"}),(m:festivel {nome : "rock in rio"})
CREATE(b)-[r:COMPARECEU]->(m)
CREATE(b)-[t:CANTOU]->(m)

MATCH (b:Musico{nome : "Jimmy Hendrix"}),(m:festivel {nome : "Festival of Unity no Harvard Stadium in Boston"})
CREATE(b)-[r:COMPARECEU]->(m)
CREATE(b)-[t:CANTOU]->(m)

MATCH (b:Musico{nome : "Bob Dylan"}),(m:festivel {nome : "rock in rio"})
CREATE(b)-[r:COMPARECEU]->(m)
CREATE(b)-[t:CANTOU]->(m)

MATCH (b:Musico{nome : "Bob Dylan"}),(m:festivel {nome : "Festival of Unity no Harvard Stadium in Boston"})
CREATE(b)-[r:COMPARECEU]->(m)
CREATE(b)-[t:CANTOU]->(m)

--excluindo e atualizando:
MATCH(hendrix:Musico {nome : "Jimmy Hendrix"}) 
SET hendrix.data_de_nascimento='1942-11-27' 
RETURN hendrix

MATCH(hendrix:Musico {nome : "Jimmy Hendrix"}) 
SET hendrix.data_de_nascimento=null
RETURN hendrix

MATCH(bob:Musico{nome : "Bob Dylan"})-[r]-()
RETURN bob, Type(r)

MATCH(bob:Musico{nome : "Bob Dylan"})-[r]-()
delete r

MATCH(bob:Musico {nome : "Bob Dylan"}) 
delete bob

--DELETA O BD TODO
MATCH(n)
OPTIONAL MATCH (n)-[rel]-()
DELETE rel,n

--dropando os INDEX
drop index on :Product(productID)
drop index on :Category(categoryID)
drop index on :Supplier(supplierID)

--Passo a passo de importar do CSV no Neo4j

--leu arquivo e print as linhas do arquivo:
LOAD CSV WITH Headers
FROM "file:///composicoes.csv"
as linha
return linha

LOAD CSV WITH Headers
FROM "file:///composicoes.csv"
AS linha
merge (compositor:Musico{nome: linha.compositor})
merge (musica:Musica{nome : linha.musica})
merge (compositor)-[:COMPOS]->(musica)

LOAD CSV WITH Headers
FROM "file:///gravacoes.csv"
AS reg
merge(i:Musico{nome: reg.interprete})
merge(m:Musica{nome: reg.musica})
merge(i)-[:GRAVOU]->(m)

--base ja carregada, podemos fazer algumas consultas:
match(i:Musico)-[g:GRAVOU]->(m:Musica)
return i, Type(g),m

match(i:Musico)-[g:GRAVOU]->(m:Musica)
match(c:Musico)-[h:COMPOS]->(m:Musica)
return i,m,c

--import csv de uma base relacional:

LOAD CSV
WITH HEADERS FROM "file:///products.csv"
AS row
CREATE (n:Product)
SET n = row,
n.unitPrice    = toFloat(row.unitPrice),
n.unitsInStock = toInteger(row.unitsInStock), 
n.unitsOnOrder = toInteger(row.unitsOnOrder),
n.reorderLevel = toInteger(row.reorderLevel),
n.discontinued = (row.discontinued <> "0")

LOAD CSV
WITH HEADERS FROM "file:///categories.csv" 
AS row
CREATE (n:Category)
SET n = row

LOAD CSV
WITH HEADERS FROM "file:///suppliers.csv" 
AS row
CREATE (n:Supplier)
SET n = row

CREATE INDEX ON :Product(productID)
CREATE INDEX ON :Category(categoryID)
CREATE INDEX ON :Supplier(supplierID)

MATCH (p:Product),(c:Category)
WHERE p.categoryID = c.categoryID
CREATE (p)-[:PART_OF]->(c)

match(p:Product),(s:Supplier)
where p.supplierID = s.supplierID
CREATE (s)-[:SUPPLIES]->(p)

--Realizando algumas consultas: Listar as categorias de produtos fornecidas por cada fornecedor.
MATCH(s:Supplier)-->(:Product)-->(c:Category)
RETURN s.companyName as Company, collect(distinct c.categoryName) as Categories

--Encontrar um fornecedor de cada produto
MATCH(c:Category {categoryName:"Produce"})<--(:Product)<--(s:Supplier)
RETURN DISTINCT s.companyName as ProduceSuppliers

MATCH(c:Category)<--(:Product)<--(s:Supplier)
RETURN s.companyName as Company, collect(distinct c.categoryName) as Categories

--PYTHON e Neo4j

pip install neo4j-driver

pip install neo4jrestclient

--IDE - pycharm ou visual studio code






