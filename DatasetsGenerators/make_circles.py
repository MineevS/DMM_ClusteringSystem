import time

from matplotlib import pyplot as plt

import numpy as np
from numpy import linspace, cos, sin, pi
from numpy.random import default_rng

from sklearn.datasets import make_circle

if __name__ == '__main__':
    tic = time.process_time()
    Data, label = make_circle()
    toc = time.process_time()
    print(f"Вычисление заняло {toc - tic:0.4f} секунд")