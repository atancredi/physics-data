import matplotlib.pyplot as plt
import numpy as np

#--------------------------------------------------------------------------------------------------------- Signal modulation
#function for summing 2 signals v1 and v2 with a non-inverting summing amplifier
def Summing(v1,v2,config):
    if (config["R1"]+config["R2"]) == 0 or config["R3"] == 0:
        return "err" #raise exception
    return (v1*(config["R2"]/(config["R1"]+config["R2"]))+v2*(config["R1"]/(config["R1"]+config["R2"])))*(1+(config["R3"]/config["R4"]))

#--------------------------------------------------------------------------------------------------------- Quantum Harmonic Oscillator
def hermite(x, n):
    xi = numpy.sqrt(m*w/hbar)*x
    herm_coeffs = numpy.zeros(n+1)
    herm_coeffs[n] = 1
    return Herm.hermval(xi, herm_coeffs)
  
def stationary_state(x,n):
    xi = numpy.sqrt(m*w/hbar)*x
    prefactor = 1./math.sqrt(2.**n * math.factorial(n)) * (m*w/(numpy.pi*hbar))**(0.25)
    psi = prefactor * numpy.exp(- xi**2 / 2) * hermite(x,n)
    return psi

#--------------------------------------------------------------------------------------------------------- Plotting Functions

