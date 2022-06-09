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

    model = pickle.read(open('mlmodel.pkl', 'rb'))
    try:
        while True:
            if np.ptp(data) != 0:
                norm = (data - np.min(data))/np.ptp(data)
                norm = 1-(norm*255).astype(np.uint8)
                plt.imshow(norm, cmap='gray')
                
                plt.title(model.predict(data.reshape(1,8,8,1)).argmax(axis=1))
                plt.pause(0.001)
                time.sleep(0.2)
    except KeyError:
        closeSerial()
    
    serial_rd.join()