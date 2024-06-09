from flask import Flask, request, send_file
app = Flask(__name__)

import json
import os
from io import BytesIO

import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
mpl.rcParams['figure.dpi'] = 100
import matplotlib.pyplot as plt


#######################
## MAIN POST REQUEST ##
#######################

@app.route('/', methods=['POST'])
def main():

    try:
        #filling the data and settings objects
        data = []
        settings = {}
        if request.method == 'POST':
            settings = json.loads(request.form["settings"])
            for key in request.form:
                if key != "settings":
                    data.append(np.array(json.loads(request.form[key])))
    
        #plot the data
        return testPlot(data[0],data[1])
    

        return json.dumps(data)
    except Exception as e:
        return str(e)

    

########################
## PLOTTING FUNCTIONS ##
########################

#test plot function
def testPlot(data1,data2):
    plt.plot(data1,data2)
    figfile = BytesIO()
    plt.savefig(figfile, format='png')

    return send_file(
        figfile,
        mimetype='image/png',
        #as_attachment=True,
        attachment_filename='graph.png')