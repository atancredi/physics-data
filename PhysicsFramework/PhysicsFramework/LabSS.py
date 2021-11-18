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

#Unpack the raw dataSet to get the columns
def unpack_dataSet(dataSet, errorType, dataType):
    if errorType == "values":
        if dataType == "raw":
            return dataSet["freq"][0], dataSet["vin"][0], dataSet["vout"][0], dataSet["deltat"][0]
        elif dataType == "calculated":
            return dataSet["module"][0], dataSet["deltaphi"][0]
    elif errorType == "errors":
        if dataType == "raw":
            return dataSet["freq"][1], dataSet["vin"][1], dataSet["vout"][1], dataSet["deltat"][1]
        elif dataType == "calculated":
            return dataSet["module"][1], dataSet["deltaphi"][1]
    else:
        return 0

#Calculate values for plotting the bode diagram
def calc_dataSet(dataSet):

    #get the data from the dataSet
    freq, vin, vout, deltat = unpack_dataSet(dataSet, "values", "raw")

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

    return dataSet

#Plot the bode diagram from a dataset
def PlotBode(dataSet):

    #unpack data values
    freq, vin, vout, deltat = unpack_dataSet(dataSet, "values", "raw")
    module, deltaphi = unpack_dataSet(dataSet, "values", "calculated")

    plt.figure(CreateFigure())
    plt.xscale("log")
    plt.scatter(freq,20*np.log(module), label="Dati raccolti")
    plt.axhline(-3, color="red", label="-3dB")
    plt.axvline(1008.88, label="$\\nu_C$ teorica", color="green")
    plt.legend()
    plt.xlabel("$\\nu$ (Hz)")
    plt.ylabel("Attenuazione (dB)")
    plt.grid()
    plt.title("Diagramma di Bode, Funzione di trasferimento")
        
    plt.figure(CreateFigure())
    plt.xscale("log")
    plt.scatter(freq, deltaphi, label="Dati raccolti")
    plt.xlabel("$\\nu$ (Hz)")
    plt.grid()
    plt.axhline(-45, label="- 45°", color="red")
    plt.axvline(1008.88, label="$\\nu_C$ teorica", color="green")
    plt.ylabel("Sfasamento (Deg)")
    plt.legend()
    plt.title("Diagramma di Bode, fase")

    plt.show()

#Compare the bode diagrams for 2 dataSets
def BodeCompare(dataSets):

    freq1, vin1, vout1, deltat1 = unpack_dataSet(dataSets[0], "values", "raw")
    module1, deltaphi1 = unpack_dataSet(dataSets[0], "values", "calculated")

    freq2, vin2, vout2, deltat2 = unpack_dataSet(dataSets[1], "values", "raw")
    module2, deltaphi2 = unpack_dataSet(dataSets[1], "values", "calculated")

    fig = plt.figure(CreateFigure())
    ax1 = fig.add_subplot()
    plt.xscale("log")
    plt.axhline(-3, color="red", label="-3dB")
    plt.axvline(1008.88, label="$\\nu_C$ teorica", color="green")
    plt.legend()
    plt.xlabel("$\\nu$ (Hz)")
    plt.ylabel("Attenuazione (dB)")
    plt.grid()
    plt.title("Diagramma di Bode, Funzione di trasferimento")
    ax1.scatter(freq1,20*np.log(module1), marker="o",label="Dati per K=2.5")
    ax1.scatter(freq2,20*np.log(module2), marker="o", color="blue", label="Dati per K circa 1.6")


    fig = plt.figure(CreateFigure())
    ax2 = fig.add_subplot()
    plt.xscale("log")
    plt.xlabel("$\\nu$ (Hz)")
    plt.grid()
    plt.axhline(-45, label="- 45°", color="red")
    plt.axvline(1008.88, label="$\\nu_C$ teorica", color="green")
    plt.ylabel("Sfasamento (Deg)")
    plt.legend()
    plt.title("Diagramma di Bode, fase")
    ax2.scatter(freq1, deltaphi1, label="Dati per K=2.5")
    ax2.scatter(freq2, deltaphi2,  marker="o", color="blue", label="Dati per K circa 1.6")

    plt.show()

#Export the latex table of all the data passing through a Pandas dataFrame


##########################################################
#Useful functions for plotting with matplotlib
def CreateFigure():
    return len(plt.get_fignums())