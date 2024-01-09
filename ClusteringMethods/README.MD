
@Authors 
		Mineev S. A. [mineeff20@yandex.ru]
		Meshkova O. V. [oxn.lar5@yandex.ru]
		
		
Ниже приведены сведения о методах кластеризации, которые используются в данном проекте в версии v1.1.

1. BIRCH из библиотеки scikit-learn
	Установка:
		python -m pip install scikit-learn
		from  sklearn.cluster import birch
		
	Использование:
		Сигнатура: class sklearn.cluster.Birch(*, threshold=0.5, branching_factor=50, n_clusters=3, compute_labels=True, copy=True)
		
		Описание: 
			> threshold [float, default=0.5]
			Радиус подкластера, полученный путём слияния нового образца и ближайшего подоскопления, должен быть меньше порога. 
			В противном случае запускается новый подкластер. Установка этого значения на очень низком способствует расщеплению и наоборот.

			> branching_factor [int, default=50]
			Максимальное число подгрупп CF в каждом узле. Если новый образец входит таким образом, что число подкластеров превышает факторbranching_, то этот узел разбивается на два узла с подгруппами, перераспределяемыми в каждом. Родительский подкласс этого узла удаляется, и два новых подкласса добавляются в качестве родителей двух разделенных узлов.

			> n_clusters [int, instance of sklearn.cluster model or None, default=3]
			Число кластеров после заключительного этапа кластеризации, на котором подгруппы из листьев рассматриваются как новые образцы.

			> compute_labels [bool, default=True]
			Вычислять или не вычислять метки для каждого соответствия.

			> copy [bool, default=True]
			Делать или не делать копию данных. Если установлено значение False, начальные данные будут перезаписаны.
			
	Источник: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.Birch.html
		

2. BIRCH из библиотеки pyclustering

	Установка:
		python -m pip install pyclustering
		from pyclustering.cluster.birch import birch
		from pyclustering.container.cftree import measurement_type
		
	Использование:
		Сигнатура: method pyclustering.cluster.birch.birch(data, number_clusters=3, branching_factor=50, max_node_entries=3, diameter=0.5, 
			type_measurement= measurement_type.CENTROID_EUCLIDEAN_DISTANCE, entry_size_limit=500, diameter_multiplier=1.5, ccore=True)
		
		Описание: 
			> data [list]
			входные данные, представленные в виде списка точек (объектов), где каждая точка представлена списком координат.
			
			> number_clusters [uint, default=3]
			Количество кластеров, которые должны быть выделены.

			> branching_factor [uint, default=50]
			Максимальное количество последователей, которые могут содержаться в каждом нелистовом узле в CF-дереве.

			> max_node_entries [uint, default=200]
			Максимальное количество записей, которые могут содержаться в каждом конечном узле в CF-дереве.
			
			> diameter [float, default=0.5]
			CF-входной диаметр, используемый для построения CF-дерева, он может увеличиться, если превышен 'entry_size_limit'.
			
			> type_measurement [struct <type_measurement>, default=measurement_type.CENTROID_EUCLIDEAN_DISTANCE]
			тип измерения, используемый для вычисления показателей расстояния.

			> entry_size_limit [uint, default=500]
			Максимальное количество записей, которое может храниться в CF-дереве, если оно превышено при создании, 
			то "диаметр" увеличивается и CF-дерево перестраивается.

			> diameter_multiplier [float, default=1.5]
			множитель, который используется для увеличения диаметра при превышении 'entry_size_limit'
			
			> ccore [bool, default=True]
			Если True, то для обработки используется часть библиотеки C++.
			
	Источник:
		https://pyclustering.github.io/docs/0.10.1/html/d6/d00/classpyclustering_1_1cluster_1_1birch_1_1birch.html

3. CURE из библиотеки pyclustering

	Установка:
		python -m pip install pyclustering
		from pyclustering.cluster.cure import cure
		
	Использование:
		Сигнатура: method pyclustering.cluster.cure.cure(data, number_clusters=3, number_represent_points=5, compression=0.5, ccore=True)
		
		Описание: 
			> data [list]
			входные данные, представленные в виде списка точек (объектов), где каждая точка представлена списком координат.
			
			> number_clusters [uint, default=3]
			Количество кластеров, которые должны быть выделены.

			> number_represent_points [uint, default=5]
			количество репрезентативных точек для каждого кластера.

			> compression [uint, default=0.5]
			коэффициент определяет уровень сжатия точек представления по отношению к среднему значению для нового созданного кластера
			после объединения на каждом шаге. Обычно он определяется от 0 до 1.
			
			> ccore [bool, default=True]
			Если True, то для обработки используется часть библиотеки C++.
			
	Источник: https://pyclustering.github.io/docs/0.10.0/html/dc/d6d/classpyclustering_1_1cluster_1_1cure_1_1cure.html

4. ROCK из библиотеки pyclustering

	Установка:
		python -m pip install pyclustering
		from pyclustering.cluster.rock import rock
		
	Использование:
		Сигнатура: method pyclustering.cluster.rock.rock(data, eps, number_clusters=3, compute_labels=True, copy=True)
		
		Описание: 
			> data [list]
			Входные данные - список точек, где каждая точка представлена списком координат.
			
			> eps [float, default=?]
			радиус связности (порог подобия), точки являются соседними, если расстояние между ними меньше радиуса связности.
			
			> number_clusters [uint, default=3]
			Количество кластеров, которые должны быть выделены.

			> threshold [uint, default=0.5]
			значение, определяющее степень нормализации, которая влияет на выбор кластеров для объединения во время обработки.
			
			> ccore [bool, default=True]
			Определяет, должен ли CCORE (библиотека C ++ для пикластеринга) использоваться вместо кода Python или нет.
			
	Источник: https://pyclustering.github.io/docs/0.8.2/html/d8/dde/classpyclustering_1_1cluster_1_1rock_1_1rock.html
	
	