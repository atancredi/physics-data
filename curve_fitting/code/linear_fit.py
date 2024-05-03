import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Raccolta dati
x = np.array([])
y = np.array([])
sigma_y = np.array([])
    
# definisco una funzione di linearità
def line(x, m, c):
    return m*x+c

popt,pcov=curve_fit(line,x,y,sigma=sigma_y)
y_fit_L=line(x,popt[0],popt[1])
plt.plot(x, y_fit_L,color="orange",label="fit")
plt.plot(x, y, "o")
plt.xlabel("X")
plt.ylabel("Y")

print(f"a: {popt[0]}")
print(f"b: {popt[1]}")