"""Применение заданий: перебор чисел."""

from divisors import TaskRangeIterationTypeA

task = TaskRangeIterationTypeA(True)

print(task)
solution = task.solve()
for a, b in solution:
    print(a, b)