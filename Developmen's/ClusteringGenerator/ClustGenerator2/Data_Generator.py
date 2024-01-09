import pandas as pd
import numpy as np

def generate_data(dimensions, distribution_type, num_vectors, params=None):
    data = None

    if distribution_type == 'Нормальное':
        mean = params.get('mean', 0)
        std_dev = params.get('std_dev', 1)
        data = np.random.normal(mean, std_dev, size=(num_vectors, dimensions))
    elif distribution_type == 'Показательное':
        scale = params.get('scale', 1)
        data = np.random.exponential(scale, size=(num_vectors, dimensions))
    elif distribution_type == 'Биноминальное':
        n = params.get('n', 10)
        p = params.get('p', 0.5)
        data = np.random.binomial(n, p, size=(num_vectors, dimensions))
    elif distribution_type == 'Равномерное':
        low = params.get('low', 0)
        high = params.get('high', 1)
        data = np.random.uniform(low, high, size=(num_vectors, dimensions))
    elif distribution_type == 'Гамма':
        shape = params.get('shape', 2)
        scale = params.get('scale', 1)
        data = np.random.gamma(shape, scale, size=(num_vectors, dimensions))
    else:
        print("Неподдерживаемый тип распределения")
        return

    return pd.DataFrame(data, columns=[f'Feature_{i + 1}' for i in range(dimensions)])

def save_to_file(dataset, file_name='generated_data.xlsx', file_format='excel'):
    if file_format == 'excel':
        dataset.to_excel(file_name, index=False)
        print(f"Данные сохранены в файл '{file_name}'")
    elif file_format == 'csv':
        dataset.to_csv(file_name, index=False)
        print(f"Данные сохранены в файл '{file_name}'")
    # Добавьте поддержку других форматов сохранения по необходимости

dimensions = int(input("Введите размерность (число фичей): "))
distribution_type = input("Введите тип распределения (Нормальное, Показательное, Биноминальное, Равномерное, Гамма): ").capitalize()
num_vectors = int(input("Введите количество векторов (точек): "))

# Дополнительные параметры для различных распределений (можно настроить по умолчанию или позволить пользователю вводить)
distribution_params = {}
if distribution_type == 'Нормальное':
    distribution_params['mean'] = float(input("Введите среднее значение: "))
    distribution_params['std_dev'] = float(input("Введите стандартное отклонение: "))
elif distribution_type == 'Показательное':
    distribution_params['scale'] = float(input("Введите параметр масштаба: "))
elif distribution_type == 'Биноминальное':
    distribution_params['n'] = int(input("Введите n (число экспериментов): "))
    distribution_params['p'] = float(input("Введите p (вероятность успеха): "))
elif distribution_type == 'Равномерное':
    distribution_params['low'] = float(input("Введите нижнюю границу: "))
    distribution_params['high'] = float(input("Введите верхнюю границу: "))
elif distribution_type == 'Гамма':
    distribution_params['shape'] = float(input("Введите параметр формы (shape): "))
    distribution_params['scale'] = float(input("Введите параметр масштаба (scale): "))

generated_dataset = generate_data(dimensions, distribution_type, num_vectors, params=distribution_params)

if generated_dataset is not None:
    save_format = input("Выберите формат сохранения (Excel, CSV): ").lower()
    save_to_file(generated_dataset, file_format=save_format)
