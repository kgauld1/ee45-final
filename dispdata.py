import pickle
import numpy as np
import matplotlib.pyplot as plt

CLASSES = ['PEACE SIGN', 'LETTER C', 'LETTER T', 'NO GESTURE']


d1 = pickle.load(open('g1.pkl', 'rb'))[0:10]
d2 = pickle.load(open('g2.pkl', 'rb'))[0:10]
d3 = pickle.load(open('g3.pkl', 'rb'))[0:10]
d4 = pickle.load(open('g4.pkl', 'rb'))[0:10]
ds = [d1,d2,d3,d4]
idx = 0
plt.figure(figsize=(15,6))
for k in range(len(ds)):
    for i in range(len(ds[k])):
        plt.subplot(4,10,k*10+i+1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(ds[k][i], cmap=plt.cm.binary)
        plt.xlabel(CLASSES[k])
        
plt.show()

plt.figure(figsize=(15,9))
out = pickle.load(open('OUT.pkl', 'rb'))
for k in range(len(out)):
    plt.subplot(6,10,k+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(out[k][0], cmap=plt.cm.binary)
    plt.xlabel(CLASSES[out[k][1]])

plt.show()

plt.figure(figsize=(15,9))
out = pickle.load(open('OUT.pkl', 'rb'))
for k in range(len(out)):
    data = out[k][0]
    norm = (data - np.min(data))/np.ptp(data)
    norm = 1-(norm*255).astype(np.uint8)
    plt.subplot(6,10,k+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(norm, cmap=plt.cm.binary)
    plt.xlabel(CLASSES[out[k][1]])

plt.show()
