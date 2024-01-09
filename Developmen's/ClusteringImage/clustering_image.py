import cv2
import numpy as np
from sklearn.cluster import Birch, AgglomerativeClustering
import json
from pyclustering.cluster import rock
import time


def rock_clustering_image(X, config):
    radius = config.get("radius", 1.0)
    n_clusters = config.get("n_clusters", 2)
    threshold = config.get("threshold", 0.5)
    return rock.rock(X, radius, n_clusters, threshold, ccore=True)


def birch_clustering_image(config):
    threshold = config.get("threshold", 20)
    n_clusters = config.get("n_clusters", 2)
    return Birch(threshold=threshold, n_clusters=n_clusters)


def cure_clustering_image(config):
    n_clusters = config.get("n_clusters", 2)
    linkage = config.get("linkage", "complete")
    affinity = config.get("affinity", "euclidean")
    return AgglomerativeClustering(
        n_clusters=n_clusters, linkage=linkage, affinity=affinity
    )


def clustering_image(image_path, config_path):
    with open(config_path, "r") as f:
        config = json.load(f)

    algorithm = config.get("algorithm", "rock")

    image = cv2.imread(image_path)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    coords_and_colors = [
        (x, y, hsv_image[y, x])
        for y in range(hsv_image.shape[0])
        for x in range(hsv_image.shape[1])
    ]

    # X = np.array([[round(h)] for (_, _, (h, _, _)) in coords_and_colors])
    X = np.array([[round(h), round(s), round(v)] for (_, _, (h, s, v)) in coords_and_colors])


    if algorithm == "birch":
        clustering_algorithm = birch_clustering_image(config.get("birch", {}))
    elif algorithm == "cure":
        clustering_algorithm = cure_clustering_image(config.get("cure", {}))
    elif algorithm == "rock":
        start = time.time()
        clustering_algorithm = rock_clustering_image(X, config.get("rock", {}))
    else:
        raise ValueError(
            "Неподдерживаемый алгоритм кластеризации. Поддерживаются 'birch', 'cure' и 'random_projection'."
        )

    if algorithm == "rock":
        clustering_algorithm.process()
        end = time.time()

        print(
            "The time of execution of rock is :",
            (end - start) * 10 ** 3,
            "ms",
        )

        clusters = clustering_algorithm.get_clusters()
        labels = [0] * len(X)
        for cluster_id, cluster in enumerate(clusters):
            for index in cluster:
                labels[index] = cluster_id
    else:
        clustering_algorithm.fit(X)
        labels = clustering_algorithm.labels_

    colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
    ]

    clustered_image = np.zeros_like(image)
    for index, (x, y, _) in enumerate(coords_and_colors):
        clustered_image[y, x] = colors[labels[index] % len(colors)]

    output_path = "clustered_{}_{}".format(algorithm, image_path.split("/")[-1])
    cv2.imwrite(output_path, clustered_image)

    return {"output_path": output_path}


config_path = "config.json"
clustering_image("small.jpg", config_path)
