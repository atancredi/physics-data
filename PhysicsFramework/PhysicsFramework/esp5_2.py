import pandas as pd
import numpy as np

import LabSS

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
import matplotlib.ticker as mticker

import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 100

#import pylatexenc.latexencode as pltx

#frequenze suggerite con aggiunta delle frequenze intorno a quella di taglio aspettata
print(LabSS.hint_nu([500,750,800,950,1000,1050,1100,1150,1300,1500]))

#
#   Presa Dati
#

freq1 = np.hstack((np.array([9.625,26.15,39.931,60.762,98.36,157.3,306.06,496.5,564.28,629.15,755.00,886.20,938.86])*10**-3,
                   np.array([1.0580,1.215,1.3025,1.5008,1.6158,2.2816,3.2393,4.4964,6.246]))) #kHz
vin1 = np.array([0.980,0.96,0.98,0.98,0.98,0.96,0.96,0.96,0.96,0.96,0.96,0.96,1.01,0.98,0.96,0.98,0.96,1.01,0.96,0.98,0.98,0.96])
vout1 = np.array([2.27,2.27,2.27,2.27,2.29,2.29,2.43,2.73,2.93,3.14,3.62,4.00,4.00,3.58,2.65,2.21,1.51,1.25,0.58,0.34,0.22,0.16])
deltat1 = -1*np.array([35,35,120,56,86,128,93.04,105.8,119.44,122.9,153.6,206.1,221.6,262.96,277.8,283.2,267.92,256.8,186.96,139.74,108.29,78.78])

freq2 = np.hstack((np.array([9.927,27.06,40.96,59.78,93.05,156.94,302.4,499.4,563.8,621,755.7,885.3,959])*10**-3,
                 np.array([1.0638,1.2105,1.3191,1.4880,1.6224,2.2875,3.2337,4.8730,6.170,8.4460,11.672,14.642])))
vin2 = np.array([0.95,0.95,0.96,0.95,0.95,0.96,0.96,0.95,0.96,0.96,0.96,0.95,0.96,0.96,0.95,0.95,0.96,0.96,0.96,0.95,0.96,0.96,0.96,0.95,0.95])
vout2 = np.array([0.95,0.95,0.95,0.95,0.93,0.93,0.9,0.84,0.810,0.8,0.75,0.7,0.68,0.64,0.59,0.56,0.52,0.5,0.39,0.29,0.2,0.16,0.13,0.09,0.08])
deltat2 = -1*np.array([100,124,152,144,167,166.4,159.2,158.4,153.6,154.4,148.8,141.6,132.8,135.2,122.37,118.88,111.42,107.5,89.44,71.14,53.31,44.45,34.98,27.716,24.854])

#scale the data to match the base I.S. measurement unit
freq1 = freq1*10**3 #from kHz to Hz
deltat1 = deltat1*(10**-6)  #from us to s

freq2 = freq2*10**3 #from kHz to Hz
deltat2 = deltat2*(10**-6)  #from us to s

#create the dataSets from the raw data
dataSet1 = LabSS.dataSet(freq1, vin1, vout1, deltat1)
dataSet2 = LabSS.dataSet(freq2, vin2, vout2, deltat2)

print(LabSS.calc_dataSet(dataSet1))
print(LabSS.calc_dataSet(dataSet2))

#LabSS.PlotBode(dataSet1)
LabSS.BodeCompare([dataSet1,dataSet2])

#
#   Fine Presa Dati
#

