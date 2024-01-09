"""@package main_script.py
    Этот скрипт представляет собой программу на языке Python для генерации синтетических данных с использованием различных функций из библиотеки scikit-learn,
     а также для сохранения данных в файл CSV и построения графика для визуализации данных.
"""

# main_script.py

import argparse
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs, make_circles, make_moons


def generate_blobs(n_samples, n_features, centers, cluster_std=1.0, center_box=(-10.0, 10.0), shuffle=True,
                   random_state=None, return_centers=False):
    """
    Генерация данных с использованием make_blobs.

    Args:
        n_samples (int): Число точек данных.
        n_features (int): Количество фич.
        centers (int): Количество центров (кластеров), которые будут созданы.
        cluster_std (float, optional): Стандартное отклонение кластеров. По умолчанию 1.0.
        center_box (tuple, optional): Границы для каждого центра кластера. По умолчанию (-10.0, 10.0).
        shuffle (bool, optional): Перемешивать точки данных. По умолчанию True.
        random_state (int, optional): Состояние генератора случайных чисел для воспроизводимости. По умолчанию None.
        return_centers (bool, optional): Возвращать центры кластеров в дополнение к точкам данных. По умолчанию False.

    Returns:
        tuple: Данные X и метки y (или X, y, centers, если return_centers=True).
    """
    center_box = tuple(center_box)
    X, y = make_blobs(
        n_samples=n_samples,
        n_features=n_features,
        centers=centers,
        cluster_std=cluster_std,
        center_box=center_box,
        shuffle=shuffle,
        random_state=random_state,
        return_centers=return_centers
    )
    return X, y


def generate_circles(n_samples, shuffle=True, noise=None, random_state=None, factor=0.8):
    """
    Генерация данных с использованием make_circles.

    Args:
        n_samples (int): Число точек данных.
        shuffle (bool, optional): Перемешивать точки данных. По умолчанию True.
        noise (float, optional): Стандартное отклонение (разброс данных) гауссовского шума. По умолчанию None.
        random_state (int, optional): Состояние генератора случайных чисел для воспроизводимости. По умолчанию None.
        factor (float, optional): Масштабный коэффициент между внутренним и внешним кругом. По умолчанию 0.8.

    Returns:
        tuple: Данные X и метки y.
    """
    X, y = make_circles(
        n_samples=n_samples,
        shuffle=shuffle,
        noise=noise,
        random_state=random_state,
        factor=factor
    )
    return X, y


def generate_moons(n_samples, shuffle=True, noise=None, random_state=None):
    """
    Генерация данных с использованием make_moons.

    Args:
        n_samples (int): Число точек данных.
        shuffle (bool, optional): Перемешивать точки данных. По умолчанию True.
        noise (float, optional): Стандартное отклонение (разброс данных) гауссовского шума. По умолчанию None.
        random_state (int, optional): Состояние генератора случайных чисел для воспроизводимости. По умолчанию None.

    Returns:
        tuple: Данные X и метки y.
    """
    X, y = make_moons(
        n_samples=n_samples,
        shuffle=shuffle,
        noise=noise,
        random_state=random_state
    )
    return X, y


def save_to_csv(X, output_file):
    """
    Сохранение данных в CSV файл.

    Args:
        X (numpy.ndarray): Данные.
        output_file (str): Имя выходного CSV файла.
    """
    if X.shape[1] == 1:
        df = pd.DataFrame(data={'1 feature': X[:, 0]})
    elif X.shape[1] == 2:
        df = pd.DataFrame(data={'1 feature': X[:, 0], '2 feature': X[:, 1]})
    elif X.shape[1] > 2:
        df = pd.DataFrame(data={f'{i+1} feature': X[:, i] for i in range(X.shape[1])})
    df.to_csv(output_file, index=False)
    print(f'Data saved to {output_file}')


