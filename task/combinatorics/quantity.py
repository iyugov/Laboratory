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

class TaskCombinatoricsQuantityTypeB(Task):
    """Задание: определить количество чисел, имеющих в системе счисления с основанием N ровно K цифр,
    при этом четные или нечётные цифры не должны повторяться."""

    BASE_MIN: int = 2
    """Минимальное основание системы счисления."""

    BASE_MAX: int = 10
    """Максимальное основание системы счисления."""

    base: int = 10
    """Основание системы счисления."""

    LENGTH_MIN: int = 2
    """Минимальная длина числа."""

    LENGTH_MAX: int = 6
    """Максимальная длина числа."""

    length: int = 4
    """Длина числа."""

    parity_for_unique: int = 1
    """Чётность для уникальности цифр (0 - чётные, 1 - нечётные)."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import randint
        self.base = randint(self.BASE_MIN, self.BASE_MAX)
        self.length = randint(self.LENGTH_MIN, self.LENGTH_MAX)
        self.parity_for_unique = randint(0, 1)

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        self.__generate_raw()
        solution_ok = False
        while not solution_ok:
            solution = self.solve()
            solution_ok = solution > 0

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> int:
        """Решение задания."""
        from itertools import product
        count = 0
        for digits in product(range(self.base), repeat=self.length):
            if digits[0] == 0:
                continue
            parity_digits = [d for d in digits if d % 2 == self.parity_for_unique]
            if len(parity_digits) != len(set(parity_digits)):
                continue
            count += 1
        return count

    def __repr__(self) -> str:
        """Представление задания."""
        parity = 'чётные' if self.parity_for_unique == 0 else 'нечётные'
        result = f'Задание: определить количество чисел в системе счисления с основанием {self.base},\n'
        result += f'состоящих из {self.length} цифр, при этом {parity} цифры не должны повторяться.'
        return result