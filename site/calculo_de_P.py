####calculo de P#####

valor_inicial=1
N=int(input("\nInforme a quantidade de Termos:"))
x=int(input("\nInforme o valor de X:"))
a=int(input("\nInforme o valor de A:"))

calcula=0
calcula_final=0

for v_loop in range(valor_inicial,N):
	calcula=a*x**v_loop
	print("Parciais:"+str(calcula))
	calcula_final=calcula+calcula_final
print(calcula_final)




