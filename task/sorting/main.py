"""Применение заданий: Обработка числовых данных с сортировкой."""

from sorting import SortingTypeA

for file_number in range(756, 776):
    file_name = f'{file_number:04}.txt'
    task = SortingTypeA(True)
    task.write_to_file(file_name)
    solution = task.solve()
    print(file_name, solution[0], solution[1])
