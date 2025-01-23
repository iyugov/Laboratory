"""Применение заданий: комбинаторика."""

from subsequences import TaskCharSequenceTypeE

unique_solutions = set()
for file_number in range(381, 391):
    file_name = f'files/{file_number:04}.txt'
    unique_solution_ok = False
    task = None
    solution = None
    while not unique_solution_ok:
        task = TaskCharSequenceTypeE(True)
        solution = task.solve()
        unique_solution_ok = solution not in unique_solutions
    unique_solutions.add(solution)
    task.write_to_file(file_name)
    print(file_name, task.first_letter, task.second_letter,  solution, len(task.sequence))