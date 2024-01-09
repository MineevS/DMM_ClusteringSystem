import os
import numpy as np
from sklearn.cluster import Birch
from PIL import Image
import matplotlib.pyplot as plt

os.environ.setdefault("LOKY_MAX_CPU_COUNT", str(3))

image = Image.open('Mona1.jpg')
image = np.array(image)


pixels = image.reshape((-1, 3))

# treshold максимальное расстояние между точками данных, чтобы они могли быть сгруппированы в один кластер
# n_clusters ожидаемое количество кластеров, которое алгоритм должен выделить из данных
birch = Birch(threshold=20, n_clusters=100)  
birch.fit(pixels)

labels = birch.labels_

segmented_image = labels.reshape(image.shape[:2])

plt.figure(figsize=(10, 5))
plt.subplot(121)
plt.title('Исходное изображение')
plt.imshow(image)

plt.subplot(122)
plt.title('Сегментированное изображение')
plt.imshow(segmented_image, cmap='tab20')

plt.show()
