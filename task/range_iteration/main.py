"""Применение заданий: перебор чисел."""

from divisors import TaskRangeIterationTypeB

task = TaskRangeIterationTypeB(True)
print(task)
solution = task.solve()
for a, b in solution:
    print(a, b)