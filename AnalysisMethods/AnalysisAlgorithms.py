# Authors:
#       Nikolaev M. A. [Misha.via@yandex.ru]
#       Fedorov A. V. [alexis.sasis7@gmail.com]
#       Griban M. S. [gribanms007@gmail.com]

import numpy as np
from scipy.spatial import distance

def converter_to_c(points, labels) -> []:
    C = []  # count=len(set(labels)) np.float # При создании С=[[]]*len(set(labels))
            # мы фактически получаем ссылки на некий объект [] len(set(labels)) раз
            # и при добавлении нового элемента в массив С, он будет во всех подмассивах.
    b = []
    for _ in range(len(set(labels))):
        C.append(b[:])  # Не глубокое копирование
    for index, label in enumerate(labels):
        C[label].append(points[index])
    return C

#------------------------------------------------------------#

def MinInterCluster(C, i, j):
    mind = 100000

    for i1 in C[i]:
        for j1 in C[j]:
            # Расстояние, ВСТАВЬТЕ МЕТРИКУ!
            temp = distance.euclidean(i1, j1)
            if temp < mind:
                mind = temp
    return (mind)


def MaxIntraCluster(C, i):
    maxd = 0

    for i1 in C[i]:
        for j1 in C[i]:
            if j1 != i1:
                # Расстояние, ВСТАВЬТЕ МЕТРИКУ!
                temp = distance.euclidean(i1, j1)
                if temp > maxd:
                    maxd = temp
    return (maxd)


def DunnIndex(C):
    mind = 100000
    maxd = 0
    for i in range (0, len(C), 1):
        for j in range (i+1, len(C), 1):
                temp = MinInterCluster(C, i, j)
                if mind > temp:
                    mind = temp
    for i in range (0, len(C), 1):
        temp = MaxIntraCluster(C,i)
        if temp > maxd:
            maxd = temp

    return(mind/maxd)

#------------------------------------------------------------#

def MeanInterclusterDistance(C,i,j):
    #Нормализация
    normMinter = lambda i,j : 1/( len(C[i]) * len(C[j]))
    sum = 0
    for i1 in C[i]:
        for j1 in C[j]:
            # Расстояние, ВСТАВЬТЕ МЕТРИКУ!
            sum += distance.euclidean(i1,j1)
    MInter = sum * normMinter(i,j)
    return(MInter)

def DunnIndexMean(C):
    mind = 100000
    maxd = 0
    for i in range (0, len(C), 1):
        for j in range (i+1, len(C), 1):
                temp = MeanInterclusterDistance(C,i,j)
                if mind > temp:
                    mind = temp
    for i in range (0, len(C), 1):
        temp = MaxIntraCluster(C,i)
        if temp > maxd:
            maxd = temp

    return(mind/maxd)

#------------------------------------------------------------#

# DBi
def normp(p, u, v):
    sum = 0
    for i in range(0, len(u), 1):
        tempsum = 0
        tempsum += abs(u[i] - v[i])
        tempsum = tempsum ** p
        sum += tempsum
    return (sum ** (1 / p))


def Mi(C, i):
    # Инициализация
    mi = []
    for j1 in range(0, len(C[i][0]), 1):
        mi.append(0)

    # Поиск средневзешенного центроида i
    # Сумма координат точек
    for i1 in C[i]:
        for j1 in range(0, len(C[i][0]), 1):
            mi[j1] += i1[j1]
    # Нормализация
    for j1 in range(0, len(C[i][0]), 1):
        mi[j1] /= len(C[i])
    return (mi)


def IntraclusterSeparation(C, i, p, q):
    Norm = 1 / len(C[i])
    sum = 0

    M = Mi(C, i)
    for i1 in C[i]:
        sum += normp(p, i1, M) ** q
    sum *= Norm
    sum = sum ** (1 / q)
    return (sum)


def InterclusterSeparation(C, l, k, p):
    u = Mi(C, l)
    v = Mi(C, k)
    res = normp(p, u, v)
    return (res)

def DBi(C,l,k,p,q):
    return((IntraclusterSeparation(C,l,p,q) + IntraclusterSeparation(C,k,p,q))/InterclusterSeparation(C,l,k,p))

# default:  DBi(C,0,1,1,1);

#------------------------------------------------------------#

