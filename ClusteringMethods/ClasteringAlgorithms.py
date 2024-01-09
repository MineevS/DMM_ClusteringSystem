#Authors:
#       Mineev S. A. [mineeff20@yandex.ru]
#       Meshkova O. V. [oxn.lar5@yandex.ru]

from __future__ import annotations
from abc import ABC, abstractmethod

import numpy as np                      # pip install numpy
from pyclustering.cluster.birch import birch
from pyclustering.cluster.cure import cure
from pyclustering.cluster.rock import rock
from pyclustering.container.cftree import measurement_type
from sklearn.cluster import Birch       # pip install sklearn-learn

class Context:
    """
    Контекст определяет интерфейс, представляющий интерес для клиентов.
    """

    def __init__(self, strategy: Strategy) -> None:
        """
        Обычно Контекст принимает стратегию через конструктор, а также
        предоставляет сеттер для её изменения во время выполнения.
        """

        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        """
        Контекст хранит ссылку на один из объектов Стратегии. Контекст не знает
        конкретного класса стратегии. Он должен работать со всеми стратегиями
        через интерфейс Стратегии.
        """
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        """
        Обычно Контекст позволяет заменить объект Стратегии во время выполнения.
        """
        self._strategy = strategy

    def do_some_clustering_image(self, pixels, params, i) -> []:
            """
            Вместо того, чтобы самостоятельно реализовывать множественные версии
            алгоритма, Контекст делегирует некоторую работу объекту Стратегии.
            """
            if i > 0:
                # Извлечение координат и цветов всех пикселей в формате HSV
                coords_and_colors = [
                    (x, y, pixels[y, x])
                    for y in range(pixels.shape[0])
                    for x in range(pixels.shape[1])
                ]
                # Преобразование координат и цветов в двумерный массив для кластеризации
                # X = np.array([[h, s, v] for (_, _, (h, s, v)) in coords_and_colors])
                X = [[float(h), float(s), float(v)] for (_, _, (h, s, v)) in coords_and_colors]
                # ------------------------------------------------------------------------------------- #
                labels = self._strategy.clastering_image(X, params)
                # ------------------------------------------------------------------------------------- #
                # Визуализация результата кластеризации
                colors = [
                    (255, 0, 0),
                    (0, 255, 0),
                    (0, 0, 255),
                    (255, 255, 0),
                    (255, 0, 255),
                    (0, 255, 255),
                ]
                clustered_image = np.zeros_like(pixels)
                for index, (x, y, _) in enumerate(coords_and_colors):
                    clustered_image[y, x] = colors[labels[index] % len(colors)]
            else: 
                # None(used Rashape)
                labels = self._strategy.clastering_image(pixels.tolist(), params)
            return labels

    def do_some_clustering_points(self, data, params) -> []:
        fitchs = np.array(data, dtype=float)
        points = fitchs.transpose()
        if isinstance(self._strategy, ConcreteStrategyBIRCH_from_SKLEARN_LEARN):
            labels = self._strategy.clastering_points(points, params).tolist()
        else:
            labels = self._strategy.clastering_points(points, params)
        return labels


class Strategy(ABC):
    """
    Интерфейс Стратегии объявляет операции, общие для всех поддерживаемых версий
    некоторого алгоритма.

    Контекст использует этот интерфейс для вызова алгоритма, определённого
    Конкретными Стратегиями.
    """
    @abstractmethod
    def clastering_image(self, image_path: str, num_clasters: int):
        pass

    @abstractmethod
    def clastering_points(self):
        pass

    """
    @brief Метод преобразование cluster_index in labels для birch из sklearn-learn.
    """
    def clusters_to_labels(self, clusters) -> []:
        size = sum(map(lambda x: len(x), clusters))
        labels = [0] * size
        for cluster_index in range(len(clusters)):
            for i in clusters[cluster_index]:
                labels[i] = cluster_index

        return labels


"""
Конкретные Стратегии реализуют алгоритм, следуя базовому интерфейсу Стратегии.
Этот интерфейс делает их взаимозаменяемыми в Контексте.
"""
class ConcreteStrategyBIRCH_from_SKLEARN_LEARN(Strategy):

    '''
        @brief метод кластеризации изображений с использованием birch из sklearn-learn.

        @param[in] self (obj): The current object.
        @param[in] pixels (list): the image represented by pixels.
        @param[in] params (list): the parameters for clustering.

        @return (list) The label for everyone pixel.
    '''
    def clastering_image(self, pixels: str, params: []) -> list:
        # Создание и обучение объекта BIRCH
        birch1 = Birch(n_clusters=int(params[0]), branching_factor=int(params[1]), threshold=params[2],
            compute_labels=params[3], copy=params[4])
        birch1.fit(pixels)

        # Получение меток кластеров для каждой точки
        #labels = birch1.labels_
        labels = birch1.predict(pixels)
        return labels


    '''
        @brief метод кластеризации точек с использованием birch из sklearn-learn.

        @param[in] self (obj): The current object.
    	@param[in] points (list): the image represented by points.

    	@return (list) The label for everyone point.
    '''
    def clastering_points(self, points, params) -> []:
        # Создание и обучение объекта BIRCH
        birch1 = Birch(n_clusters=int(params[0]), branching_factor=int(params[1]), threshold=params[2],
            compute_labels=params[3], copy=params[4])
        birch1.fit(points)
        # Получение меток кластеров для каждой точки
        if params[3]:
            labels = birch1.labels_
        else:
            labels = birch1.predict(points)
        return labels