def dataFrame(freq,v_in,v_out,delta_t):
    
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
        
        
        
        #calcolo i dati indiretti ed i sigma
        module, sigma_module, delta_phi, sigma_deltaphi = printGraph(v_out, v_in, freq, delta_t, "nograph")
        #sigma_freq = np.around((freq[0])*0.03, 3)
        sigma_freq = (freq[0])*0.03
        rel_freq = sigma_freq/freq[0]
        
        #sigma_vin = np.around(v_in[0]*0.03,2)
        sigma_vin = v_in[0]*0.03
        rel_vin = sigma_vin/v_in[0]
        
        #sigma_vout = np.around(v_out[0]*0.03,2)
        sigma_vout = v_out[0]*0.03
        rel_vout = sigma_vout/v_out[0]
        
        #sigma_deltat = np.around(delta_t[0]*0.03,3)
        sigma_deltat = delta_t[0]*0.03
        rel_deltat = sigma_deltat/delta_t[0]
        
        data = [freq[0],v_in[0],v_out[0],module,delta_t[0],delta_phi]
        
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
        traslated = DataTraslator(data)
        
        #array of the column heads
        colheads = [freq[1],v_in[1],v_out[1],"|T(\u03C9)|",delta_t[1],"\u0394\u03C6"]
        
        df = pd.DataFrame(np.array(traslated),
                            columns=colheads)
        
        df = df.sort_values(by=[freq[1]])
        
        #errori = [np.around(sigma_freq,3).tolist(),np.around(sigma_vin,3).tolist(),
        #          np.around(sigma_vout,3).tolist(),np.around(sigma_module,3).tolist(),
        #          np.around(sigma_deltat,3).tolist(),np.around(sigma_deltaphi,3).tolist()]
        errori = [sigma_freq,sigma_vin,sigma_vout,sigma_module,sigma_deltat,sigma_deltaphi]
        datafinale = []
        outercnt = 0
        
        while outercnt < len(data):
            print(colheads[outercnt])
            
            #studying = np.around(df.iloc[:,outercnt],6).tolist()
            studying = df.iloc[:,outercnt]
            
            
            cnt = 0
            buffer = []
            for row in studying:
                sx = row
                dx = errori[outercnt][cnt]
                
                #controllo scaling kHz per le frequenze
                kflag = 0
                varswitch = 0
                if "Frequenza" in colheads[outercnt]:
                    if sx < 1:
                        sx = sx*10**3
                        dx = dx*10**3
                        kflag = 1
                    else:
                        varswitch = 1
                else:
                    roundfactor = 3
                    sx = np.round(sx, roundfactor)
                    dx = np.round(dx, roundfactor)
                    varswitch = 2
                
                
                #controllo cifre significative
                sx_cifre = len(str(sx).split(".")[1])
                dx_cifre = len(str(dx).split(".")[1])
                if sx_cifre > dx_cifre:
                    #innercnt = 0
                    #dxtmp = str(dx)
                    #while innercnt < (sx_cifre-dx_cifre):
                    #    dxtmp += "0"
                    #    innercnt += 1
                    #dx = float(dxtmp)
                    sx = np.around(sx,dx_cifre)
                elif sx_cifre < dx_cifre:
                    #sx = np.round(sx,dx_cifre)
                    dx = np.around(dx,sx_cifre)
                
                
                
                
                
                if varswitch == 0:
                    var = "§§§("+str(sx)+"@@@"+str(dx)+")§§§"
                elif varswitch == 1:
                    var = "§§§("+str(sx)+"@@@"+str(dx)+")k§§§"
                elif varswitch == 2:
                    var = "§§§("+str(sx)+"@@@"+str(dx)+")§§§"
                
                buffer.append(var)
                cnt+=1
            datafinale.append(buffer)
            outercnt += 1
        
        df2 = pd.DataFrame(DataTraslator(datafinale), columns=colheads)
        
        return df2

#df1 = dataFrame(freq1,vin1,vout1,deltat1)
#print(df1.to_latex(index=False).replace("rrrrrr","|c|c|c|c|c|c|").replace("@@@","\pm").replace("§§§","$"))


#df2 = dataFrame(freq2,vin2,vout2,deltat2)
#print(df2.to_latex(index=False).replace("rrrrrr","|c|c|c|c|c|c|").replace("@@@","\pm").replace("§§§","$"))