from py2neo import Graph , Node, Relationship

bd = Graph("localhost", auth=('neo4j','sucra'))

op = bd.begin()

#criacao da label e o registro
u1 = Node("Usuario",name="Bob")
u2 = Node("Usuario",name="Alice")
u3 = Node("Usuario",name="Lea")
u4 = Node("Usuario",name="Ana")
u5 = Node("Usuario",name="Joel")
u6 = Node("Usuario",name="Rafael")
u7 = Node("Usuario",name="Lara")

op.create(u1)
op.create(u2)
op.create(u3)
op.create(u4)
op.create(u5)
op.create(u6)
op.create(u7)

#for i in range(1,7):
#    text = "u"+str(i)
#    op.create(text)

#criando o relacionamento
r1 = Relationship(u1,"follows",u2)
r2 = Relationship(u4,"follows",u1)
r3 = Relationship(u2,"follows",u3)
r4 = Relationship(u2,"follows",u5)
r5 = Relationship(u5,"follows",u6)
r6 = Relationship(u5,"follows",u7)

op.create(r1)
op.create(r2)
op.create(r3)
op.create(r4)
op.create(r5)
op.create(r6)

op.commit()