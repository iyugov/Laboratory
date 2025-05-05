"""Задания: арифметические исполнители, тип B."""
from typing import Callable, Dict, List, Tuple
from task import Task


class TaskActorsArithmeticTypeB(Task):
    """Задание: дан набор команд действий над числами.
    Определить количество программ, преобразующих число A в число B."""

    commands: Dict[str, Callable] = {
        'A': lambda x: x + 1,
        'B': lambda x: x * 2
    }
    """Команды для изменения числа."""

    starting_number_min: int = 1
    """Минимальное возможное значение для A."""

    starting_number_max: int = 5
    """Максимальное возможное значение для A."""

    starting_number: int = 1
    """Начальное число (A)."""

    ending_number_min: int = 10
    """Минимальное возможное значение для B."""

    ending_number_max: int = 20
    """Максимальное возможное значение для B."""

    ending_number: int = 10
    """Конечное число (B)."""

    increasing: bool = True
    """Увеличение числа (True) или уменьшение (False)."""

    program_constraints: List[Callable] = []
    """Ограничения на программу."""

    path_constraints: List[Callable] = []
    """Ограничения на путь."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__()
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без проверки."""
        from random import randint
        self.starting_number = randint(self.starting_number_min, self.starting_number_max)
        self.ending_number = randint(self.ending_number_min, self.ending_number_max)

    def __generate(self) -> None:
        """Генерация задания с проверкой."""
        solution_ok = False
        while not solution_ok:
            self.__generate_raw()
            solution = self.solve()
            if len(solution[0]) == 0:
                continue
            solution_ok = True

    def generate(self) -> None:
        """Генерирует параметры условия."""
        self.__generate()

    def solve(self) -> Tuple[List[str], List[List[int]]]:
        """Решает задание."""
        def make_programs(current: int, target: int, current_programs: List[str], current_paths: List[List[int]], program_prefix: str, path_prefix: List[int], increasing: bool) -> None:
            """Рекурсивная функция для генерации программ."""
            if current == target:
                if all(constraint(program_prefix) for constraint in self.program_constraints) and all(constraint(path_prefix) for constraint in self.path_constraints):
                    current_programs.append(program_prefix)
                    current_paths.append(path_prefix)
                return
            for command in self.commands:
                next_value = self.commands[command](current)
                if next_value <= target and increasing or next_value >= target and not increasing:
                    make_programs(next_value, target, current_programs, current_paths, program_prefix + command,  path_prefix + [next_value], increasing)

        programs = []
        paths = []
        make_programs(self.starting_number, self.ending_number, programs, paths, '', [self.starting_number], self.increasing)
        return programs, paths

    def __repr__(self) -> str:
        """Представление задания."""
        result = 'Заданы команды преобразования числа.\n'
        a, b = self.starting_number, self.ending_number
        result += f'Определить программы, преобразующие число {a} в число {b}.'
        return result

