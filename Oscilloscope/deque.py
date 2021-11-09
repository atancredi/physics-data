from collections import deque
import csv
import matplotlib
import matplotlib.pyplot as plt


maxlen = 20
window = deque(maxlen=maxlen)
window2 = deque(maxlen=maxlen)

with open('data/scope_21.csv') as f_input:
    csv_input = csv.reader(f_input)
    header = next(csv_input)

    freq = [[],[]]
    x_axis = []

    print("start cycle")
    for x,v1,v2 in csv_input:
        try:
            x = float(x)
            v1 = float(v1)
            v2 = float(v2)
        except ValueError:
            print(x+" - "+v1+" - "+v2)
            continue
    
        window.append(v1)
        window2.append(v2)
        if (len(window) == maxlen) and (len(window2) == maxlen) and (len(window) == len(window2)):
            

            first = window[0]
            last = window[-1]
            
            first2 = window2[0]
            last2 = window2[-1]
            if ((last2-first2) > -2e-9):
                
                if first != last:
                    freq[0].append(maxlen / ((last - first)))
                else:
                    freq[0].append(0)

                if first2 != last2:
                    freq[1].append(maxlen / ((last2 - first2)))
                else:
                    freq[1].append(0)

                x_axis.append(x)

            else:
              continue

    plt.plot(x_axis, freq[0], 'b-')
    plt.plot(x_axis, freq[1], 'r-')
    plt.show()
