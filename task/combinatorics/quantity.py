"""Задания: комбинаторика, количество комбинаторных объектов."""
from typing import Tuple, Callable

from task import Task

class TaskCombinatoricsQuantityTypeA(Task):
    """Задание: определить количество цифровых кодов заданной длины из заданного набора цифр
    (допускаются ведущие нули), соответствующих заданным условиям."""

    digit_value_lower_bound: int = 1
    """Нижняя граница значения цифры."""

    digit_value_upper_bound: int = 9
    """Верхняя граница значения цифры."""

    digit_value_count_min: int = 4
    """Минимальное количество цифр."""

    digit_value_count_max: int = 6
    """Максимальное количество цифр."""

    digit_value_min: int = 0
    """Минимальное значение цифры."""

    digit_value_max: int = 9
    """Максимальное значение цифры."""

    digit_count_min: int = 4
    """Минимальное количество цифр."""

    digit_count_max: int = 6
    """Максимальное количество цифр."""

    digit_count: int = 0
    """Количество цифр."""

    conditions: Tuple[Callable] = (
        lambda s: len([x for x in s if int(x) % 2 == 0]) <= len([x for x in s if int(x) % 2 != 0]),
        lambda s: s.count('5') == 1
    )
    """Условия задания."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import randint
        range_ok = False
        while not range_ok:
            self.digit_value_min = randint(self.digit_value_lower_bound, self.digit_value_upper_bound)
            self.digit_value_max = randint(self.digit_value_lower_bound, self.digit_value_upper_bound)
            digit_value_count = self.digit_value_max - self.digit_value_min + 1
            range_ok = self.digit_value_count_min <= digit_value_count <= self.digit_value_count_max
        self.digit_count = randint(self.digit_count_min, self.digit_count_max)

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        self.__generate_raw()

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> int:
        """Решение задания."""
        from itertools import product
        count = 0
        for digits in product(range(self.digit_value_min, self.digit_value_max + 1), repeat=self.digit_count):
            digits_str = ''.join(map(str, digits))
            if all([condition(digits_str) for condition in self.conditions]):
                count += 1
        return count

    def __repr__(self) -> str:
        """Представление задания."""
        result = f'Задание: определить количество цифровых кодов длины {self.digit_count},\n'
        result += f'составленных из цифр от {self.digit_value_min} до {self.digit_value_max} включительно '
        result += f'согласно установленным условиям.'
        return result

