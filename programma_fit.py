import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

print("♢━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━♢")
print("┃            ♣  CUSTOM FIT PPROGRAM   ♣        ┃")
print("┃               (by Tommaso Talli)             ┃")
print("♢━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━♢")
print("\n\n")


#-----------------------------------------------------------------------------Inserimento dati e format
def Choice():
    global file_path

    print("\n"+"━"*51 + "\n")
    # Nome del file da cui leggere i dati
    while True:
        file_path = input("Chose file path: ")
        try:
            open(file_path)
            break
        except FileNotFoundError:
            print("The file path is not present in the directory")
            print("")

    print("")
    print(f"――――――――――――――――――――♣ {file_path} ♣――――――――――――――――――――――")
    print("")
    
    # Errori costanti ?
    print("Set error (sigma_x,sigma_y) constant ? (y/n):")
    choice = input("(y/n) ")
    while choice not in ["y","n"]: choice = input("(y/n) ")
    print("")

    if choice == "y": #Errori costanti
        print("Set an asset:")
        print("0)------------------------------------------------")
        print("  #X constant increase ")
        print("                       ")
        print("       ┃comumn Y┃      ")
        print("1)------------------------------------------------")
        print("      ┃comumn X│comumn Y┃")
        print("2)------------------------------------------------")
        print("      ┃line X   ")
        print("      ┃―――――――――")
        print("      ┃line Y   ")
        print("3)------------------------------------------------")
        print("        #X measurements          Y measurements")
        print("      ┃X_11│X_12┆...┆X_1n┃    ┃Y_11│Y_12┆...┆Y_1N┃")
        print("      ┃X_21│X_22┆...┆X_2n┃    ┃Y_21│Y_22┆...┆Y_2N┃")  
        print("      ┃  ↓    ↓       ↓  ┃    ┃  ↓    ↓       ↓  ┃")
        print("      ┃X_m1│X_m2┆...┆X_mn┃    ┃Y_M1│Y_M2┆...┆Y_MN┃")
        print("")
        print("4)------------------------------------------------")
        print(" #X measurements ↓")
        print("                   ┃X_11│X_12┆...┆X_1n┃")
        print("                   ┃X_21│X_22┆...┆X_2n┃")  
        print("                   ┃  ↓    ↓       ↓  ┃")
        print("                   ┃X_m1│X_m2┆...┆X_mn┃")
        print("")
        print(" #Y measurements ↓")
        print("                   ┃Y_11│Y_12┆...┆Y_1N┃")
        print("                   ┃Y_21│Y_22┆...┆Y_2N┃")
        print("                   ┃  ↓    ↓       ↓  ┃")
        print("                   ┃Y_M1│Y_M2┆...┆Y_MN┃")
        print("---------------------------------------------------")
        print("")
        print("                           (type 'back' to go back)")
        print("")

        while True:
            choice_2 = input("Asset: ")

            while choice_2 not in ["0","1", "2", "3", "4","back"]:
                choice_2 = input("Asset: ")

            if choice_2 == "back":
                print("―"*42,"\n")
                Choice()

            try:
                if choice_2 == "0":
                    Y = np.loadtxt(file_path, unpack=True)  # verticale
                    while True:
                        incr = input("X constant increase : ")
                        a = input("start value : ")
                        try:
                            incr = float(incr)
                            a = float(a)
                            break
                        except ValueError: print("increase values must be numbers")
                    print("")
                    X = np.arange(a, a + len(Y) * incr, incr)[:len(Y)]
                    
                elif choice_2 == "1":
                    X, Y = np.loadtxt(file_path, unpack=True)  # verticale
                elif choice_2 == "2":
                    X, Y = np.loadtxt(file_path)  # orizzontale
                elif choice_2 == "3":  # Media verticale
                    data = np.loadtxt(file_path, delimiter='\t')
                    x_column = int(input("number of x_column : "))
                    X = np.mean(data[:, :x_column], axis=1)
                    Y = np.mean(data[:, x_column:], axis=1)
                    dx = np.std(data[:, :x_column], axis=1)
                    dy = np.std(data[:, x_column:], axis=1)
                else:  # Media orizzontale
                    data = np.loadtxt(file_path, delimiter='\t')
                    x_line = int(input("number of x measurements per point : "))
                    X = np.mean(data[:x_line, :], axis=0)
                    Y = np.mean(data[x_line:, :], axis=0)
                    print("X shape:", X.shape)
                    print("Y shape:", Y.shape)

                    dx = np.std(data[:x_line, :], axis=0)
                    dy = np.std(data[x_line:, :], axis=0)
            
                break

            except ValueError:
                print("Wrong format selected")


        #Caso errori nulli nella media
        if choice_2 in ["3","4"]:
            if np.all(dx) == 0:
                while True:
                    sigma_x = input("Set sigma_x error shape: ")
                    try:
                        dx = np.full(X.shape , float(sigma_x))
                        break
                    except ValueError:
                        print("sigma values must be numbers")
                    
            if np.all(dy) == 0:
                while True:
                    sigma_y = input("Set sigma_y error shape: ")
                    try:
                        dy = np.full(Y.shape , float(sigma_y))
                        break
                    except ValueError:
                        print("sigma values must be numbers")

        #Caso generale (non 3,4)
        else:
            while True:
                sigma_x = input("Set sigma_x error shape: ")
                sigma_y = input("Set sigma_y error shape: ")
                try:
                    dx = float(sigma_x)
                    dy = float(sigma_y)
                    break
                except ValueError:
                    print("sigma values must be numbers")
                
            dx = np.full(X.shape, dx)
            dy = np.full(Y.shape, dy)

            print(len(dx),len(dy))
            


    else:   #Errori non costanti
        print("Set an asset:")
        print("1)    ┃comumn X|comumn sigma_x|comumn Y|comumn sigma_y┃")
        print("2)    ┃comumn X|comumn Y|comumn sigma_x|comumn sigma_y┃")
        print("")
        print("3)    ┃line X|line sigma_x|line Y|line sigma_y┃")
        print("4)    ┃line X|line Y|line sigma_x|line sigma_y┃")
        print("")
        print("                           (type 'back' to go back)")
        print("")
        

        while True:
            choice_2 = input("Asset: ")

            while choice_2 not in ["1", "2", "3", "4","back"]:
                choice_2 = input("Asset: ")
                
            if choice_2 == "back":
                print("―"*42,"\n")
                Choice()
                
            try:
                if choice_2 == "1": X, dx, Y, dy = np.loadtxt(file_path, unpack=True)
                elif choice_2 == "2": X, Y, dx, dy = np.loadtxt(file_path, unpack=True)
                elif choice_2 == "3": X, dx, Y, dy = np.loadtxt(file_path)
                elif choice_2 == "4": X, Y, dx, dy = np.loadtxt(file_path)

                break

            except ValueError:
                print("Wrong format selected")
    return X,Y,dx,dy


