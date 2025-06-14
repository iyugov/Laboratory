"""Применение заданий: комбинаторика."""

from subsequences import TaskCharSequenceTypeG

for file_number in range(401, 411):
    file_name = f'{file_number:04}.txt'
    solution_ok = False
    while not solution_ok:
        task = TaskCharSequenceTypeG(True)
        solution1 = task.solve(method='regexp')
        solution2 = task.solve(method='iteration')
        solution_ok = solution1 == solution2
        task.write_to_file(file_name)
        print(f'{file_number:04}.txt: {task.parity_of_digit} {task.letter_for_count} {task.letter_count}: {solution1}')
