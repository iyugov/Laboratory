
from strategy import TaskGameTheoryStrategyStoneHeaps

def next_positions(position):
    a, b = position
    result = []
    for i in range(1, a):
        result.append((a - i, b))
    for i in range(1, b):
        result.append((a, b - i))
    #for i in range(1, min(a, b)):
    #    result.append((a - i, b - i))
    return tuple(result)

task = TaskGameTheoryStrategyStoneHeaps(False)
task.starting_position = (3, None)
task.solution_interval = (1, 150)
task.moves_count_range = (1, 6)
task.is_won = lambda x: x[0] == x[1] == 1
task.is_lost = lambda x: False
task.next_positions = next_positions
print(task)
print(task.solve())