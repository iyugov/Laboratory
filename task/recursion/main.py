"""Применение заданий: десятичные исполнители."""

from functions_big import TaskRecursionFunctionsBigTypeC

task = TaskRecursionFunctionsBigTypeC(True)
task.term1 = 48
task.term2 = 63
task.recursion_limit = 9983
print(task)
print(task.solve())


