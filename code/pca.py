import pandas as pd 
import numpy as np 
import pickle
from pathlib import Path

import pandas as pd
import numpy as np

from sklearn.decomposition import PCA

from scipy.stats import zscore

import seaborn as sns
import matplotlib.pyplot as plt

#from limmpca.util import correct_scale
#from limmpca.mixedmodel import (parallel_mixed_modelling,
#                                effect_matrix_decomposition,
#                                variance_explained,)
#from limmpca.bootstrap import bootstrap_limmpca

# TODO : Differentiate these results based on a) control  vs ASD, b) 0-back 1 back

def varimax(Phi, gamma = 1, q = 20, tol = 1e-6):
    from numpy import eye, asarray, dot, sum, diag
    from numpy.linalg import svd
    p,k = Phi.shape
    R = eye(k)
    d=0
    for _ in range(q):
        d_old = d
        Lambda = dot(Phi, R)
        u,s,vh = svd(dot(Phi.T,asarray(Lambda)**3 \
        - (gamma/p) * dot(Lambda, diag(diag(dot(Lambda.T,Lambda))))))
        R = dot(u,vh)
        d = sum(s)
        if d/d_old < tol: break
    return dot(Phi, R)


def correct_scale(data, labels):
    # correct each subject by used scale range
    for id in np.unique(data.subnum):
        id_idx = data['subnum'].str.match(id)
        cur = data[id_idx].loc[:, labels].values
        scling = np.max(cur.flatten())
        floor = np.min(cur.flatten())
        cur = (cur - floor) / scling
        # update
        data[id_idx].loc[:, labels] = cur
    return data


# use the top three for dev
## n_componant = 3 due to knee of scree plot 
n_components = 3
pca_varimax = "; raw"
varimax_on = False
bootstrap_n = 2000

# set random seed
np.random.seed(42)

#import data 
path = '/Users/willstrawson/Documents/PhD/adie_ongoingthoughts/data/mw_data/processed_data/perprobe.csv'
data = pd.read_csv(path)

# Some columns have loads of NaN values -  create dataframe of summaries 
nans = pd.DataFrame(data.isna().sum()) 
# rename column for .loc
nans.columns = ['n_nans']   
# Which MW questions had no nans - add to list keepcols
keepcols = nans.loc[nans['n_nans'] == 0].index.tolist()  
# remove these columns from original data
data = data[keepcols]

# Get MWQ labels 
labels = data.columns.tolist()[:-3]    
# get everything in the same scale - redundent 
data = correct_scale(data, labels)
data = data.reset_index(drop=True)


# Separate data here into groups 

data = data.loc[data['']]
# SPSS PCA was performed on correlation matrix
# so we z-score the input data
X = data.loc[:, labels].values
Xz = zscore(X)

# Run pca
pca = PCA(svd_solver='full').fit(Xz)

# scree plot
plt.figure()
plt.plot(pca.explained_variance_ratio_ * 100, "-o")
plt.xticks(ticks=range(13),
           labels=range(1, 14))
plt.ylabel("explained variance (%)")
plt.title("Scree plot")

plt.show()

# calculate principle component scores
#TODO ; understand this 
if n_components:
    scores = pca.transform(Xz)[:, :n_components]
    pc = pca.components_[:n_components, :]
else:
    scores = pca.transform(Xz)
    pc = pca.components_
    n_components = pc.shape[0]

if varimax_on:
    from limmpca.util import varimax
    pc = varimax(pc.T).T
    scores = np.dot(Xz, pc.T)
    pca_varimax = "; varimax"

# heatmap 
plt.matshow(pc.T, cmap="RdBu_r", vmax=0.7, vmin=-0.7)
plt.xticks(ticks=range(n_components),
           labels=range(1, n_components + 1))
plt.yticks(ticks=range(len(labels)),
           labels=labels)
plt.title("Principle components" + pca_varimax)
plt.colorbar()
plt.show()
# add per run factor score for each row of original dataframe and save as pca_res
pca_res = data.loc[:,:].copy()
m_components = scores.shape[-1]
for i in range(scores.shape[-1]):
    pca_res[f"factor_{i + 1}"] = scores[:, i]

# scatter plot assessing relationship between factor scores 
plt.figure()
sns.scatterplot("factor_2", "factor_4",
                data=pca_res.loc[:90,:])
plt.figure()
sns.scatterplot("factor_2", "factor_1",
                data=pca_res.loc[:90,:])



