import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
import sys
import os
import math
# Import helper functions
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + "/../utils")
from data_operation import mean_squared_error
from data_manipulation import train_test_split


class LinearRegression():
    def __init__(self, n_iterations=100, learning_rate=0.001, gradient_descent=True):
        self.w = None
        self.n_iterations = n_iterations
        self.learning_rate = learning_rate
        self.gradient_descent = gradient_descent

    def fit(self, X, y):
        # Insert constant ones for bias weights
        X = np.insert(X, 0, 1, axis=1)
        if self.gradient_descent:
            # Get weights by gradient descent opt.
            n_features = np.shape(X)[1]
            # Initial weights between [-1/sqrt(N), 1/sqrt(N)]
            a = -1 / math.sqrt(n_features)
            b = -a
            self.w = (b - a) * np.random.random((n_features, )) + a
            # Tune weights for n_iterations
            for _ in range(self.n_iterations):
                w_gradient = -(y - X.dot(self.w)).dot(X)
                self.w -= self.learning_rate * w_gradient
        else:
            # Get weights by least squares (by pseudoinverse)
            U, S, V = np.linalg.svd(X.T.dot(X))
            S = np.diag(S)
            X_sq_inv = V.dot(np.linalg.pinv(S)).dot(U.T)
            self.w = X_sq_inv.dot(X.T).dot(y)

    def predict(self, X):
        # Insert constant ones for bias weights
        X = np.insert(X, 0, 1, axis=1)
        y_pred = X.dot(self.w)
        return y_pred

def main():

    X, y = datasets.make_regression(n_features=1, n_samples=100, bias=3, noise=15)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)

    clf = LinearRegression()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    # Print the mean squared error
    print "Mean Squared Error:", mean_squared_error(y_test, y_pred)

    # Plot the results
    plt.scatter(X_test[:, 0], y_test, color='black')
    plt.plot(X_test[:, 0], y_pred, color='blue', linewidth=3)
    plt.show()

if __name__ == "__main__":
    main()
