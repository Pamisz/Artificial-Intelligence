import numpy as np


def initialize_centroids_forgy(data, k):
    centroid_indices = np.random.choice(len(data), size=k, replace=False)
    centroids = data[centroid_indices]
    return np.array(centroids)


def initialize_centroids_kmeans_pp(data, k):
    centroids = [data[np.random.randint(len(data))]]
    for _ in range(1, k):
        distances = np.array([min(np.linalg.norm(centroid - point) for centroid in centroids) for point in data])
        new_centroid = data[np.argmax(distances)]
        centroids.append(new_centroid)
    return np.array(centroids)


def assign_to_cluster(data, centroids):
    assignments = [np.argmin([np.linalg.norm(point - centroid) for iter, centroid in enumerate(centroids)]) for point in data]
    return np.array(assignments)

def update_centroids(data, assignments):
    new_centroids = []
    for i in np.unique(assignments):
        new_centroid = np.mean(data[assignments == i], axis=0)
        new_centroids.append(new_centroid)
    return np.array(new_centroids)


def mean_intra_distance(data, assignments, centroids):
    return np.sqrt(np.sum((data - centroids[assignments, :]) ** 2))


def k_means(data, num_centroids, kmeansplusplus=False):
    # centroids initizalization
    if kmeansplusplus:
        centroids = initialize_centroids_kmeans_pp(data, num_centroids)
    else:
        centroids = initialize_centroids_forgy(data, num_centroids)

    assignments = assign_to_cluster(data, centroids)
    for i in range(100):  # max number of iteration = 100
        print(f"Intra distance after {i} iterations: {mean_intra_distance(data, assignments, centroids)}")
        centroids = update_centroids(data, assignments)
        new_assignments = assign_to_cluster(data, centroids)
        if np.all(new_assignments == assignments):  # stop if nothing changed
            break
        else:
            assignments = new_assignments

    return new_assignments, centroids, mean_intra_distance(data, new_assignments, centroids)
