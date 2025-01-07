
from strategy import TaskGameTheoryStrategyStoneHeaps

def next_positions(position):
    a, b = position
    result = []
    for i in range(4):
        for d in -1, +1:
            t = a + (i + 1) * d
            if abs(t - b) < abs(a - b):
                result.append((t, b))
            t = b + (i + 1) * d
            if abs(a - t) < abs(a - b):
                result.append((a, t))
    return tuple(result)

task = TaskGameTheoryStrategyStoneHeaps(False)
task.starting_position = (15, None)
task.solution_interval = (1, 100)
task.moves_count_range = (1, 4)
task.is_won = lambda x: x[0] == x[1]
task.is_lost = lambda x: False
task.next_positions = next_positions
print(task)
print(task.solve())