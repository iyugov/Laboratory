"""Применение заданий: двоичные исполнители."""

from type_a import TaskActorsBinaryTypeA

tasks_count = 100
file_name = 'tasks.txt'

# Генерация заданий
unique_targets = set()
for task_index in range(1, tasks_count + 1):
    target_ok = False
    task = None
    while not target_ok:
        task = TaskActorsBinaryTypeA(True)
        if task.target in unique_targets:
            continue
        unique_targets.add(task)
        target_ok = True
    solution = task.solve()
    print(task_index)
    print(task)
    print(solution)
    print()
    with open(file_name, 'a') as out_file:
        out_file.write(str(task_index) + '\n')
        out_file.write(str(task) + '\n')
        out_file.write(str(solution) + '\n\n')
