from scipy.spatial import distance

### SMOKE
"""
#набор точек для смоук-теста
p1 = [1,1,1]
p2 = [1,1,2]
p3 = [1,10,1]
p4 = [2,20,1]
points = [p1,p2,p3,p4]

#кластеры для смоук-теста
lables = [0,1,1,0] 

"""
###SMOKE

def converter_to_c(points, lables) -> []:
    C = []  # count=len(set(labels)) np.float # При создании С=[[]]*len(set(labels))
            # мы фактически получаем ссылки на некий объект [] len(set(labels)) раз
            # и при добавлении нового элемента в массив С, он будет во всех подмассивах.
    b = []
    for _ in range(len(set(labels))):
        C.append(b[:])  # Не глубокое копирование
    for index, label in enumerate(labels):
        C[label].append(points[index])
    return C

def get_C(labels,points): #Happy New Year! ---Argailo points&labels
    C = list()
    for i in range (0,max(lables) + 1,1):
        C.append( list() )
    for i in range (0,len(lables),1):
        C[lables[i]-1].append(points[i])
    return(C)
 

##SMOKE
#C = get_C(lables,points) 
#print(C)
##SMOKE

# МЕТРИКИ ‘braycurtis’, ‘canberra’, ‘chebyshev’,
#‘cityblock’, ‘correlation’, ‘cosine’, ‘dice’, ‘euclidean’, ‘hamming’,
#‘jaccard’, ‘jensenshannon’, ‘kulczynski1’, ‘mahalanobis’, ‘matching’,
#‘minkowski’, ‘rogerstanimoto’, ‘russellrao’, ‘seuclidean’, 
#‘sokalmichener’, ‘sokalsneath’, ‘sqeuclidean’, ‘yule’.

def MeanIntraclusterDistance(C,i):

    #Нормализация
    normMintra = lambda i : 1/( (len(C[i])) * (len(C[i]) - 1) )

    sum = 0
    for i1 in C[i]:
        for j1 in C[i]:
            if j1 != i1:
                # Расстояние, ВСТАВЬТЕ МЕТРИКУ!
                sum += distance.euclidean(i1,j1)
        
    MIntra = normMintra(i) * sum
    return(MIntra)
    
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
    
def MaxIntraCluster(C,i):
    maxd = 0
    
    for i1 in C[i]:
        for j1 in C[i]:
            if j1 != i1:
                # Расстояние, ВСТАВЬТЕ МЕТРИКУ!
                temp = distance.euclidean(i1,j1)
                if temp > maxd:
                    maxd = temp
    return(maxd)
  
def MaxInterCluster(C,i,j):
    maxd = 0
    
    for i1 in C[i]:
        for j1 in C[j]:
            # Расстояние, ВСТАВЬТЕ МЕТРИКУ!
            temp = distance.euclidean(i1,j1)
            if temp > maxd:
                maxd = temp
    return(maxd)
    
def MinInterCluster(C,i,j):

    mind = distance.euclidean(C[i][0],C[j][0]) 
    for i1 in C[i]:
        for j1 in C[j]:
            # Расстояние, ВСТАВЬТЕ МЕТРИКУ!
            temp = distance.euclidean(i1,j1)
            if temp < mind:
                mind = temp
    return(mind)
    
    
def MeanIntraclusterDeviation(C,i):
    
    #Инициализация 
    res = 0 
    mi = []
    for j1 in range (0,len(C[i][0]),1):
        mi.append(0)
    
    #Поиск средневзешенного центроида
    #Сумма координат точек
    for i1 in C[i]:
        for j1 in range (0,len(C[i][0]),1):
            mi[j1] += i1[j1]
    #Нормализация
    for j1 in range (0,len(C[i][0]),1):
            mi[j1] /= len(C[i])
    #Поиск среднего отклонения
    for i1 in C[i]:
        # Расстояние, ВСТАВЬТЕ МЕТРИКУ!
        res += distance.euclidean(i1,mi)
    res /= len(C[i])
    return(res)  
    
    
