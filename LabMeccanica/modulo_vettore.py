import numpy as np

componenti = int(input("Quante componenti ha il vettore? "))
i = 0
j = 0
vettore = np.empty((int(componenti),1))

while i < componenti:
    inn = input("Componente "+(str(i+1))+": ")
    vettore[i] = float(inn)
    inn = 0
    i += 1
    
moduloquadro = 0
while j < componenti:
    moduloquadro += np.power(vettore[j], 2)
    j += 1

modulo = np.sqrt(moduloquadro)
print(modulo)
