"""Применение заданий: двоичные исполнители."""

from type_c import TaskActorsBinaryTypeC

solution_set = set()
while True:
    task = TaskActorsBinaryTypeC(True)

    solution = task.solve()
    if solution not in solution_set:
        print(task)
        print(solution)
        solution_set.add(solution)
