@Author
		Komintsev N. V. [nikita.comin@gmail.com]
# Генератор данных для кластеризации: создает и визуализирует точки для трех различных форм распределения - кластеры, вложенные круги и полукруги.


## Оглавление

- [Описание](#description)
- [Функции](#functions)
- [Пример использования](#usage)

# Реализация алгоритмов кластеризации <a name="description"></a>

Этот репозиторий содержит скрипт на языке Python для генерации синтетических данных с использованием различных функций из библиотеки scikit-learn. Программа также предоставляет возможность сохранения данных в файл CSV и построения графика для визуализации данных.


## Функции <a name="functions"></a>

### `generate_blobs(n_samples, n_features, centers, cluster_std=1.0, center_box=(-10.0, 10.0), shuffle=True, random_state=None, return_centers=False)`

Генерация данных с использованием make_blobs.

Аргументы:
- `n_samples` (int): Число точек данных.
- `n_features` (int): Количество фич.
- `centers` (int): Количество центров (кластеров), которые будут созданы.
- `cluster_std` (float, optional): Стандартное отклонение кластеров. По умолчанию 1.0.
- `center_box` (tuple, optional): Границы для каждого центра кластера. По умолчанию (-10.0, 10.0).
- `shuffle` (bool, optional): Перемешивать точки данных. По умолчанию True.
- `random_state` (int, optional): Состояние генератора случайных чисел для воспроизводимости. По умолчанию None.
- `return_centers` (bool, optional): Возвращать центры кластеров в дополнение к точкам данных. По умолчанию False.

Возвращает:
- tuple: Данные X и метки y (или X, y, centers, если return_centers=True).

### `generate_circles(n_samples, shuffle=True, noise=None, random_state=None, factor=0.8)`

Генерация данных с использованием make_circles.

Аргументы:
- `n_samples` (int): Число точек данных.
- `shuffle` (bool, optional): Перемешивать точки данных. По умолчанию True.
- `noise` (float, optional): Стандартное отклонение (разброс данных) гауссовского шума. По умолчанию None.
- `random_state` (int, optional): Состояние генератора случайных чисел для воспроизводимости. По умолчанию None.
- `factor` (float, optional): Масштабный коэффициент между внутренним и внешним кругом. По умолчанию 0.8.

Возвращает:
- tuple: Данные X и метки y.

### `generate_moons(n_samples, shuffle=True, noise=None, random_state=None)`

Генерация данных с использованием make_moons.

Аргументы:
- `n_samples` (int): Число точек данных.
- `shuffle` (bool, optional): Перемешивать точки данных. По умолчанию True.
- `noise` (float, optional): Стандартное отклонение (разброс данных) гауссовского шума. По умолчанию None.
- `random_state` (int, optional): Состояние генератора случайных чисел для воспроизводимости. По умолчанию None.

Возвращает:
- tuple: Данные X и метки y.

### `save_to_csv(X, output_file)`

Сохранение данных в CSV файл.

Аргументы:
- `X` (numpy.ndarray): Данные.
- `output_file` (str): Имя выходного CSV файла.

### `plot_data(X, y, title, output_image)`

Построение графика.

Аргументы:
- `X` (numpy.ndarray): Данные.
- `y` (numpy.ndarray): Метки классов.
- `title` (str): Заголовок графика.
- `output_image` (str): Имя выходного JPG изображения.

### `main()`

Основная функция скрипта.

## Пример использования: <a name="usage"></a>

```bash
python main_script.py --data make_blobs  --samples 150 --features 2 --clusters 4 --cluster_std 1
```
![blobs_plot](https://github.com/Nikita-Komintsev/Clustering-Data-Generator/assets/70846416/cc1ebb7d-0e0e-4a5f-a6ef-0c03eb008726)
```bash
python main_script.py --data make_circles --samples 150 --noise 0
```
![circles_plot](https://github.com/Nikita-Komintsev/Clustering-Data-Generator/assets/70846416/ec330a47-bd21-4625-b0f6-0c3f5011c8e7)
```bash
python main_script.py --data make_moons --samples 150 --noise 0
```
![moons_plot](https://github.com/Nikita-Komintsev/Clustering-Data-Generator/assets/70846416/48bf868c-2281-4eff-b7ae-a7c81cdceadd)
