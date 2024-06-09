import numpy as np
def hint_nu():
	# Frequenze suggerite:
	print(np.logspace(1,2.8, 4, base=10).round(-1))
	print(np.logspace(2.8,5.5, 20,base=10).round(-1)[1:])
	print(np.logspace(5.5, 6, 3,).round(-4)[1:])