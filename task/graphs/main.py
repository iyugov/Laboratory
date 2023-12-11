"""Применение заданий: графы."""

from match import TaskGraphsMatchTable

task = TaskGraphsMatchTable(False)
task.edges = 'ab bc cd dh hg gf fe ea bf cg af fc gd'
task.weighted = False
task.solve_for_vertices = 'af'
task.bad_edge_present = True
task.generate()
print(task)
print(task.solve())
