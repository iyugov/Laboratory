"""Задания: арифметические исполнители, тип A."""
from typing import Callable, Dict, List
from task import Task


class TaskActorsArithmeticTypeA(Task):
    """Задание: дан набор команд действий над числами.
    Определить самую короткую программу, преобразующую число A в число B."""

    commands: Dict[str, Callable] = {
        '1': lambda x: x - 9,
        '2': lambda x: int(x**0.5) if x > 0 and int(x**0.5)**2 == x else None
    }
    """Команды для изменения числа."""

    number_min: int = 1
    """Минимальное возможное значение для A и B."""

    number_max: int = 1000
    """Максимальное возможное значение для A и B."""

    starting_number: int = 2
    """Начальное число (A)."""

    ending_number: int = 6
    """Конечное число (B)."""

    program_length_min: int = 4
    """Минимальная длина программы."""

    program_length_max: int = 7
    """Максимальная длина программы."""

    program_length_max_search_limit: int = 10
    """Максимальная длина программы (ограничение поиска)."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__()
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без проверки."""
        from random import randint
        self.starting_number = randint(self.number_min, self.number_max)
        self.ending_number = randint(self.number_min, self.number_max)

    def __generate(self) -> None:
        """Генерация задания с проверкой."""
        solution_ok = False
        while not solution_ok:
            self.__generate_raw()
            solution = self.solve()
            if len(solution) != 1:
                continue
            solution = solution[0]
            if not all(solution.count(opcode) > 1 for opcode in self.commands):
                continue
            solution_ok = self.program_length_min <= len(solution) <= self.program_length_max

    def generate(self) -> None:
        """Генерирует параметры условия."""
        self.__generate()

    def solve(self) -> List[str]:
        """Решает задание."""
        from collections import deque
        result = []
        queue = deque([(self.starting_number, '')])
        visited = {self.starting_number}
        while queue:
            current_number, program = queue.popleft()
            if current_number == self.ending_number:
                result.append(program)
                continue
            if len(program) == self.program_length_max_search_limit:
                continue
            for opcode, command in self.commands.items():
                next_number = command(current_number)
                if next_number is not None:
                    visited.add(next_number)
                    queue.append((next_number, program + opcode))
        if not result:
            return []
        min_length = min(len(program) for program in result)
        result = [program for program in result if len(program) == min_length]
        return result

    def __repr__(self) -> str:
        """Представление задания."""
        result = 'Заданы команды преобразования числа.\n'
        a, b = self.starting_number, self.ending_number
        result += f'Определить самую короткую программу, преобразующую число {a} в число {b}.'
        return result