def Pregraph(X,Y,dx,dy):
    
    # Grafico preliminare
    plt.clf()
    plt.plot(X,Y,'.',label='Points')
    plt.legend()
    plt.savefig(f'Points_{file_path}.png', format='png')
    print("\nSet of points correctly printed ✅\n")
    print("―"*52)


    # Range di punti da analizzare
    ask = input("\nDo you want to manage the X point range? (y/n): ")

    if ask in ["y","Y"]:
        while True:
            while True:
                x1 = input("X minimum value : ")
                x2 = input("X maximum value : ")
                try:
                    x1 = float(x1)
                    x2 = float(x2)
                    break 
                except ValueError: print("\n invalid values \n")

            a = np.searchsorted(X, x1, side='left')
            b = np.searchsorted(X, x2, side='right')

            X_cut = X[a:b]
            Y_cut = Y[a:b]
            dx_cut = dx[a:b]
            dy_cut = dy[a:b]

            plt.clf()
            plt.plot(X_cut,Y_cut,'.',label='Points')
            plt.legend()
            plt.savefig(f'Points_{file_path}.png', format='png')
            print("\nSet of points correctly printed ✅\n")
        
            ask = input("Are you sure of the selected range (y/n)?")
            if ask in ["y","Y"]:
                break
    else:
        X_cut = X
        Y_cut = Y
        dx_cut = dx
        dy_cut = dy

    return X_cut,Y_cut,dx_cut,dy_cut
        

#------------------------------------------------------------------------------------ Grafico preliminare

