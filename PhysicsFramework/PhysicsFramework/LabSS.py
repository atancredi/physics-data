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

##########################################################
#Configuration

oscilloscope_error = 0.03 #uncertainty when reading the oscilloscope

##########################################################
#Core program

#Suggested frequencies: evenly spaced values of the frequency on the log scale
#useful when measuring the bode diagram of a circuit
def hint_nu(join):
    try:
        join
    except NameError:
        join = []

    return np.sort(np.hstack((np.logspace(1,2.8, 4, base=10).round(-1),np.logspace(2.8,5.5, 20,base=10).round(-1)[1:],join)).astype(int)).tolist()

#Create the dataset from the direct data
def dataSet(freq, vin, vout, deltat):
    return {
        "freq": [freq,None],
        "vin": [vin,None],
        "vout": [vout,None],
        "module": [None,None],
        "deltat": [deltat,None],
        "deltaphi": [None, None]
        }


#Unpack the dataSet to get the columns
def unpack_dataSet(dataSet, type):
    if type == "values":
        return dataSet["freq"][0], dataSet["vin"][0], dataSet["vout"][0], dataSet["deltat"][0]
    elif type == "errors":
        return dataSet["freq"][1], dataSet["vin"][1], dataSet["vout"][1], dataSet["deltat"][1]
    else:
        return 0

#Calculate values for plotting the bode diagram
def BodeCalculations(dataSet):

    #get the data from the dataSet
    freq, vin, vout, deltat = unpack_dataSet(dataSet, "values")

    #scalate the data (measurement-unit-wise)
    freq = freq*10**3
    deltat = deltat[0]*(10**-6)  #us

    #calculate the uncertainty on the acquired data based on the specs from the oscilloscope
    sigma_freq = freq*oscilloscope_error
    rel_freq = sigma_freq/freq

    sigma_vin = vin*oscilloscope_error
    rel_vin = sigma_vin/vin

    sigma_vout = vout*oscilloscope_error
    rel_vout = sigma_vout/vout

    sigma_deltat = deltat*oscilloscope_error
    rel_deltat = sigma_deltat/deltat

    #calculate the module of the transfer function, with its error
    module = vout/vin
    sigma_module = rel_vin + rel_vout

    #calculate the phase difference between vin and vout, with its error
    delta_phi = ((2*np.pi*freq*deltat)*(180/np.pi))
    sigma_deltaphi = (rel_deltat + rel_freq)

    #put the data inside the dataSet and return it
    dataSet["freq"][1] = sigma_freq
    dataSet["vin"][1] = sigma_vin
    dataSet["vout"][1] = sigma_vout
    dataSet["deltat"][1] = sigma_deltat
    dataSet["module"][0] = module
    dataSet["module"][1] = sigma_module
    dataSet["deltaphi"][0] = delta_phi
    dataSet["deltaphi"][1] = sigma_deltaphi

#Plot the bode diagram from a dataset
def Bode(dataSet):
    
    
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


##########################################################
#Useful functions for plotting with matplotlib
def CreateFigure():
    return len(plt.get_fignums())