class ConcreteStrategyBIRCH_from_PYCLUSTERING(Strategy):
    '''
        @brief метод кластеризации пикселей с использованием birch из pyclustering.

        @param[in] self (obj): The current object.
    	@param[in] points (list): the image represented by pixels.

    	@return (list) The label for everyone point.
    '''
    def clastering_image(self, pixels, params: []) -> []:
        type = self.TYPE(params[9])
        instance = birch(data=pixels, number_clusters=int(params[0]), branching_factor=int(params[1]),
                         max_node_entries=int(params[5]), diameter=params[6], type_measurement=type,
                         entry_size_limit=int(params[7]), diameter_multiplier=params[8], ccore=params[10])
        instance.process()
        return np.array(self.clusters_to_labels(instance.get_clusters()))

    '''
        @brief метод кластеризации точек с использованием birch из pyclustering.

        @param[in] self (obj): The current object.
    	@param[in] points (list): the image represented by points.
    	@param[in] params (list): the parameters for clustering.

    	@return (list) The label for everyone point.
    '''
    def clastering_points(self, points, params):
        type = self.TYPE(params[9])
        instance = birch(data=points.tolist(), number_clusters=int(params[0]), branching_factor=int(params[1]),
                         max_node_entries=int(params[5]), diameter=params[6], type_measurement=type,
                         entry_size_limit=int(params[7]), diameter_multiplier=params[8], ccore=params[10])
        instance.process()
        return np.array(self.clusters_to_labels(instance.get_clusters()))

    '''
        @brief метод, определяющий тип метрики для birch из pyclustering.

        @param[in] self (obj): The current object.
    	@param[in] param (list): the index metric from mainwindow.py.

    	@return (measurement_type: int) The type metric.
    '''
    def TYPE(self, param):
        match param:
            case 'Euclidean':
                type = measurement_type.CENTROID_EUCLIDEAN_DISTANCE
            case 'Manhattan':
                type = measurement_type.CENTROID_MANHATTAN_DISTANCE
            case 'Inter':
                type = measurement_type.AVERAGE_INTER_CLUSTER_DISTANCE
            case 'Intra':
                type = measurement_type.AVERAGE_INTRA_CLUSTER_DISTANCE
            case 'Increase':
                type = measurement_type.VARIANCE_INCREASE_DISTANCE
            case _:
                type = measurement_type.CENTROID_EUCLIDEAN_DISTANCE
        return type


class ConcreteStrategyCURE(Strategy):

    '''
        @brief метод кластеризации пикселей с использованием cure из pyclustering.

        @param[in] self (obj): The current object.
    	@param[in] pixels (list): the image represented by points.

    	@return (list) The label for everyone point.
    '''
    def clastering_image(self, pixels, params: []) -> str:
        instance = cure(data=pixels, number_cluster=int(params[0]),
                        number_represent_points=int(params[11]), compression=params[12], ccore=params[10])
        instance.process()
        return np.array(self.clusters_to_labels(instance.get_clusters()))

    '''
        @brief метод кластеризации точек с использованием cure из pyclustering.

        @param[in] self (obj): The current object.
    	@param[in] points (list): the image represented by points.
    	@param[in] params (list): the parameters for clustering.

    	@return (list) The label for everyone point.
    '''
    def clastering_points(self, points, params):
        instance = cure(data=points.tolist(), number_cluster=int(params[0]),
                        number_represent_points=int(params[11]), compression=params[12], ccore=params[10])
        instance.process()
        return self.clusters_to_labels(instance.get_clusters())


class ConcreteStrategyROCK(Strategy):
    '''
        @brief метод кластеризации пикселей с использованием rock из pyclustering.

        @param[in] self (obj): The current object.
    	@param[in] pixels (list): the image represented by pixels.

    	@return (list) The label for everyone point.
    '''
    def clastering_image(self, pixels, params: []) -> str:
        instance = rock(data=pixels, eps=params[-1], number_clusters=int(params[0]), threshold=params[2], ccore=params[10])
        instance.process()
        labels = np.array(self.clusters_to_labels(instance.get_clusters()))
        return labels

    '''
        @brief метод кластеризации точек с использованием rock из pyclustering.

        @param[in] self (obj): The current object.
    	@param[in] points (list): the image represented by points.
    	@param[in] params (list): the parameters for clustering.

    	@return (list) The label for everyone point.
    '''
    def clastering_points(self, points,  params):
        instance = rock(data=points.tolist(), eps=params[-1], number_clusters=int(params[0]), threshold=params[2], ccore=params[10])
        instance.process()
        x = instance.get_clusters()
        labels = self.clusters_to_labels(x)
        return labels