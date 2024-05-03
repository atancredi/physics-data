import  numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Set measurement unit for mu and sigma (for text inside plot)
MEASUREMENT_UNIT = "nm"

def gaussiana(x,x0,b,c,sigma):
    return c * np.exp(-((x-x0)**2/(2*sigma**2))) + b

x = np.array([])
y = np.array([])
sigma_y = np.array([])

# Set initial parameters: mu, b, c, sigma
mu_0 = 0
sigma_0 = 0
b_0 = 0 #offset
c_0 = 1 #scale

# Fit parameters
popt, pcov = curve_fit(gaussiana, x, y, p0 = (mu_0,b_0,c_0,sigma_0), sigma=sigma_y)
perr = np.sqrt(np.diag(pcov))

# Print parameters in terminal with errors
print(f"x0: {popt[0]} +- {perr[0]}")
print(f"b: {popt[1]} +- {perr[1]}")
print(f"c: {popt[2]} +- {perr[2]}")
print(f"sigma: {popt[3]} +- {perr[3]}")

# Plot the gaussian line
xfit = np.linspace(popt[0] - 6*popt[3], popt[0] + 6*popt[3], 100)
yfit = gaussiana(xfit,popt[0],0,1,popt[3])

fig, ax = plt.subplots()
ax.errorbar(x, y,sigma_y,fmt=".")
ax.plot(xfit,yfit)

# Add dashed vertical line on mu value
# plt.vlines(popt[0],0,max(yfit),linestyles="dashed",colors="black")
# plt.text(popt[0]+0.1,0.01,f"$x_0=589.1nm$")

# Add style to the plot
plt.xlabel()
plt.ylabel()

# Write gaussian best fit parameters directly on the plot
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
textstring = f"$\mu = ({round(popt[0],2)}\pm{round(perr[0],2)}){MEASUREMENT_UNIT}$\n"+\
    f"$\sigma = ({round(popt[3])}\pm{round(perr[3])}){MEASUREMENT_UNIT}$"

ax.text(0.6, 0.95, textstring, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', bbox=props)


plt.show()
