"""Обработка числовых данных с сортировкой."""
from typing import List, Tuple

from task import Task

class SortingTypeA(Task):
    """Тип A: задача о деталях на ленте транспортёра.
    Есть N деталей, для каждой детали известны время шлифовки и окрашивания.
    Детали располагаются на ленте с N местами так:
    - все 2*N значений времени сортируются по возрастанию;
    - перебираются значения из полученного списка;
    - деталь с временем шлифовки помещается на первое свободное место с начала ленты;
    - деталь с временем окрашивания помещается на первое свободное место с конца ленты;
    - каждая деталь обрабатывается только один наз.
    Определить порядковый номер детали, которая будет обработана последней, и количество деталей,
    отшлифованных до неё."""

    items_count_min: int = 900
    """Минимальное значение количества элементов."""

    items_count_max: int = 1000
    """Максимальное значение количества элементов."""

    items_value_min: int = 1
    """Минимальное значение элемента."""

    items_value_max: int = 5000
    """Минимальное значение элемента."""

    items: List[Tuple[int, int]] = []
    """Значение делителя."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import randint, shuffle
        self.items_count = randint(self.items_count_min, self.items_count_max)
        raw_items = list(range(self.items_count_min, self.items_value_max + 1))
        shuffle(raw_items)
        raw_items = raw_items[: 2 * self.items_count]
        self.items = [(raw_items[i], raw_items[i + 1]) for i in range(0, len(raw_items), 2)]

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        self.__generate_raw()

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> Tuple[int, int]:
        """Решение задания."""
        data = []
        for i in range(len(self.items)):
            time_grinding, time_painting = self.items[i]
            data.append((min(time_grinding, time_painting), time_grinding < time_painting, i + 1))
        data.sort()
        part_start, part_end = [], []
        for _, grinding, number in data:
            (part_start if grinding else part_end).append(number)
        return data[-1][2], (len(part_start) - 1 if data[-1][1] else len(part_start))

    def __repr__(self) -> str:
        """Представление задания."""
        result = self.__doc__
        return result

    def write_to_file(self, file_name: str) -> None:
        """Запись данных в файл."""
        with open(file_name, 'w') as file_out:
            file_out.write(f'{len(self.items)}\n')
            for item in self.items:
                file_out.write(f'{item[0]} {item[1]}\n')

    def read_from_file(self, file_name: str) -> None:
        """Чтение данных из файла."""
        with open(file_name, 'r') as file_in:
            items_count = int(file_in.readline())
            self.items = []
            for i in range(items_count):
                item = file_in.readline().split()
                self.items.append((int(item[0]), int(item[1])))