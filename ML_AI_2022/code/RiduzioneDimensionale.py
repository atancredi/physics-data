#code
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

RiduzioneDimensionale(X_ising,{
    'figsize': {
      'a': 15,
      'b': 5  
    },
    'subplots': [
      {
          'subplot': {
              'a': 1,
              'b': 2,
              'c': 1
          },
          'color': T_ising,
          'colormap': 'hot',
          'labels': {
              'colorbar': 'Temperature',
              'xlabel': '$PCA_0$',
              'ylabel': '$PCA_1$'
          }
      },
      {
          'subplot': {
              'a': 1,
              'b': 2,
              'c': 2
          },
          'color': Y_ising,
          'colormap': 'tab10',
          'labels': {
              'colorbar': 'Classe',
              'xlabel': '$PCA_0$',
              'ylabel': '$PCA_1$'
          }
      },
    ]
  },{
      'algo': 'pca',
      'n_components': 10 #istanza PCA con n componenti = 10
  })