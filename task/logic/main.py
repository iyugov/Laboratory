"""Применение заданий: логика."""
from truth_table import TaskLogicTruthTableMatchColumnsAndVariables

tasks_count = 100
file_name = 'tasks.txt'

# Генерация заданий
for task_index in range(1, tasks_count + 1):
    task = TaskLogicTruthTableMatchColumnsAndVariables()
    task.solutions_count_min = 1
    task.solutions_count_max = 1
    task.same_result_in_rows = False
    task.generate()
    solution = task.solve()
    print(task_index)
    print(task)
    print(solution)
    print()
    with open(file_name, 'a') as out_file:
        out_file.write(str(task_index) + '\n')
        out_file.write(str(task) + '\n')
        out_file.write(str(solution) + '\n\n')