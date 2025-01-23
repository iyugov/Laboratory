"""Применение заданий: логика."""
from digits import TaskNumeralSystemsFindDigitsInSum

task = TaskNumeralSystemsFindDigitsInSum(True)
print(task)
print(task.formula_for_editor())
solution = task.solve()
print(solution)
print(min(solution), max(solution))