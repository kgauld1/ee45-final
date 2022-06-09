import pickle
import matplotlib.pyplot as plt
import numpy as np


g1 = pickle.load(open('g1.pkl', 'rb'))
g2 = pickle.load(open('g2.pkl', 'rb'))
g3 = pickle.load(open('g3.pkl', 'rb'))
g4 = pickle.load(open('g4.pkl', 'rb'))
pkls = [g1,g2,g3,g4]


X = np.zeros((len(g1)+len(g2)+len(g3)+len(g4), 8, 8))
y = np.zeros(X.shape[0])
idx = 0
for i in range(4):
    g = pkls[i]
    print(i)
    for k in g:
        X[idx] = k
        y[idx] = int(i+1)
        idx+=1

print(X.shape)

display = True
if display:
    plt.figure(figsize=(10,10))
    for i in range(len(X)):
        plt.subplot(10,20,i+1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(X[i], cmap=plt.cm.binary)
        plt.xlabel(y[i])
        
    plt.show()

pickle.dump((X,y), open('traindat.pkl', 'wb'))