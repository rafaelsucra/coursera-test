numero=int(input("\nDigite um numero interiro:"))

numero_final=numero+10

print("Numero Inicial:" + str(numero))

print("Numero Final:" + str(numero_final))

saida=0

for v_cal in range(numero,numero_final):
	ant=saida
	saida=v_cal
	armazena=saida+ant
	print(armazena)

v_total=0

for v_calcula in range(1,11):
	v_num=int(input("\nDigite o seu "+ str(v_calcula) +":"))
	v_recebe=v_num
	v_total=v_recebe+v_total

print("Valor final:"+ str(v_total))