def Fit(X,Y,dx,dy,i):
    global fit_func
    global chi_2
    global popt
    global ndof

    
    #-------------------------------------------------------------------------Inserimento simboli e funzione
    # Primo ciclo per chiedere i simboli da usare
    symbols = []
    units = []
    block_cycle = False
    print("Insert popt variables symbols (type 'stop' to stop) : \n")

    while True:
        symbol = input(f"Variable {len(symbols) + 1}: ")

        if symbol == 'stop':
            if len(symbols) > 0:
                print("")
                break
            else:
                print("\nNo fit parameters entered!\n")
                symbols = []
                block_cycle = True

        if block_cycle == False:
            unit = input("Unit: ")
        
            if unit == 'stop':
                if len(symbols) > 0:
                    print("")
                    break
                else:
                    print("\nNo fit parameters entered!\n")
                    symbols = []
                    units = []
                    block_cycle = True

        if block_cycle == False:
            # Verifica della presenza di sole lettere
            if not symbol.isalpha():
                print("Unsupported symbol")
            else:
                # Verifica dell'indipendenza dei simboli (niente simboli esistenti attaccati)
                if any(sym in "".join(symbols) for sym in symbol):
                    print("Do not concatenate two or more existing symbols")
                else:
                    symbols.append(symbol)
                    units.append(unit)

        block_cycle = False
        print("")

  
    #p0 values
    print("-"*50)
    print("Desideri fissare il popt preliminare (p0)")
    p0_choice = input("(y/n): ")                        #Scegliere se fissare dei vincoli sul p0

    if p0_choice == "y":
        P0 = {}
        for symbol in symbols:
            while True:
                p0 = input(f"Enter the value of p0 for the symbol '{symbol}': ")
                try:
                    p0 = float(p0)
                    break
                except ValueError:
                    print("The value of p0 must be a number")
            P0[symbol] = p0
        print(f"\n{P0}")
        
    else: P0 = None

        
    #Fit func
    print("\n","-"*50)
    print("Funzioni disponibili:")
    print("sin(x): seno di x                 cos(x): coseno di x")
    print("tan(x): tangente di x             exp(x): esponenziale di x")
    print("log(x): logaritmo naturale di x   sqrt(x): radice quadrata di x")
    print("abs(x): valore assoluto di x      log(x,n): logaritmo in base n di x")    
    print("")
    print("Costanti disponibili:")
    print("pi: costante matematica pi greco  E: costante matematica di Nepero (e)")
    print("I: unità immaginaria (i)")
    print("-"*50,"\n")


    symbols.insert(0, "x")
    Symbols = []
    for i in symbols:                   #symbols: list of str symbols
       Symbols.append(sp.symbols(i))    #Symbols: list of sympy symbols

    while True:
        f = input(f"Insert the fit function f({symbols}): ")

        #Controllo delle funzioni utilizzate
        try: f = sp.sympify(f)
        except (SyntaxError, TypeError):
            print("Function syntax error\n")
                
        else:
            #Controllo dei simboli utilizzati
            used_symbols = list(f.free_symbols)
            
            count = 0
            for i in used_symbols:
                if not i in Symbols:
                    print(f"'{i}' variable not declared")
                    count = count + 1

            if count == 0 : break
                
    print("\n","-"*52)


    #-----------------------------------------------------------------------------Calcoli del programma
       
    #Derivate
    f_deriv = sp.diff(f , Symbols[0])


    #Lambdify derivate
    f_deriv = sp.lambdify(Symbols,f_deriv)

    #Errori efficaci
    if p0_choice == "y":
        P0 = list(P0.values())
        ev = []
        ev = np.array([(dy[i]**2 + ( f_deriv(X[i], *P0)**2 * dx[i] )  )**(1/2) for i in range(len(X))])

    else: ev = np.array([ (dy[i]) for i in range(len(X))])

    # Errori seguono una distribuzione uniforme?
    print("Uniform distribution:\n")
    print("a) Ruler distribution:            sigma*1/sqrt(12)")
    print("b) Light signal distribution:     sigma*1/sqrt(3)\n")
          
    tipe_x = input("sigma_x follow unifor distribution (y/n) : ")
    tipe_y = input("sigma_y follow unifor distribution (y/n) : ")

    if tipe_x == "y":
        tipe2_x = input("a/b : ")
        while tipe2_x not in ["a","b"]:
            tipe2_x = input("a/b : ")
        if tipe2_x == "a":  dx = dx/np.sqrt(12)
        else: dx = dx/np.sqrt(3)
        print("")
       
        
    if tipe_y == "y":
        tipe2_y = input("a/b : ")
        while tipe2_y not in ["a","b"]:
            tipe2_y = input("a/b : ")
        if tipe2_y == "a":  dy = dy/np.sqrt(12)
        else: dy = dy/np.sqrt(3)
        print("")
        

    # Absolute sigma
    choise_abs = input("\nDo you want to use absolute sigma (y/n) : ")
    if choise_abs == "y": abs_sigma = True
    else: abs_sigma = False

    print("-"*52)
    
    #---------------------------------------------------------------------------------Fit e chi quadro

    #Fit
    
    fit_func = sp.lambdify(Symbols,f)
    for i in range(5):
        try:
            popt, pcov = curve_fit(fit_func, X , Y , p0=P0, sigma=ev , absolute_sigma=abs_sigma, check_finite=False)

        except RuntimeError as e:
            print("\n")
            print("#"*50)
            print(f"Errore durante l'ottimizzazione: {e}")
            print("#"*50)
            Loop()
        except OptimizeWarning as e:
            print("\n")
            print("#"*50)
            print(f"Errore nella stima della covarianza: {e}")
            print("#"*50,"\n")
        
    #check_finite=False: significa che cerca valori di popt finiti (l'algoritmo converge prima)
    
    #Print popt
    print('')
    print('Value of popt:')
    for i, p in enumerate(popt):
        print(f'{Symbols[i+1]}: {p:.3f} ± {pcov[i,i]**0.5:.3f} {units[i]}')

    #Normalized pcov
    diag = np.sqrt(np.diagonal(pcov))
    norm_diag = np.outer(diag, diag)
    norm_pcov = np.round(pcov / norm_diag , decimals=3)
    print(f"\nNormalized pcov:\n{norm_pcov}\n")
    
    #Chi square
    chi_2 = 0
    for i in range(len(X)):
        chi_2 += ( (Y[i] - fit_func(X[i], *popt)) /ev[i] )**2
    print('chi_2 = ',chi_2)
    
    ndof = len(X) - len(popt) - 1       #Valore di aspettazione del chi_2
    print("ndof = ",ndof)
    
    sigma_chi_2 = np.sqrt(2*ndof)
    sigma_chi_2_instrumental = sigma_chi_2*(4/5)    #Uniform distribution
    print("sigma_chi_2 = ", sigma_chi_2)
    print("chi_2_rid = ", chi_2/ndof)


