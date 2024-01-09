# Synthetic data and CURE clustering
Synthetic data for big data 2D/3D/large dimensions and the CURE clustering method

@Author 
	Meshkova O.V. [oxn.lar5@yandex.ru]

В данном репозитории представлены как стандартные методы генерации синтетических данных для кластеризации и их визуализация, так и новые разработанные методы.
Язык - Python.

# Новые функции 3D

### `make_s_curve_3D(n_sampls, nois, random_stat)`

Создание набора данных для двух S-образных кривых в трехмерном пространтсве. Одна кривая завернута вокруг другой, образуя винтовую форму. Используется make_s_curve из sklearn.datasets.  

Параметры:
- `n_sampls` (int): Число точек выборки для кривой - default = 100
- `nois` (float): Стандартное отклонение гауссовского шума - default = 0.0
- `random_stat` (int): Определяет генерацию случайных чисел для создания воспроизводимиого набора данных - default = None

Возвращает:
- `X1` (ndarray of shape (n_sampls, 3)): Точки для 1й кривой
- `X2` (ndarray of shape (n_sampls, 3)): Точки для 2й кривой
- `t` (ndarray of shape (n_sampls,)): Одномерное положение выборки в соответствии с основным размером точек

Пример:

![s-curve](https://github.com/Olga-GitH/Synthetic-data---CURE/blob/main/Examples/About_curves_Sklearn_My_3D.png)

### `make_spheres_3D(n_samp_user, shuff, nois, random_stat, factr)`

Создание набора данных для двух сфер в трехмерном пространтсве. Одна сфера поменьше внутри другой побольше, каждая представляется ввиде набора кругов разных размеров. Используется make_circles из sklearn.datasets.  

Параметры:
- `n_sampls_user` (int): Общее число сгенерированных точек - default = 1000000
- `shuff` (bool): Следует ли перемешивать образцы - default = True
- `nois` (float): Стандартное отклонение гауссовского шума - default = None
- `random_stat` (int): Определяет генерацию случайных чисел для создания воспроизводимиого набора данных - default = None
- `factr` (float): Масштабный коэффициент между внутренним и внешним кругом в диапазоне [0, 1)- default = 0.5

Возвращает:
- `mass_xyzt` (tuple): Для каждого i-го слоя кругов в mass_xyzt:
  - `i[0], i[1], i[2]` - Сгенерированные образцы координат по x, y, z
  - `i[3]` - Целочисленные метки (0 или 1) для принадлежности к классу (внутр или внеш) каждого образца.

Пример:

![s-curve](https://github.com/Olga-GitH/Synthetic-data---CURE/blob/main/Examples/About_spheres_Sklearn_My_3D.png)
 
### `make_DNA_3D(n_samples, length)`

Создание набора данных для двух спиралевидных кривых вида ДНК в трехмерном пространтсве. Одна кривая завернута вокруг другой, образуя винтовую форму. Количество витков (высота) спирали - регулируемая. Используется random из numpy.

Параметры:
- `n_samples` (int): Число сгенерированных точек для одной полосы спирали - default = 300
- `length` (int): Количество витков (высота) спирали- default = 3

Возвращает:
- `[x, y, z, beg, end]` (tuple): где
  - `x, y, z` - Сгенерированные образцы координат по x, y, z
  - `[beg:]` - Индексы образцов координат для 1й кривой
  - `[:end]` - Индексы образцов координат для 2й кривой

Пример:

![s-curve](https://github.com/Olga-GitH/Synthetic-data---CURE/blob/main/Examples/About_dna_helix_Random_My_3D.png)
 

 # Примеры запусков  
Основные идеи и примеры запусков данных функций 3D можно найти в следующих файлах:
 - About_curves_Sklearn_My_3D.ipynb
 - About_spheres_Sklearn_My_3D.ipynb
 - About_dna_helix_Random_My_3D.ipynb

Также можно найти пример генерации синтетических данных 2D, использующей основные распределения ['uniform', 'normal', 'exponential', 'lognormal', 'chisquare', 'beta']. Идея строится на том, что задав необходимые распределения и их параметры однажды, можно рандомно выбирать индекс распределения и индекс его параметров сколь угодно много раз, в зависимости от заданного количества фич требуемой выборки. Упрощается процесс описания набора данных - для вопроизведения необходимо только задать один сид `np.random.RandomState(seed)`
 - About_synthetic_data_Rand_My_2D.ipynb

Пример:

![s-curve](https://github.com/Olga-GitH/Synthetic-data---CURE/blob/main/Examples/About_synthetic_data_Rand_My_2D.png)
 

Примеры запусков стандартных методов 3D генерации из Sklearn можно найти в:
 -  _About_curves_rolls_Sklearn_3D.ipynb

Примеры запусков стандартных методов 2D генерации из Sklearn можно найти в:
 -  _About_blobs_and_others_Sklearn_2D.ipynb

Пример реализации и работы с алгоритмом кластеризации CURE можно найти в:
 - _About_CURE_implementation.ipynb

