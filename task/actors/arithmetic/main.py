"""Применение заданий: арифметические исполнители."""

from random import randint

from type_b import TaskActorsArithmeticTypeB

task = TaskActorsArithmeticTypeB(False)
task.starting_number = randint(1, 10)
task.ending_number = randint(50, 150)
a = randint(10, 20)
b = randint(40, 50)
task.path_constraints.append(lambda path: (a in path) and (b in path))
print(task)
print(a, b)
solution = task.solve()
# print(solution[0])
# print(solution[1])
print(len(solution[0]))
# print(len(solution[1]))