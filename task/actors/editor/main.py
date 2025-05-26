"""Применение заданий: десятичные исполнители."""

from type_b import TaskActorsEditorTypeB

for _ in range(30):
    print('=' * 40)
    task = TaskActorsEditorTypeB(True)
    print(task)
    solution = task.solve()
    print(solution, sum(solution), sum(k * x for k, x in enumerate(solution, 1)))
    print('=' * 40)