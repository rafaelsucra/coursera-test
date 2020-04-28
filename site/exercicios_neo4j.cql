#Exercicios Unidade 4 neo4j:

--capturar filmes lançados apartir de 90

match(filme90:Movie) where filme90.released >= 1990 return (filme90)

--capturar pessoas do filme Cloud Atlas:

match(filme90:Movie)-[]-(pessoa:Person) 
where filme90.released >= 1990 
return (pessoa.name)

--seria todos atributos da Label Pessoa:
match(filme90:Movie)-[]-(pessoa:Person) 
where filme90.released >= 1990 
return (pessoa)

--Achando filmes do kevin Bacon:
match(f:Movie)-[r]-(p:Person)
where p.name = "Kevin Bacon"

--Achando filmes de Kevin bacon apenas com 3 saltos:
match(f:Movie)-[r]-(p:Person)-[r1]-(f1:Movie)-[r2]-(p1:Person) 
where p.name = "Kevin Bacon"
return f,Type(r),p,Type(r1),f1,Type(r2),p1

--Caminho mais curto de relacionamento de Kevin Bacon com Meg Ryan:
match(f:Movie)-[r]-(p:Person)
where p.name = "Kevin Bacon"
Return f,Type(r),p

match(f:Movie)-[r]-(p:Person)
where p.name = "Meg Ryan"
Return f,Type(r),p

match(f:Movie)-[r]-(p:Person{name : "Kevin Bacon"})-[r1]-(f1:Movie)-[r2]-(p1:Person{name : "Meg Ryan"})

match(f:Movie)-[r]-(p:Person)-[r1]-(f1:Movie)-[r2]-(p1:Person{name : "Meg Ryan"}) 
return f,Type(r),p,Type(r1),f1,Type(r2),p1

match(f:Movie)-[r]-(p:Person{name:"Tom Hanks"})-[r1]-(f1:Movie)-[r2]-(p1:Person{name : "Meg Ryan"}) 
return f,Type(r),p,Type(r1),f1,Type(r2),p1

match(f:Movie)-[r]-(p:Person{name : "Tom Hanks"})-[r1]-(f1:Movie)-[r2]-(p1:Person)
where p1.name = "Meg Ryan"
return f,Type(r),p,Type(r1),f1,Type(r2),p1

match(p:Person{name:"Kevin Bacon"})-[r]-(f:Movie)-[r1]-(p1:Person{name:"Meg Ryan"}) 
return p,Type(r),f,Type(r1),p1

match(p:Person{name:"Tom Hanks"})-[r]-(f:Movie)-[r1]-(p1:Person{name:"Meg Ryan"}) 
return p,Type(r),f,Type(r1),p1