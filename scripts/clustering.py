import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
#%matplotlib inline

#En clus4.csv debe estar el archivo con los datos normalizados para usar clustering

data = pd.read_csv("clus4.csv",delimiter="\t")
#data = data.ix[:,2:]
data = data.replace('\\N','0')
data[:] = data[:].convert_objects(convert_numeric=True)
X = data.as_matrix()
Xnorm = X / X.max(axis=0)

#Xnorm[:,0] = 5*Xnorm[:,0]
#print Xnorm
print list(data)
print X.max(axis=0)

sm = pd.tools.plotting.scatter_matrix(data,figsize=(16,10))
plt.show()

err = [np.nan,np.nan]
for i in range(2,18):
    km = KMeans(n_clusters=i)
    km.fit(Xnorm)
    err.append(km.inertia_)

plt.figure(figsize=(12,8))
plt.xlabel("K")
plt.ylabel("MSE")
plt.title("Error cuadratico medio con respecto a la cantidad de clusters")
plt.plot(err)

### KMEANS
km = KMeans(n_clusters=6)
km.fit(Xnorm)
print "\t".join(map(lambda(e): str(e)[1:8],list(data)))
for c in km.cluster_centers_:
    print "\t".join(map(lambda(e): str(e)[0:7],c))
    
print "\n Distancia media cluster-dato: "+str(float(km.inertia_)/len(X)/9)


### DBSCAN
from sklearn.cluster import DBSCAN

db = DBSCAN(eps=0.15, min_samples=20).fit(Xnorm)
print "Samples = " + str(len(db.core_sample_indices_)) + " / " + str(len(X))
print "Clusters = " + str(np.max(db.labels_)+1)

from sklearn import decomposition

pca = decomposition.PCA(n_components=2)
pca.fit(Xnorm)

### KMEANS plot
Xpca = pca.transform(Xnorm)
plt.figure(figsize=(12,8))
plt.axis([np.min(Xpca[:,0]),np.max(Xpca[:,0]),np.min(Xpca[:,1]),np.max(Xpca[:,1])])
plt.scatter(Xpca[:,0],Xpca[:,1], c=km.labels_)

plt.figure(figsize=(12,8))
plt.axis([np.min(Xpca[:,0]),np.max(Xpca[:,0]),np.min(Xpca[:,1]),np.max(Xpca[:,1])])

### DBSCAN plot
A = ['blue','green','orange','purple','red','yellow','cyan','magenta','gray','lightblue','pink','darkgreen',
    'darkred','brown','black']

def uncolor_noise(d):
    if d==-1:
        return 'white'
    else:
        return A[d]

ldd = map(uncolor_noise,db.labels_)

plt.scatter(Xpca[:,0],Xpca[:,1], c=ldd)

### Matriz de Distancia
samples = 10
clsampl = []
for i in range(0,6):
    k = np.nonzero(km.labels_ == i)[0][0:samples].tolist()
    for e in k:
        clsampl.append(e)


M = []
for i in range(len(clsampl)):
    L = []
    for j in range(len(clsampl)):
        Xr = Xnorm[clsampl[i]] - Xnorm[clsampl[j]]
        L.append(np.sqrt(9)-np.sqrt(np.dot(Xr,Xr)))
    M.append(L)
    
plt.figure(figsize=(12,12))    
plt.matshow(M,interpolation='nearest',aspect='auto')
plt.show()