"""Задания: двоичные исполнители, тип A."""
from typing import Tuple

from task import Task


class TaskActorsBinaryTypeA(Task):
    """Задание: определено преобразование натурального числа N в натуральное число R по следующему правилу:
    1) строится двоичная запись числа N;
    2) в этой записи подсчитывается количество единиц (A) и нулей (B);
    3) значения A и B записываются в двоичной системе счисления - сначала запись числа A, потом запись числа B;
    4) полученная запись является двоичной записью числа R.
    Определить предельное значение исходного числа N для ориентира на результирующее число R."""

    initial_number_min: int = 1
    """Минимальное значение исходного числа."""

    initial_number_max: int = 1_000_000
    """Максимальное значение исходного числа."""

    target_min: int = 10
    """Минимальное значение ориентира результата."""

    target_max: int = 1000
    """Максимальное значение ориентира результата."""

    target: int = 0
    """Ориентир результата."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__()
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без проверки."""
        from random import randint
        self.target = randint(self.target_min, self.target_max)

    def __generate(self) -> None:
        """Генерация задания с проверкой."""
        solution_ok = False
        while not solution_ok:
            self.__generate_raw()
            solution = self.solve()
            solution_ok = solution.count(float('-inf')) == 0 and solution.count(float('inf')) == 0

    def generate(self) -> None:
        """Генерирует параметры условия."""
        self.__generate()

    def solve(self) -> Tuple[int]:
        """Решает задание."""
        result = [float('-inf'), float('-inf'), float('-inf'), float('inf'), float('inf'), float('inf')]
        for n in range(self.initial_number_min, self.initial_number_max + 1):
            function_result = self.actor_function(n)
            if function_result < self.target:
                result[0] = max(result[0], n)
            if function_result <= self.target:
                result[1] = max(result[1], n)
            if function_result == self.target:
                result[2] = max(result[2], n)
            if function_result == self.target:
                result[3] = min(result[3], n)
            if function_result >= self.target:
                result[4] = min(result[4], n)
            if function_result > self.target:
                result[5] = min(result[5], n)
        return tuple(result)

    def __repr__(self) -> str:
        """Представление задания."""
        result = f'{self.__doc__}\n'
        result += f'Определить максимальное значение N, для которого результат меньше {self.target}.\n'
        result += f'Определить максимальное значение N, для которого результат не больше {self.target}.\n'
        result += f'Определить максимальное значение N, для которого результат равен {self.target}.\n'
        result += f'Определить минимальное значение N, для которого результат равен {self.target}.\n'
        result += f'Определить минимальное значение N, для которого результат не меньше {self.target}.\n'
        result += f'Определить минимальное значение N, для которого результат больше {self.target}.\n'
        return result

    @staticmethod
    def actor_function(n: int) -> int:
        """Функция преобразования исполнителя."""
        s = bin(n)[2:]
        a = s.count('1')
        b = s.count('0')
        s = bin(a)[2:] + bin(b)[2:]
        return int(s, 2)
