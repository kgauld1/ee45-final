import numpy as np
import pickle
import matplotlib.pyplot as plt

import threading
import cv2 as cv

import serial
import time

START = b'-'
reading = True
data = np.zeros((8,8))

CLASSES = ['PEACE SIGN', 'LETTER C', 'LETTER T', 'NO GESTURE RECOGNIZED']


savedat = []
filename='g4.pkl'

def closeSerial():
    global reading
    reading = False

def readFromSerial():
    global data
    ser = serial.Serial(port='/dev/cu.usbmodem14301', 
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

    model = pickle.load(open('mlmodel.pkl', 'rb'))
    sgd = pickle.load(open('sgd.pkl', 'rb'))
    try:
        while True:
            if np.ptp(data) != 0:
                norm = (data - np.min(data))/np.ptp(data)
                norm = 1-(norm*255).astype(np.uint8)
                plt.imshow(norm, cmap='gray')
                
                mlpred = model.predict(data.reshape(1,8,8,1)).argmax(axis=1)[0]
                sgdpred = sgd.predict(data.flatten().reshape((1,-1))) -1

                cval = int(mlpred if mlpred==3 else sgdpred)

                plt.title(CLASSES[cval])
                plt.pause(0.001)
                time.sleep(0.2)
    except KeyError:
        closeSerial()
    
    serial_rd.join()