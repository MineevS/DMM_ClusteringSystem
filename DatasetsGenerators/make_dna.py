import time

import numpy as np
from matplotlib import pyplot as plt

#from math import pi, sin, cos

from numpy import linspace, cos, sin, pi

from numpy.random import default_rng

def make_dna(n_samples: int = 300, center_box = (-1.0, 1.0),
             width: float  = 0.5, min_u: float = 0.0, max_u: float = 3 * pi):
    # ВЫЧИСЛЕНИЯ
    rng = default_rng()
    u = linspace(min_u, max_u, n_samples)
    x1, x2 = width * cos(u), - width * cos(u)
    y1, y2 = width * sin(u), - width * sin(u)
    z1, z2 = u / pi, u / pi

    x_nod1, y_nod1, z_nod1 = [], [], []
    x_nod2, y_nod2, z_nod2 = [], [], []
    for i in range(n_samples):
        for axis_nod_i, axis_i in zip([x_nod1, y_nod1, z_nod1, x_nod2, y_nod2, z_nod2], [x1, y1, z1, x2, y2, z2]):
            axis_nod_i.append(axis_i[i] + rng.uniform(low=center_box[0], high=center_box[1]))

    label1 = [0] * len(x_nod1)
    label2 = [1] * len(x_nod2)

    return [[x_nod1 + x_nod2, y_nod1 + y_nod2, z_nod1 + z_nod2], [x1, y1, z1],  [x2, y2, z2]], [label1, label2]

if __name__ == '__main__':
    tic = time.process_time()
    Data, label = make_dna()
    toc = time.process_time()
    print(f"Вычисление заняло {toc - tic:0.4f} секунд")

    x_nod1, y_nod1, z_nod1 = Data[0][0], Data[0][1], Data[0][2]
    #x_nod2, y_nod2, z_nod2 = Data[1][0], Data[1][1], Data[1][2]

    x1, y1, z1 = Data[1][0], Data[1][1], Data[1][2]
    x2, y2, z2 = Data[2][0], Data[2][1], Data[2][2]

    # ГРАФИКИ
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    ax.plot3D(x1, y1, z1)
    ax.plot3D(x2, y2, z2)
    ax.scatter(x_nod1, y_nod1, z_nod1, c=label)
    plt.title('TWO TWISTING CURVES CLOSE BY')

    ax = fig.add_subplot(1, 2, 2, projection='3d')
    ax.plot3D(x1, y1, z1)
    ax.plot3D(x2, y2, z2)
    ax.scatter(x_nod1, y_nod1, z_nod1, c=label)
    #ax.scatter(x_nod2, y_nod2, z_nod2)
    plt.xlim([-4, 4])
    plt.ylim([-4, 4])
    plt.title('TWO TWISTING CURVES IN THE DISTANCE')
    plt.show()