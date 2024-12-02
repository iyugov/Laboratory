from task.data_analysis.clusterization import TaskClusterization

clusters_ok = False
task = None
clusters = None
while not clusters_ok:
    task = TaskClusterization(True)
    clusters = task.clusterize_for_clusters_count()
    clusters_ok = all(len(cluster) >= 400 for cluster in clusters)
task.write_data_to_file('points_data.txt')
print(task)
print(task.solve())
task.visualize(clusters)