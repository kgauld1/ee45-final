from lib2to3.pytree import Base
import numpy as np
import pickle
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
import threading
import cv2 as cv

import serial
import time

START = b'-'
reading = True
data = np.zeros((8,8))


savedat = []
filename='g4.pkl'

def train_model(datafile):
    data = pickle.load(open(datafile, 'rb'))
    X = np.array(data[0])
    y = np.array(data[1])
    X = X.reshape(len(X), 64)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    sgd_clf = SGDClassifier(random_state=42, max_iter=1000, tol=1e-3)
    sgd_clf.fit(X_train, y_train)
    y_pred = sgd_clf.predict(X_test)
    acc = np.sum(y_pred == y_test)/len(y_test)
    return sgd_clf, acc


def closeSerial():
    global reading
    reading = False

def readFromSerial():
    global data
    ser = serial.Serial(port='/dev/cu.usbmodem14401', 
                        baudrate=9600,
                        bytesize=serial.EIGHTBITS)
    databuffer = [[0]*8]*8
    while reading:
        while ser.readline()[:-2] != START:
            continue
        row = ser.readline()[:-2]
        rl = ser.readline()[:-2]

        databuffer[int(row)] = np.array([int(k) for k in rl.split()])
        if int(row) == 7:
            data = np.array(databuffer)
            if data[0].all() == 0:
                data = np.zeros((8,8))
            #else:
            #    global savedat
            #    savedat.append(data.copy())
    ser.close()




if __name__ == "__main__":
    serial_rd = threading.Thread(name='serial',
                                 target=readFromSerial)
    serial_rd.start()
    sgd, acc = train_model('traindat.pkl')
    print(acc)
    try:
        while True:
            if np.ptp(data) != 0: 
                norm = data #1/(1+np.exp(-data))
                norm = (norm - np.min(norm))/np.ptp(norm)
                norm = 1-(norm*255).astype(np.uint8)
                #edges = cv.Canny(image=norm, threshold1=100, threshold2=200)
                plt.imshow(norm, cmap='gray')
                
                plt.title(sgd.predict([data.flatten()])[0])
                plt.pause(0.001)
                time.sleep(0.2)
    except KeyError:
        closeSerial()
    
    serial_rd.join()