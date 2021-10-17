import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 100

def init_figure():
    fig = len(plt.get_fignums())
    plt.figure(fig)

def save_figures():
    for i in plt.get_fignums():
        plt.figure(i)
        plt.savefig('figure%d.png' % i)

#plot bode diagrams of a transfer function
def bode_diagram(v_in,v_out,delta_t,freq):
    #function that plots the module
    def bode_module(v_out,v_in,freq):

        #initialize the figure
        init_figure()
        module = v_out[0]/v_in[0]
        plt.xscale("log")
        plt.scatter(freq[0],20*np.log(module), label="dati raccolti")
        plt.axhline(-3, color="red", label="-3dB")
        plt.axvline(71050, label="$\\nu_C$ teorica", color="green")
        plt.legend()
        plt.xlabel("$\\nu$ (Hz)")
        plt.ylabel("Attenuazione (dB)")
        plt.grid()
        plt.title("Diagramma di Bode, Funzione di trasferimento")
        return module

    #function that plots the phase
    def bode_phase(freq,delta_t):
    
        delta_t[0] = delta_t[0]*(10**-6)  #us
        delta_phi = ((2*np.pi*freq[0]*delta_t[0])*(180/np.pi))

        init_figure()
        plt.xscale("log")
        plt.scatter(freq[0], delta_phi, label="Dati raccolti")
        plt.ylim(0,99)
        plt.xlabel("$\\nu$ (Hz)")
        plt.grid()
        plt.axhline(45, label="45°", color="red")
        plt.axvline(71050, label="$\\nu_C$ teorica", color="green")
        plt.ylabel("Sfasamento (Deg)")
        plt.legend()
        plt.title("Diagramma di Bode, fase")

        return delta_phi
    
    #generation of the pandas dataFrame
    def dataFrame(freq,v_in,v_out,module,delta_t,delta_phi):
        data = [freq[0]/1000,v_in[0],v_out[0],module,delta_t[0]*(10**6),delta_phi]

        #FUNCTION THAT TRANSLATES THE DATA
        def DataTraslator(data):
            finaldata = []
            i = 0
            while i < buff:
                row = []
                for j in data:
                    row.append(j[i])
                finaldata.append(row)
                i += 1
            return finaldata

        #check on the sizes
        buff = 0
        flag = 0
        for i in data:
            if buff == 0:
                buff = i.size
            elif i.size != buff:
                flag = 1
                break
        if flag == 1:
            return "The data arrays must all have the same dimension" #throw exception for god's sake

        #traslate the data
        DataTraslator(data)

        df = pd.DataFrame(np.array(finaldata),
                            columns=[freq[1],v_in[1],v_out[1],"|T(\u03C9)|",delta_t[1],"\u0394\u03C6"])
        return df.sort_values(by=[freq[1]])

    module = bode_module(v_out,v_in,freq)
    delta_phi = bode_phase(freq,delta_t)
    
    #return the dataframe
    return dataFrame(freq,v_in,v_out,module,delta_t,delta_phi)

#scatter plot of amperes over volts in the diode
def diode(V_r,V_d,R_d):
    I = V_r/R_d

    init_figure()
    plt.scatter(V_D,I)
    plt.grid()

#Partitore resistivo
R1 = [1004.5, 1004.4]
R2 = [2209.3, 2209.7]

#CR Passa-Alto
v_in = [np.array([3.11,3.06,3,2.87,2.8,2.7,2.644,2.619,2.594,2.5937,2.72]),"Vin(V)"] #v
v_out = [np.array([0.1,0.2925,1.06,1.7,2.094,2.19,2.275,2.462,2.55,2.55,2.1]),"Vout(V)"]  #v
freq = [np.array([1,5.07,20,40,60,80,100,200,500,1000,71.7])*(10**3),"Frequenza (kHz)"] #kHz
delta_t = [np.array([266,49.6,10,3.5,1.94,1.04,0.74,0.18,0.028,0.01,1.3]),"\u03BCs"]

#diodo
R_d = 680
#V_in_d = np.array([.2,.4,.5,.6,.7,.8,.9,.75])
V_D = np.array([201.3,400,478,525,557,579,595,565,-12.2,-58.5,-108.5,-209.12,-407,-609,-802])*(10**(-3))
V_r = np.array([0.12,5.73,31.5,79.4,147.3,225,304.5,181.6,2.2,9.7,0,0,0,0,0])*(10**(-3))

bode_results = bode_diagram(v_in,v_out,delta_t,freq)

print(bode_results.to_latex(index=False))

diode(V_r,V_D,R_d)

plt.show()

