import time

from matplotlib import pyplot as plt

import numpy as np
from numpy import linspace, cos, sin, pi
from numpy.random import default_rng

from sklearn.datasets import make_blobs

if __name__ == '__main__':
    X, y = make_blobs(n_samples=10, centers=3, n_features=2,
                      random_state=0)
    print(X.shape)
    X, y = make_blobs(n_samples=[3, 3, 4], centers=None, n_features=2,
                      random_state=0)
    print(X.shape)