def MeanInterClusterDeviation(C,i,j):
    
    #Инициализация 
    res  = 0 
    res2 = 0
    mi = []
    for j1 in range (0,len(C[i][0]),1):
        mi.append(0)
    mj = []
    for j1 in range (0,len(C[j][0]),1):
        mj.append(0)
        
    #Поиск средневзешенного центроида i
    #Сумма координат точек
    for i1 in C[i]:
        for j1 in range (0,len(C[i][0]),1):
            mi[j1] += i1[j1]
    #Нормализация
    for j1 in range (0,len(C[i][0]),1):
            mi[j1] /= len(C[i])
            
    #Поиск средневзешенного центроида j
    #Сумма координат точек
    for i1 in C[j]:
        for j1 in range (0,len(C[j][0]),1):
            mj[j1] += i1[j1]
    #Нормализация
    for j1 in range (0,len(C[j][0]),1):
            mj[j1] /= len(C[j])
            
    #Поиск среднего отклонения
    for i1 in C[i]:
        # Расстояние, ВСТАВЬТЕ МЕТРИКУ!
        res += distance.euclidean(i1,mj)
    res /= len(C[i])
    
    for i1 in C[j]:
        # Расстояние, ВСТАВЬТЕ МЕТРИКУ!
        res2 += distance.euclidean(i1,mi)
    res2 /= len(C[i])
    
    res += res2
    return(res)
    
#Dunn индекс с минимальным расстоянием между кластерами
def DunnIndex(C):
    mind = 100000
    maxd = 0
    for i in range (0, len(C), 1):
        for j in range (i+1, len(C), 1):
                temp = MinInterCluster(C,i,j)
                if mind > temp:
                    mind = temp
    for i in range (0, len(C), 1):
        temp = MaxIntraCluster(C,i)
        if temp > maxd:
            maxd = temp

    return(mind/maxd)

#Dunn индекс с минимальным средним расстоянием между кластерами

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


def S_Intra(C,i,a):
# !!! a in i cluster    
    sum = 0
    norm = 1/(len(C[i]) - 1)
    for i1 in C[i]:
        # Расстояние, ВСТАВЬТЕ МЕТРИКУ!
        if i1 != a:
            sum += distance.euclidean(i1,a)
    return(sum*norm)

def S_Inter(C,i,a):
    # !!! a in i cluster
    #Инициализация
    sum = 0
    min = 100000
    norm = lambda i : 1/(len(C[i]))
    
    #
    for i1 in range (0, len(C), 1):
        if i1 != i:
            for j1 in C[i1]:
                # Расстояние, ВСТАВЬТЕ МЕТРИКУ!
                sum += distance.euclidean(j1,a)
            sum *= norm(i1)
            if sum < min:
                min = sum
    return(min)

def silhouette(C,i,a):
    res = (S_Inter(C,i,a) - S_Intra(C,i,a))/max(S_Inter(C,i,a),S_Intra(C,i,a))
    return res
    
#DBi assist methods
def normp(p,u,v):
    sum = 0
    for i in range (0, len(u), 1):
        tempsum = 0
        tempsum += abs(u[i] - v[i])
        tempsum = tempsum **p
        sum += tempsum
    return(sum **(1/p))

def Mi(C,i):
    #Инициализация
    mi = []
    for j1 in range (0,len(C[i][0]),1):
        mi.append(0)
    
    #Поиск средневзешенного центроида i
    #Сумма координат точек
    for i1 in C[i]:
        for j1 in range (0,len(C[i][0]),1):
            mi[j1] += i1[j1]
    #Нормализация
    for j1 in range (0,len(C[i][0]),1):
            mi[j1] /= len(C[i])
    return (mi)

            
            
def IntraclusterSeparation(C,i,p,q):
    
    Norm = 1/len(C[i])
    sum = 0
    
    M = Mi(C,i)
    for i1 in C[i]:
        sum += normp(p,i1,M)**q
    sum *= Norm
    sum  = sum **(1/q)
    return(sum)

def InterclusterSeparation(C,l,k,p):
        
    u = Mi(C,l)
    v = Mi(C,k)
    res = normp(p,u,v)
    return(res)


def DBi_formula(C,l,k,p,q):
    return((IntraclusterSeparation(C,l,p,q) + IntraclusterSeparation(C,k,p,q))/InterclusterSeparation(C,l,k,p))
    
def DBi_max(C,p,q,l):
    max = 0
    for i in range (0, len(C), 1):
            if i!= l :
                temp = DBi_formula(C,i,l,p,q)
                if temp > max:
                    max = temp
    max /= len(C)
    return(max)
    
def DBi(C,p,q):
    sum = 0
    for i in range (0, len(C), 1):
        sum += DBi_max(C,p,q,i)
    sum /= len(C)
    return(sum)


##TEST   
##DBi_formula(C,0,1,1,1)
##print(DBi_max(C,1,1))


