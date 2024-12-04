"""Применение заданий: обработка строк."""

from parentheses import TaskStringsParenthesesLongestValid

def generate_and_solve(file_number_min: int, file_number_max: int) -> None:
    solutions_set = set()
    for file_number in range(file_number_min, file_number_max + 1):
        file_name = f'{file_number:04}.txt'
        task = None
        solution = None
        solution_ok = False
        while not solution_ok:
            task = TaskStringsParenthesesLongestValid(True)
            solution = task.solve()
            solution_ok = solution not in solutions_set
        solutions_set.add(solution)
        task.save_to_file(file_name)
        print(file_name, solution)