#------------------------------------------------------------------------------------Grafico

def Graph(X,Y,dx,dy,i):
    # Scelta della scala:
    print("-"*40)
    print("\nChoose the scale:\n-linear (lin)\n-logarithmic (log)\n")
    x_scale = input("x scale (lin/log) : ")
    y_scale = input("y scale (lin/log) : ")

    if x_scale=="log":
        dex_max = np.log10(abs(max(X)))
        x_plot = np.logspace(-dex_max, dex_max, 1000)
    else:
        x_plot = np.linspace(min(X)-2*max(dx), max(X)+2*max(dx), 1000)
        
    
    # Grafico dei dati e della curva di fit
    y_plot = fit_func(x_plot, *popt)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [2, 1]})
    ax1.errorbar(X, Y, yerr=dy, xerr=dx, fmt='.', label='Dati')
    ax1.plot(x_plot, fit_func(x_plot, *popt), label='Fit')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.legend()
    ax1.grid(True, which="both", linestyle="--", linewidth=0.5)

    #Scala bilogaritmica
    if x_scale=="log" and y_scale=="log":
        ax1.set_xscale("log")
        ax1.set_yscale("log")
        plt.loglog()
        plt.grid(True, which="both", linestyle="--", linewidth=0.5)

    #Scala semilogaritmica
    if x_scale=="log" and y_scale=="lin":
        ax1.set_xscale("log")

    if x_scale=="lin" and y_scale=="log":
        ax1.set_yscale("log")

    # Grafico dei residui
    residui = Y - fit_func(X, *popt)
    if x_scale=="log": ax2.errorbar(X, residui, yerr=np.log10(dy), fmt='.', label='Residui')
    else: ax2.errorbar(X, residui, yerr=dy, fmt='.', label='Residui')
    
    if x_scale=="log" and y_scale=="lin": ax2.semilogx(X, np.zeros_like(X), 'r--')
    if x_scale=="log" and y_scale=="log": ax2.loglog(X, np.full_like(X, 1), 'r--')

    else : ax2.plot(X, np.zeros_like(X), 'r--')
    
    ax2.set_xlabel('X')
    ax2.set_ylabel('Residui')
    ax2.legend()
    ax2.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig(f'Fit_n{i}_{file_path}.png', format='png')

    print("\nFit correctly printed ✅\n")
    print("―"*52)

