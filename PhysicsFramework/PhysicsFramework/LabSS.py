#Script that makes lab reports for Lab Segnali e Sistemi way easier

import pandas as pd
import numpy as np


import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 100


#from scipy.optimize import curve_fit

#from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
#from mpl_toolkits.axes_grid1.inset_locator import mark_inset
#import matplotlib.ticker as mticker


#Suggested frequencies: evenly spaced values of the frequency on the log scale
#useful when measuring the bode diagram of a circuit
def hint_nu(join):
    try:
        join
    except NameError:
        join = []

    return np.sort(np.hstack((np.logspace(1,2.8, 4, base=10).round(-1),np.logspace(2.8,5.5, 20,base=10).round(-1)[1:],join)).astype(int)).tolist()

#Calculate values for plotting the bode diagram
def BodeCalculations(vout, vin, freq, deltat):

    #calculate the module of the transfer function
    module = vout[0]/vin[0]
    freq_act = freq[0]*10**3
    deltat_act = deltat[0]*(10**-6)  #us
    delta_phi = ((2*np.pi*freq_act*deltat_act)*(180/np.pi))
    sigma_freq = np.around((freq[0]*10**3)*0.03, 3)
    rel_freq = sigma_freq/freq[0]
    sigma_vin = np.around(vin[0]*0.03,2)
    rel_vin = sigma_vin/vin[0]
    sigma_vout = np.around(vout[0]*0.03,2)
    rel_vout = sigma_vout/vout[0]
    sigma_deltat = np.around(deltat[0]*0.03,3)
    rel_deltat = sigma_deltat/deltat[0]
    
    sigma_module = rel_vin + rel_vout
    sigma_deltaphi = (rel_deltat + rel_freq)

#Plot the bode diagram from a raw dataset
def Bode(vout, vin, freq, deltat, mode):
    
    
    if(mode != "nograph"):
        plt.figure(LabSS.CreateFigure())
        plt.xscale("log")
        plt.scatter(freq[0]*10**3,20*np.log(module), label="Dati raccolti")
        plt.axhline(-3, color="red", label="-3dB")
        plt.axvline(1008.88, label="$\\nu_C$ teorica", color="green")
        plt.legend()
        plt.xlabel("$\\nu$ (Hz)")
        plt.ylabel("Attenuazione (dB)")
        plt.grid()
        plt.title("Diagramma di Bode, Funzione di trasferimento")
        
        plt.figure(LabSS.CreateFigure())
        plt.xscale("log")
        plt.scatter(freq_act, delta_phi, label="Dati raccolti")
        plt.xlabel("$\\nu$ (Hz)")
        plt.grid()
        plt.axhline(-45, label="- 45°", color="red")
        plt.axvline(1008.88, label="$\\nu_C$ teorica", color="green")
        plt.ylabel("Sfasamento (Deg)")
        plt.legend()
        plt.title("Diagramma di Bode, fase")
    
    return module, sigma_module, delta_phi, sigma_deltaphi


##########################################################à
#Useful functions for plotting with matplotlib
def CreateFigure():
    return len(plt.get_fignums())