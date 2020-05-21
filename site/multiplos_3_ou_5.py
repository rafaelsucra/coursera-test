import numpy as np
import pandas as pd

v_ENTRADA = int(input("Digite um valor, para identificar multiplos de um numero: "))
v_MULTIPLO_1 = int(input("Digite o primeiro numero: "))
v_MULTIPLO_2 = int(input("Digite o segundo numero: "))

lista_archive_1 = []
lista_archive_2 = []
lista_archive_1_2 = []

for v_loop in range(1,v_ENTRADA):
    if v_loop % v_MULTIPLO_1 == 0:
        lista_archive_1.append(v_loop)
    if v_loop % v_MULTIPLO_2 == 0:
        lista_archive_2.append(v_loop)
    if (v_loop % v_MULTIPLO_1 == 0) and (v_loop % v_MULTIPLO_2 == 0):
        lista_archive_1_2.append(v_loop)

print("Multiplos de 1 a {} divisivel por {} => {}".format(v_ENTRADA,v_MULTIPLO_1,lista_archive_1))
print("Multiplos de 1 a {} divisivel por {} => {}".format(v_ENTRADA,v_MULTIPLO_2,lista_archive_2))
print("Multiplos de 1 a {} divisivel por {} e {} => {}".format(v_ENTRADA,v_MULTIPLO_1,v_MULTIPLO_2,lista_archive_1_2))

