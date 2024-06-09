#cambiare le costanti
#i file dat si devono chiamare pallinometro-n.dat dove n è il numero (1 <= n <= infinito)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy import stats
import pandas as pd
import math
from scipy import interpolate
from scipy.stats import binom

#costanti
N_misure = 200
nlineelist = [5, 5, 5, 25, 25, 25, 50, 50, 50] #lista dei numeri di righe
plist = [0.05, 0.25, 0.5, 0.05, 0.25, 0.5, 0.05, 0.25, 0.5] #lista delle probabilità impostate per ciascun esperimento
delimitatore = '\t' #delimitatore per i valori dat (al momento è una tablatura)
chi2values = [11.070, 11.070, 11.070, 37.652, 37.652, 37.652, 67.505, 67.505, 67.505] #i 9 valori limite per la validità del chi quadro

#ciclo principale
i = 1
while i <= len(nlineelist):
    #carico i dati dal file
    data1 = np.genfromtxt('misure/pallinometro-'+str(i)+'.dat',
                     skip_header=0,
                     skip_footer=0,
                     names=True,
                     dtype=None,
                     delimiter=delimitatore)

    
    j = 0
    col1, col2, col3 = [], [], []

    #sottociclo principale
    while j < len(data1):
        #popolo un'array con i valori estratti dal file dat, parsati
        splitted = str(data1[j]).split(",")
        temp1 = splitted[0].replace('(','')
        temp2 = splitted[1].replace(' ','')
        temp3 = splitted[2].replace(')','')
        temp3bis = temp3.replace(' ','')
        col1.append(float(temp1)) #numero della misura (non serve)
        col2.append((float(temp2))) #y
        col3.append(float(temp3bis)) #m
        
        #ripristino le variabili per l'iterazione successiva
        splitted = []
        temp1, temp2, temp3, temp3bis = "","","",""
        
        j += 1 #incremento il contatore
    
    #Disegno l'istogramma
    xmin = 0
    nlinee = nlineelist[(i-1)]
    xmax = nlinee+1
    Nbins= xmax-xmin
    y, bins, patches= plt.hist(col2,bins=Nbins,range=(xmin-0.5,xmax-0.5),label="Data")
    
    
    #CALCOLO LA DISTRIBUZIONE BINOMIALE
    p = plist[(i-1)]
    n = nlineelist[(i-1)]
    x = list(range(0,(int(nlineelist[(i-1)])+1)))
    l = 1
    
    bn = binom.pmf(x, n, p)
    binomm = (bn)*N_misure
    
    #Calcolo l'errore sulla binomiale
    step1 = bn * np.subtract(1, bn)
    step2 = step1 * N_misure
    sigma_bin = np.sqrt(step2)
    
    #Disegno la binomiale
    plt.errorbar(x,
             binomm,
             yerr=sigma_bin,
             marker='o',markersize=3,linestyle='none',label="Previsione")
    
    #finisco di disegnare il grafico
    title = str(nlineelist[(i-1)])+" file di chiodi. Probabilità del "+str(int(plist[(i-1)]*100))+"%"
    plt.xlabel("Tasca",fontsize=13)
    plt.ylabel("Occorrenze",fontsize=13)
    plt.legend(fontsize=13)
    plt.title(title,fontsize=13)
    plt.savefig("data/"+str(i)+".png")
    plt.clf()
    
    #Calcolo la probabilità di successo supponendo che sia la media della colonna Y diviso il numero di righe
    mmean = np.mean(np.asarray(col2))
    probsuccesso = mmean/nlineelist[(i-1)]
    
    #Calcolo l'errore sulla probabilità di successo
    sigmap = probsuccesso/(math.sqrt(N_misure) * math.sqrt(Nbins))
    
    #Eseguo test del chi quadro
    chi2 = (np.square(y-binomm))/np.square(sigma_bin)
    showchi2 = np.sum(chi2)
    
    #Stampo
    print ("passo: "+str(i))
    print ("1 - Salvo su file l'istogramma")
    print ("2 - La probabilità di successo è "+str(probsuccesso))
    print ("( Errore associato alla probabilità di successo: "+str(sigmap)+" )")
    print ("3 - Test del Chi Quadro:")
    print (showchi2)
    #stampo la validità del chi2
    print ("Validità del test")
    if showchi2 < chi2values[(i-1)]:
        print (str(showchi2)+" < "+str(chi2values[(i-1)])+" : valido")
    else:
        print (str(showchi2)+" > "+str(chi2values[(i-1)])+" : non valido")


    #ripristino le variabili per la prossima iterazione
    xmin, xmax, nlinee, mylambda, Nbins = "","","","",""
    data1, col1, col2, col3, x, = [], [], [], [], []
    j = 0
    probsuccesso, showchi2 = "",""
    chi2 = []
    binomm = []
    
    i += 1 #incremento il contatore

print ("Fine esecuzione del codice")
