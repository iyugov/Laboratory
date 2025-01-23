"""Применение заданий: двоичные исполнители."""

from type_d import TaskActorsBinaryTypeD

unique_solutions = set()
while len(unique_solutions) < 10:
    task = TaskActorsBinaryTypeD(True)
    solution = task.solve()
    if solution in unique_solutions:
        continue
    unique_solutions.add(solution)
    print(task.target, solution)