import time
import numpy as np
from sklearn.datasets import make_circles
from numpy import arange
import matplotlib.pyplot as plt
from math import pi, sin, ceil

def make_spheres(n_samples=100, shuffle=None, noise=None, random_state=None, factor=0.5):
    levels = 10
    n_samp = round(n_samples * (2 / 3))
    z = [sin(i) for i in arange(-pi / 2, pi / 2 + ((pi / 2) / levels), (pi / 2) / levels)]
    sampls = [abs(i) for i in range(-levels, levels + 1)]
    sampl_i = [ceil(n_samp / 2) if i == 0 else ceil((n_samp / 2) * (1 / pow(2, i))) for i in sampls]
    sampl_i[levels] -= (sum(sampl_i) - n_samples)

    data = [[], [], []]
    labels = []
    for i in range(len(sampls)):
        xy, label = make_circles(n_samples=sampl_i[i], shuffle=shuffle, noise=noise, random_state=random_state, factor=factor)
        xy[:, 0] = xy[:, 0] * ((levels + 1 - sampls[i]) / (levels))
        xy[:, 1] = xy[:, 1] * ((levels + 1 - sampls[i]) / (levels))

        data[0] += xy[:, 0].tolist()
        data[1] += xy[:, 1].tolist()
        data[2] += [z[i] for _ in range(xy[:, 0].shape[0])]
        labels += label.tolist()

    return data, labels

''' 
if __name__ == '__main__':
    tic = time.process_time()
    Data, labels = make_spheres(n_samp_user=1000000, shuffle=True, nois=None, random_stat=None, factr=0.5)
    toc = time.process_time()
    print(f"Вычисление заняло {toc - tic:0.4f} секунд")

    fig = plt.figure(figsize=(10, 8))
    ax = plt.axes(projection='3d')
    ax.view_init(5, 45)
    ax.scatter(Data[0], Data[1], Data[2], c=labels, cmap='plasma')
    ax.set_xlabel('X-axis', fontweight='bold')
    ax.set_ylabel('Y-axis', fontweight='bold')
    ax.set_zlabel('Z-axis', fontweight='bold')
    plt.show()
'''