def plot_data(X, y, title, output_image):
    """
    Построение графика.

    Args:
        X (numpy.ndarray): Данные.
        y (numpy.ndarray): Метки классов.
        title (str): Заголовок графика.
        output_image (str): Имя выходного JPG изображения.
    """
    fig = plt.figure()

    if X.shape[1] == 1:
        ax = fig.add_subplot(121)
        ax.scatter(X[:, 0], [0] * len(X), c=y, cmap='viridis', edgecolors='k', s=50)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        ax = fig.add_subplot(122, projection='3d')
        ax.scatter(X[:, 0], [0] * len(X), [0] * len(X), c=y, cmap='viridis', edgecolors='k', s=50)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

    if X.shape[1] == 2:
        ax = fig.add_subplot(121)
        ax.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis', edgecolors='k', s=50)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        ax = fig.add_subplot(122, projection='3d')
        ax.scatter(X[:, 0], X[:, 1], [0] * len(X), c=y, cmap='viridis', edgecolors='k', s=50)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

    if X.shape[1] > 2:
        ax = fig.add_subplot(121)
        ax.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis', edgecolors='k', s=50)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        ax = fig.add_subplot(122, projection='3d')
        ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=y, cmap='viridis', edgecolors='k', s=50)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

    plt.title(title)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.savefig(output_image, format='jpeg')
    print(f'Image saved to {output_image}')


def main():
    """
    Основная функция скрипта.

    Пример использования:

        python main_script.py --data make_blobs  --samples 150 --features 2 --clusters 4 --cluster_std 1 --output blobs_data.csv --output_image blobs_plot.jpg

        python main_script.py --data make_circles --samples 150 --noise 0 --output circles_data.csv --output_image circles_plot.jpg

        python main_script.py --data make_moons --samples 150 --noise 0 --output moons_data.csv --output_image moons_plot.jpg
    """
    X, y, title = None, None, None

    parser = argparse.ArgumentParser(description='Скрипт генерации данных')
    parser.add_argument('--data', type=str, metavar='str', choices=['make_blobs', 'make_circles', 'make_moons'], required=True,
                        help='Тип данных для генерации: make_blobs, make_circles или make_moons.')
    parser.add_argument('--samples', type=int, metavar='int', default=300, help='Число точек данных')
    parser.add_argument('--features', type=int, metavar='int', default=2, help='Количество фич')
    parser.add_argument('--clusters', type=int, metavar='int', default=4, help='Количество центров (кластеров), которые будут созданы (для make_blobs)')
    parser.add_argument('--cluster_std', type=float, metavar='float', default=1.0, help='Стандартное отклонение кластеров (для make_blobs)')
    parser.add_argument('--center_box', type=float, nargs=2, metavar=' float (min max)', default=(-10.0, 10.0),
                        help='Границы для каждого центра кластера (для make_blobs)')
    parser.add_argument('--shuffle', type=bool, metavar='bool', default=True, help='Перемешивать точки данных')
    parser.add_argument('--random_state', type=int, metavar='int', default=None,
                        help='Состояние генератора случайных чисел для воспроизводимости')
    parser.add_argument('--return_centers', type=bool, metavar='bool', default=False,
                        help='Возвращать центры кластеров в дополнение к точкам данных (для make_blobs)')
    parser.add_argument('--noise', type=float, metavar='float', default=None,
                        help='Стандартное отклонение (разброс данных) гауссовского шума (для make_circles, make_moons)')
    parser.add_argument('--factor', type=float, metavar='float', default=0.8,
                        help='Масштабный коэффициент между внутренним и внешним кругом (для make_circles)')
    parser.add_argument('--output', type=str, metavar='str', default='generated_data.csv', help='Имя выходного CSV файла')
    parser.add_argument('--output_image', type=str, metavar='str', default='data_plot.jpg', help='Имя выходного JPG изображения')

    args = parser.parse_args()

    match args.data:
        case 'make_blobs':
            X, y = generate_blobs(
                args.samples,
                args.features,
                args.clusters,
                cluster_std=args.cluster_std,
                center_box=args.center_box,
                shuffle=args.shuffle,
                random_state=args.random_state,
                return_centers=args.return_centers
            )
            title = 'Blobs Data'

        case 'make_circles':
            X, y = generate_circles(
                args.samples,
                shuffle=args.shuffle,
                noise=args.noise,
                random_state=args.random_state,
                factor=args.factor
            )
            title = 'Circles Data'

        case 'make_moons':
            X, y = generate_moons(
                args.samples,
                shuffle=args.shuffle,
                noise=args.noise,
                random_state=args.random_state
            )
            title = 'Moons Data'

    save_to_csv(X, args.output)
    plot_data(X, y, title, args.output_image)


if __name__ == '__main__':
    main()
