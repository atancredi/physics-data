import signals as s
import matplotlib.pyplot as plt
import numpy as np

config = { #dati dell'esperienza 4 di labss
    "R1": 100200,
    "R2": 100200,
    "R3": 2175,
    "R4": 4331
}

#Discretized space
dx = 0.05
x_lim = 12
x = np.arange(-x_lim,x_lim,dx)

plt.figure()
plt.plot(x, s.Summing(s.stationary_state(x,4), s.stationary_state(x,32), config))
#plt.xlabel(r"x")
#plt.ylabel(r"$\psi_4(x)$")
#plt.title(r"Test Plot of $\psi_{"+str(sstate)+"}(x)$")
plt.show()