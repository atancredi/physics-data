#Bode diagrams with python

import numpy as np
import matplotlib.pyplot as plt
import control

def PassaAlto_Trasferimento():

    def fTrasf(R,C):
        return control.tf([C*R,0],[C*R,1])

    mag,phase,omega = control.bode(fTrasf(207,10.28*(10^(-9))), Hz=True)

    # find the cross-over frequency and gain at cross-over
    wc = np.interp(-180.0,np.flipud(phase),np.flipud(omega))
    Kcu = np.interp(wc,omega,mag)

    plt.tight_layout()
    ax1,ax2 = plt.gcf().axes     # get subplot axes
    plt.sca(ax1)                 # magnitude plot
    plt.sca(ax2)                 # phase plot
    plt.show()

def PassaAlto_Misure():
    v_in = np.array([3.11,3.06,3,2.87,2.8,2.7,2.644,2.619,2.594,2.5937,2.72]) #v
    v_out = np.array([0.1,0.2925,1.06,1.7,2.094,2.19,2.275,2.462,2.55,2.55,2.1])  #v
    delta_t = np.array([266,49.6,10,3.5,1.94,1.04,0.74,0.18,0.028,0.01,1.3])  #us
    freq = np.array([1,5.07,20,40,60,80,100,200,500,1000,71.7]) #kHz
    delta_phi = 2*np.pi*freq*delta_t

PassaAlto()