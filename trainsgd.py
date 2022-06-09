import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier

if __name__=="__main__":
    data = pickle.load(open('traindat.pkl', 'rb'))
    X = np.array(data[0])
    y = np.array(data[1])
    X = X.reshape(len(X), 64)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    sgd_clf = SGDClassifier(random_state=42, max_iter=1000, tol=1e-3)
    sgd_clf.fit(X_train, y_train)
    y_pred = sgd_clf.predict(X_test)
    acc = np.sum(y_pred == y_test)/len(y_test)
    pickle.dump(sgd_clf, open('sgd.pkl', 'wb'))