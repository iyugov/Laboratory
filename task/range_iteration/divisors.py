"""Задания: перебор чисел, делители."""
from typing import Callable, Dict, List
from task import Task


class TaskRangeIterationTypeA(Task):
    """Задание: найти первые K натуральных чисел, превышающих N, у которых есть хотя бы один делитель,
    заканчивающийся в десятичной записи на X, но при этом не равный ни X, не самому числу.
    Вывести сами эти числа, а также их наибольший из таких делителей, в порядке возрастания чисел."""

    numbers_count: int = 5
    """Количество чисел, которые нужно найти."""

    start_number_min: int = 30_000_000
    """Минимальное значение начального числа."""

    start_number_max: int = 100_000_000
    """Максимальное значение начального числа."""

    start_number: int = 50_000_000
    """Начальное число."""

    start_number_multiplier: int = 10_000
    """Множитель начального числа."""

    divisor_ending: int = 100
    """Значение делителя."""

    ending_digits: int = 3
    """Количество последних цифр в делителе, на которые накладывается условие."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__()
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без проверки."""
        from random import randint

        start_number_min = self.start_number_min // self.start_number_multiplier
        start_number_max = self.start_number_max // self.start_number_multiplier
        self.start_number = randint(start_number_min, start_number_max) * self.start_number_multiplier
        self.divisor_ending = randint(10 ** (self.ending_digits - 1), 10 ** self.ending_digits - 1)

    def __generate(self) -> None:
        """Генерация задания с проверкой."""
        self.__generate_raw()

    def generate(self) -> None:
        """Генерирует параметры условия."""
        self.__generate()

    def solve(self) -> List[str]:
        """Решает задание."""
        result = []
        n = self.start_number
        step = 10 ** self.ending_digits
        while len(result) < self.numbers_count:
            n += 1
            ending_divisors = [d for d in range(self.divisor_ending + step, n, step) if n % d == 0]
            if ending_divisors:
                result.append((n, ending_divisors[-1]))
        return result

    def __repr__(self) -> str:
        """Представление задания."""
        result = f'Найти первые {self.numbers_count} натуральных чисел, превышающих {self.start_number},\n' \
                 f'у которых есть хотя бы один делитель, заканчивающийся на {self.divisor_ending},\n' \
                 f'но не равный ни {self.divisor_ending}, не самому числу.'
        return result

