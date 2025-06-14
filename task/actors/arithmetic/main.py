"""Применение заданий: арифметические исполнители."""

from type_b import TaskActorsArithmeticTypeB

task = TaskActorsArithmeticTypeB(False)
task.commands = {
        'A': lambda x: x - 1,
        'B': lambda x: x - 4,
        'C': lambda x: x // 2
    }
task.increasing = False
task.starting_number = 30
task.ending_number = 7
task.path_constraints.append(lambda path: ((16 in path) and not (12 in path)))
print(task)
solution = task.solve()
print(len(solution[0]))

# 