#------------------------------------------------------------------------------------

def Fourier_fit(X,Y,dy):
    while True:
        n = input("number of iterations: ")
        w = input("frequency of wave: ")
        ampl = input("aplitude of wave: ")
        offset = input("offset of wave: ")
        try:
            n = int(n)
            w = float(w)
            ampl = float(ampl)
            offset = float(offset)
            break
        except ValueError: print("\nvalues must be numbers\n")
        
    t = sp.symbols('t')
    w_symbols = sp.symbols('w_:{}'.format(n + 1))

    print("\nChoose one of these waveforms:\n")
    print("1) Square waveform     2) Triangle waveform     3) Sawtooth waveform")
    print("")
    wave = input("choise : ")
    while wave not in ["1","2","3","4"]: wave = input("choise : ")
    print("")
    
    f = 0
    #-------------------------- p0
    w0 = [i * w for i in range(1, n + 2)]

    #-------------------------- serie
    if wave == "1":
        for i in range(1, n+1):
            f += (1/(2*i-1)) * sp.sin((2*i -1) * w_symbols[i] * t)
        f = f * ampl * (4/sp.pi) + offset
        
    if wave == "2":
        for i in range(1, n+1):
            f += (-1)**(i-1) * (1/(2*i -1)**2) * sp.sin((2*i - 1) * w_symbols[i] * t)
        f = f * ampl * (8 / (sp.pi**2)) + offset

    if wave == "3":
        for i in range(1, n+1):
            f += (-1)**(i-1) * (1/i) * sp.sin(i * w_symbols[i] * t)
        f = f * ampl * (2/sp.pi) + offset
            
    f = sp.lambdify([t,*w_symbols],f)

    #------------------------------------- Fit
    try:
        popt, pcov = curve_fit(f, X, Y, p0=w0, sigma=dy, check_finite=True)
    except RuntimeError as e:
        print("#"*50)
        print(f"Errore durante l'ottimizzazione: \n {e}")
        print("#"*50,"\n")
        Fourier_fit()
        
    for i in range(n):
        w_i = popt[i]
        print(f"w_{i} = {w_i} ± {pcov[i][i]}")
    
    x_fourier = np.linspace(min(X), max(X), 100)
    y_fourier = f(x_fourier, *popt)

    plt.scatter(X, Y, marker='.', s=1, color='black')
    plt.plot(x_fourier, y_fourier, label=f'Fit Fourier (n={n})')
    plt.legend()

    Wave = {"1":"square_wave","2":"triangle_wave","3":"sawtooth_wave"}
    plt.savefig(f'Fit_{Wave[wave]}.png', format='png')
    print("")
    Loop()

#------------------------------------------------------------------------------------
X,Y,dx,dy = Choice()
X_cut,Y_cut,dx_cut,dy_cut = Pregraph(X,Y,dx,dy)

def Loop():
    i = 1
    while True:
        print("\n\n"+"━"*51 + "\n\n")
        print("              CHOOSE AN OPTION FIT:        ")
        print("")
        print("       ━━━━━━━━━━━━━━━━    ━━━━━━━━━━━━━━━ ")
        print("       ┃ Standard fit ┃    ┃ Fourier fit ┃ ")
        print("       ━━━━━━━━━━━━━━━━    ━━━━━━━━━━━━━━━ ")
        print("           (key A)             (key B)     ")
        print("")

        fit_choice = input("A or B: ")
        while fit_choice not in ["A","B","a","b"]: fit_choice = input("A or B: ")
        print("")
        
        if fit_choice.lower() == "a":
            print("#-#-#-#-# Standard fit #-#-#-#-#")
            Fit(X_cut,Y_cut,dx_cut, dy_cut, i)
            Graph(X_cut,Y_cut,dx_cut,dy_cut,i)

            ask = input("Are you sure about the result of popts? (y/n): ")
            if ask.lower() == "y":
                break

                i += 1
        else:
            print("#-#-#-#-# Fourier fit #-#-#-#-#\n")
            Fourier_fit(X_cut,Y_cut,dy_cut)
            break

Loop()

