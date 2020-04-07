lista_materiais=['caderno','e-book','livro','lapis','caneta','estojo']

print(lista_materiais)

lista_materiais.append('mochila')

print(lista_materiais.index('mochila'))

posicao=lista_materiais.index('mochila')

print(posicao)

lista_materiais.sort()

print(lista_materiais)

print(len(lista_materiais))

lista_materiais.remove('e-book')

print(lista_materiais)

for material in lista_materiais:
	print(material)

for valor in range(1,5):
	print(valor)

numeros=list(range(1,6))

print(numeros)

for v_numeros in numeros:
	print(v_numeros)	

quadrados=[]

for valor in range(1,11):
	quadrado=valor ** 2
	quadrados.append(quadrado)

print(quadrados)

materiais = [1 , 2 , 3 , 4]
objetos = materiais
objetos.append(5)
print(materiais)
print(objetos)

for i in range(2,4):
	print("Tabuada do "+ str(i))
	for j in range(0,11):
		print(str (j) + " "+ str(j * i))