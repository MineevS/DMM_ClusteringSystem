import time

import numpy as np
from numpy import linspace, cos, sin, pi
from numpy.random import default_rng
from matplotlib import pyplot as plt

from sklearn.datasets import make_moons

if __name__ == '__main__':
    tic = time.process_time()
    Data, label = make_moons()
    toc = time.process_time()
    print(f"Вычисление заняло {toc - tic:0.4f} секунд")