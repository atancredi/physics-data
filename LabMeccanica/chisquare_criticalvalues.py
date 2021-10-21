from scipy.stats import chi2
print("Gradi di libertà:")
dfin = input("(valore maggiore o uguale di 1): ")
print("Accettazione:")
pin = input("(90, 95 o 99 - valori percentuali): ")

# define probability
p = int(pin)/100
# retrieve value <= probability
value = chi2.ppf(p, int(dfin))
print(value)
# confirm with cdf
pconf = chi2.cdf(value, int(dfin))
print(pconf)
