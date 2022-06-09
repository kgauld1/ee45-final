import numpy as np
import keras
import pickle
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

DATA = pickle.load(open('traindat.pkl', 'rb'))

model = keras.models.Sequential([
    keras.layers.Conv2D(32,(3,3),activation = "sigmoid", input_shape=(8,8,1)) ,  
    keras.layers.MaxPooling2D(2,2),
    keras.layers.Flatten(), 
    keras.layers.Dense(10,activation ="relu"),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(4,activation = "softmax")   #Adding the Output Layer
])

adam=keras.optimizers.Adam(lr=0.001)
model.compile(optimizer='adam', loss=keras.losses.SparseCategoricalCrossentropy(), metrics = ['accuracy'])

X = DATA[0]
y = DATA[1]-1
X = X.reshape((len(X), 8, 8, 1))
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
print(y_train)
#model.summary()
history = model.fit(X_train,
                    y_train, 
                    epochs=10,
                    batch_size=30, 
                    validation_data=(X_test, y_test))
_, acc = model.evaluate(X_test, y_test)

print('MODEL ACCURACY:', acc)
#plt.plot(history.history['loss'])
#plt.show()

model.summary()
#pickle.dump(model, open('mlmodel.pkl', 'wb'))

print(X[0].shape)
print(model.predict(X[0].reshape(1,8,8,1)).argmax(axis=1))
print(y)