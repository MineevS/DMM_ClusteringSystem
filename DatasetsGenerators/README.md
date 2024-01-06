
Ниже приведены сведения о методах генерации данных

Описание: 

	1 Генерация данных по распределениям
	
	1.1 Нормальное распределение
	
	Установка и использование:
		python -m pip install numpy as np
		seed = None (default)
		rand = np.random.RandomState(seed)
		
		Сигнатура: 
			out: ndarray = rand.normal(loc, scale, size=());
		
		Параметры:
			> loc [float or array_like of floats]
			Среднее значение (“центр”) распределения.
			
			> scale [float or array_like of floats]
			Стандартное отклонение (разброс или “ширина”) распределения. Должно быть неотрицательным.
			
			> size [int or tuple of ints, optional]
			Вывод фигуры. Если заданной формой является, например, (m, n, k), то m * n * k отрисовываются образцы. 
			Если значение size равно None (по умолчанию), возвращается единственное значение, если loc и scale оба являются скалярами. 
			В противном случае, np.broadcast(loc, scale).size отрисовываются выборки.
		
		Возвращаемое значение:
			> out [ndarray or scalar]
			Взяты выборки из параметризованного нормального распределения.
		
	Ссылка: https://numpy.org/doc/stable/reference/random/generated/numpy.random.normal.html
		
	
	1.2 Биноминальное распределение
	
	Установка и использование:
		python -m pip install numpy as np
		seed = None (default)
		rand = np.random.RandomState(seed)
		
		Сигнатура: 
			out: ndarray = rand.binomial(n, p, size=());
		
		Параметры:
			> loc [float or array_like of floats]
			Среднее значение (“центр”) распределения.
			
			> scale [float or array_like of floats]
			Стандартное отклонение (разброс или “ширина”) распределения. Должно быть неотрицательным.
			
			> size [int or tuple of ints, optional]
			Вывод фигуры. Если заданной формой является, например, (m, n, k), то m * n * k отрисовываются образцы. 
			Если значение size равно None (по умолчанию), возвращается единственное значение, если loc и scale оба являются скалярами. 
			В противном случае, np.broadcast(loc, scale).size отрисовываются выборки.
		
		Возвращаемое значение:
			> out [ndarray or scalar]
			Взяты выборки из параметризованного нормального распределения.
		
	Ссылка: https://numpy.org/doc/stable/reference/random/generated/numpy.random.binomial.html
	
	1.3 Показательное распределение
	
	Установка и использование:
		python -m pip install numpy as np
		seed = None (default)
		rand = np.random.RandomState(seed)
		
		Сигнатура: 
			out: ndarray = rand.exponential(n, p, size=());
		
		Параметры:
			> scale [float or array_like of floats]
			Параметр масштаба, `b = 1 / lambda`. Должно быть неотрицательным.
			
			> size [int or tuple of ints, optional]
			Вывод фигуры. Если заданной формой является, например, (m, n, k), то m * n * k отрисовываются образцы. 
			Если значение size равно None (по умолчанию), возвращается единственное значение, если loc и scale оба являются скалярами. 
			В противном случае, np.broadcast(loc, scale).size отрисовываются выборки.
		
		Возвращаемое значение:
			> out [ndarray or scalar]
			Взяты выборки из параметризованного нормального распределения.
		
	Ссылка: https://numpy.org/doc/stable/reference/random/generated/numpy.random.normal.html
	
	Справка:
		Данные методы подключены к проекту и используются в функции [handler_pb6_fr1], класса [mainwindow], в файле [mainwindow.py]
		
		
	2 Генерация данных с использованием make-функций

	2.1 make_blobs
	
	Установка:
		python -m pip install scikit-learn
		seed = None (default)
		from sklearn.datasets import make_blobs
	
	Описание:
		Сигнатура:
			sklearn.datasets.make_blobs(n_samples=100, n_features=2, *, centers=None, cluster_std=1.0, center_box=(-10.0, 10.0), 
				shuffle=True, random_state=None, return_centers=False)
		
		Параметры:
			> n_samples [int or array-like, default=100]
			Если int, то это общее количество точек, поровну разделенных между кластерами. 
			Если в виде массива, каждый элемент последовательности указывает количество выборок в кластере.
			
			> n_features [int, default=2]
			Количество функций для каждого образца.
			
			> centers [int or array-like of shape (n_centers, n_features), default=None]
			Количество создаваемых центров или фиксированные местоположения центров. Если n_samples равно int, а centers равно None, генерируются 3 центра. 
			Если n_samples имеет вид массива, центры должны быть либо None, либо массивом длиной, равной длине n_samples .
			
			> cluster_std [float or array-like of float, default=1.0]
			Стандартное отклонение кластеров.
			
			> center_box [tuple of float (min, max), default=(-10.0, 10.0)]
			Ограничивающая рамка для каждого центра кластера, когда центры генерируются случайным образом.
			
			> shuffle [bool, default=True]
			Перемешайте образцы.
			
			> random_state [int, RandomState instance or None, default=None]
			Определяет генерацию случайных чисел для создания набора данных. Передайте значение int для воспроизводимого вывода в нескольких вызовах функций.
			
			> return_centers [bool, default=False]
			Если True, то верните центры каждого кластера.
		
		Возвращаемые значения:
		
			> X [ndarray формы (n_samples, n_features)]
			Сгенерированные образцы.

			> Y [ndarray of shape (n_samples,)]
			Целочисленные метки для принадлежности к кластеру каждого образца.

			> _ ndarray формы дляцентров (n_centers, n_features)
			Центры каждого кластера. Возвращается только, если return_centers=True.
		
	Источник: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_blobs.html

	2.2 make_circle
	
	Установка:
		python -m pip install scikit-learn
		from sklearn.datasets import make_circles
	
	Описание:
		Сигнатура:
			sklearn.datasets.make_circles(n_samples=100, shuffle=True, noise=, random_state=None, factor=.8)
		
		Параметры:
			> n_samples [int or tuple of shape (2,), dtype=int, default=100]
			Если int, то это общее количество сгенерированных точек. Для нечетных чисел внутренний круг будет иметь на одну точку больше, чем внешний круг. 
			Если кортеж из двух элементов, количество точек во внешнем круге и во внутреннем круге.

			> shuffle [bool, default=True]
			Следует ли перетасовывать образцы.
			
			> noise [float, default=None]
			Стандартное отклонение гауссовского шума, добавленного к данным.
			
			> random_state [int, RandomState instance or None, default=None]
			Определяет генерацию случайных чисел для перетасовки набора данных и шума. Передайте значение int для воспроизводимого вывода при нескольких вызовах функций.
			
			> factor[float, default=.8]
			Масштабный коэффициент между внутренним и внешним кругом в диапазоне 0 + (0, 1).
		
		Возвращаемые значения:
		
			> X [ndarray формы (n_samples, 2)]
			Сгенерированные образцы.

			> Y [ndarray of shape (n_samples,)]
			Целочисленные метки (0 или 1) для принадлежности к классу каждого образца.
		
	Источник: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_circles.html
	
	2.3 make_moons
	
	Установка:
		python -m pip install scikit-learn
		from sklearn.datasets import make_moons
	
	Описание:
		Сигнатура:
			sklearn.datasets.make_moons(n_samples=100, *, shuffle=True, noise=None, random_state=None)
		
		Параметры:
			> n_samples [int or tuple of shape (2,), dtype=int, default=100]
			Если int, то это общее количество сгенерированных точек. Для нечетных чисел внутренний круг будет иметь на одну точку больше, чем внешний круг. 
			Если кортеж из двух элементов, количество точек во внешнем круге и во внутреннем круге.

			> shuffle [bool, default=True]
			Следует ли перетасовывать образцы.
			
			> noise [float, default=None]
			Стандартное отклонение гауссовского шума, добавленного к данным.
			
			> random_state [int, RandomState instance or None, default=None]
			Определяет генерацию случайных чисел для перетасовки набора данных и шума. Передайте значение int для воспроизводимого вывода при нескольких вызовах функций.
		
		Возвращаемые значения:
		
			> X [ndarray формы (n_samples, n_features)]
			Сгенерированные образцы.

			> Y [ndarray of shape (n_samples,)]
			Целочисленные метки для принадлежности к кластеру каждого образца.
		
	Источник: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_moons.html
	
	2.4 make_dna
	
	Установка:
		from impl.make_dna import make_dna

	Описание:
		Сигнатура:
			sklearn.datasets.make_dna(n_samples: int=300, center_box=(-1.0, 1.0), width: float=0.5, 
				min_u: float=0.0, max_u: float=3*pi)
		
		Параметры:
			> n_samples [int or tuple of shape (2,), dtype=int, default=100]
			Если int, то это общее количество сгенерированных точек. Для нечетных чисел внутренний круг будет иметь на одну точку больше, чем внешний круг. 
			Если кортеж из двух элементов, количество точек во внешнем круге и во внутреннем круге.

			> center_box [bool, default=True]
			Следует ли перетасовывать образцы.
			
			center_box[0] - Нижняя граница выходного интервала. Все сгенерированные значения будут больше или равны low . Значение по умолчанию равно 0.
			center_box[1] - Верхняя граница выходного интервала. Все сгенерированные значения будут меньше максимального. Верхний предел может быть включен в возвращаемый массив значений с плавающей запятой из-за округления с плавающей запятой в уравнении `low + (high-low) * random_sample(). значение high - low` должно быть неотрицательным. Значение по умолчанию равно 1.0 .
			
			Источник: https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.uniform.html
			
			>  width [float, default=None]
			Ширина спирали.
			
			> min_u [int, RandomState instance or None, default=None]
			Определяет генерацию случайных чисел для перетасовки набора данных и шума. Передайте значение int для воспроизводимого вывода при нескольких вызовах функций.
			
			> max_u [int, RandomState instance or None, default=3*pi]
			Отвечает за высоту спирали. чем больше верхняя граница - тем больше витков.
		
		Возвращаемые значения:
		
			> X [ndarray формы (n_samples, n_features)]
			Сгенерированные образцы. В первой размерности X[0] расположены данные точек, во второй размерности X[1] Расположены направляющие линии спиралей.

			> Y [ndarray of shape (n_samples,)]
			Целочисленные метки для принадлежности к кластеру каждого образца.
		
	Источник: make_dna.py
	
	2.5 make_spheres
	
	Установка:
		from impl.make_spheres import make_spheres
	
	Описание:
		Сигнатура:
			make_spheres(n_samples=100, shuffle=None, noise=None, random_state=None, factor=0.5)
		
		Параметры:
			> n_samples [int or tuple of shape (2,), dtype=int, default=100]
			Если int, то это общее количество сгенерированных точек. Для нечетных чисел внутренний круг будет иметь на одну точку больше, чем внешний круг. 
			Если кортеж из двух элементов, количество точек во внешнем круге и во внутреннем круге.

			> shuffle [bool, default=True]
			Следует ли перетасовывать образцы.
			
			> noise [float, default=None]
			Стандартное отклонение гауссовского шума, добавленного к данным.
			
			> random_state [int, RandomState instance or None, default=None]
			Определяет генерацию случайных чисел для перетасовки набора данных и шума. Передайте значение int для воспроизводимого вывода при нескольких вызовах функций.
			
			> factor[float, default=.8]
			Масштабный коэффициент между внутренним и внешним кругом в диапазоне 0 + (0, 1).
		
		Возвращаемые значения:
		
			> X [ndarray формы (n_samples, n_features)]
			Сгенерированные образцы.

			> Y [ndarray of shape (n_samples,)]
			Целочисленные метки для принадлежности к кластеру каждого образца.
		
	Источник: make_spheres.py
	
	Справка:
		Данные методы подключены к проекту и используются в функции [handler_tw2_fr1], класса [mainwindow], в файле [mainwindow.py]
