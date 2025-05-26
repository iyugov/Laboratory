"""Применение заданий: арифметические исполнители."""

from random import randint

from type_b import TaskActorsArithmeticTypeB

task = TaskActorsArithmeticTypeB(False)
task.starting_number = 10
task.ending_number = 61
a = 15
b = 50
task.path_constraints.append(lambda path: ((a in path) or not (b in path)))
print(task)
print(a, b)
solution = task.solve()
# print(solution[0])
# print(solution[1])
print(len(solution[0]))
# print(len(solution[1]))

# 