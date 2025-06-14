
from strategy import TaskGameTheoryStrategyStoneHeaps

task = TaskGameTheoryStrategyStoneHeaps(False)
task.starting_position = (None, )
task.solution_interval = (1, 3000)
task.moves_count_range = (1, 6)
task.is_won = lambda x: x[0] <= 64
task.is_lost = lambda x: False
task.next_positions = lambda position: ((position[0] - 3,), (position[0] - 7,), (position[0] // 3, ))
print(task)
print(task.solve())