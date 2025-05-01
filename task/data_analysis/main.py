"""Применение заданий: кластеризация."""

from clusterization import TaskClusterization

for file_number in range(0, 0):
    file_name = f'{file_number:04}.txt'
    clusters_ok = False
    task = None
    clusters = None
    solution = {}
    while not clusters_ok:
        task = TaskClusterization(True)
        clusters = task.clusterize_for_clusters_count()
        clusters_ok = all(len(cluster) >= 400 for cluster in clusters)
        if not clusters_ok:
            continue
        solution = task.solve()
        clusters_ok = clusters_ok and all(all(coordinate > 0 for coordinate in point) for point in solution['anticenters'])
    task.write_data_to_file(file_name)

    print(file_name, solution['sizes'], solution['anticenters_multiplied'])
