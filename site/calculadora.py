#######CALCULADORA########

v_fazer=int(input("\nDigite 1 para numeros inteiros e 2 para numeros com decimais"))

if v_fazer==1:
	v_valor_1=int(input("\nDigite o primeiro numero inteiro:"))
	v_valor_2=int(input("\nDigite o segundo numero inteiro:"))
	v_operacao=int(input("\nDigite a operacao (1)soma-(2)subtracao-(3)multiplicacao-(4)divisao:"))
	if v_operacao==1:
		saida=v_valor_1+v_valor_2
		print(saida)
	elif v_operacao==2:
		saida=v_valor_1-v_valor_2
		print(saida)
	elif v_operacao==3:
		saida=v_valor_1*v_valor_2
		print(saida)
	elif v_operacao==4:
		if v_valor_2==0:
			print("\nValor Não Divisivel por ZERO:")
		elif v_valor_2>0:
			saida=v_valor_1/v_valor_2
			print(saida)
elif v_fazer==2:
	v_valor_1=float(input("\nDigite o primeiro numero decimal:"))
	v_valor_2=float(input("\nDigite o segundo numero decimal:"))
	if v_operacao==1:
		saida=v_valor_1+v_valor_2
		print(saida)
	elif v_operacao==2:
		saida=v_valor_1-v_valor_2
		print(saida)
	elif v_operacao==3:
		saida=v_valor_1*v_valor_2
		print(saida)
	elif v_operacao==4:
		if v_valor_2==0:
			print("\nValor Não Divisivel por ZERO:")
		elif v_valor_2>0:
			saida=v_valor_1/v_valor_2
			print(saida)
else:
	saida=0
	print("\nDigitou numero invalido:")

