"""Применение заданий: графы."""

from match import TaskGraphsMatchTable

task = TaskGraphsMatchTable(False)
task.edges = 'AB AC BC BE CD CF DG EF FG FH GH'
task.weighted = True
# task.solve_for_vertices = 'DE'
task.solve_for_weights_sum = ('FG', )
task.constraints = ('AC > EF', )
# task.solve_for_shortest_distance = 'AF'
task.solution_count_min = 1
task.solution_count_max = 1
task.bad_edge_present = False
task.generate()
print(task.graph_signature())
print(task)
print(task.solve())
# task.draw_graph()