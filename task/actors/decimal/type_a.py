"""Задания: десятичные исполнители, тип A."""

from random import randint
from task import Task


class TaskActorsDecimalTypeA(Task):
    """Задание: k-значное число, получаются попарные суммы цифр соседних разрядов,
    отбрасывается наибольшая сумма, остальные записываются по невозрастанию.
    Найти max/min данные под заданный результат."""

    initial_digits: int = 4
    """Количество цифр в искомом числе."""
    solutions_min: int = 2
    """Требуемое минимальное количество решений."""
    solutions_max: int = 20
    """Требуемое максимальное количество решений."""
    final_number: int = 10
    """Число, которое должно получиться в результате работы исполнителя по алгоритму."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__()
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без проверки."""
        test_number = randint(10 ** (self.initial_digits - 1), 10 ** self.initial_digits - 1)
        self.final_number = self.actor_function(test_number)

    def __generate(self) -> None:
        """Генерация задания с проверкой."""
        assert self.solutions_min <= self.solutions_max
        # Критерий проверки: решений не менее указанного количества.
        solutions_count = 0
        while not (self.solutions_min <= solutions_count <= self.solutions_max):
            self.__generate_raw()
            solutions_count = len(self.solve())

    def generate(self) -> None:
        """Генерирует параметры условия."""
        self.__generate()

    def solve(self) -> list[int]:
        """Решает задание."""
        result = []
        for n in range(10**(self.initial_digits - 1), 10 ** self.initial_digits):
            if self.actor_function(n) == self.final_number:
                result.append(n)
        return result

    def __repr__(self) -> str:
        """Представление задания."""
        return f'Задана функция преобразования {self.initial_digits}-значного числа' \
               f'. Определить исходные числа для результата {self.final_number}'

    def actor_function(self, n: int) -> int | None:
        """Функция преобразования исполнителя."""
        s = ''
        while n > 0:
            s = str(n % 10) + s
            n //= 10
        if len(s) != self.initial_digits:
            return
        d = [int(a) + int(b) for a, b in zip(s, s[1:])]
        d = sorted(d, reverse=True)[1:]
        s = "".join([str(x) for x in d])
        return int(s)
