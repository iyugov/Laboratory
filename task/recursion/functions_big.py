"""Рекурсия и рекуррентные соотношения: функции с очень большими результатами."""

from task import Task

class TaskRecursionFunctionsBigTypeA(Task):
    """Задана функция от натурального N:
    F(N) = 1, если N = 1;
    F(N) = N * F(N - 1), если N > 1.
    Определить значение выражения (F(N) / p + F(N - 1)) / F(N - 2). Гарантируется делимость нацело."""

    base_argument_min: int = 1000
    """Минимальное значение основного аргумента функции."""

    base_argument_max: int = 3000
    """Максимальное значение основного аргумента функции."""

    base_argument: int = 1000
    """Значение основного аргумента функции."""

    divisor_min: int = 10
    """Минимальное значение делителя."""

    divisor_max: int = 100
    """Максимальное значение делителя."""

    divisor: int = 1
    """Значение делителя."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import randint
        division_ok = False
        while not division_ok:
            self.base_argument = randint(self.base_argument_min, self.base_argument_max)
            self.divisor = randint(self.divisor_min, self.divisor_max)
            f = [0] * (self.base_argument + 1)
            f[1] = 1
            for n in range(2, self.base_argument + 1):
                f[n] = n * f[n - 1]
            division_ok = self.base_argument % self.divisor == 0
            numerator = f[self.base_argument] // self.divisor + f[self.base_argument - 1]
            division_ok = division_ok and numerator % f[self.base_argument - 2] == 0


    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        self.__generate_raw()

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> None:
        """Решение задания."""
        f = [0] * (self.base_argument + 1)
        f[1] = 1
        for n in range(2, self.base_argument + 1):
            f[n] = n * f[n - 1]
        numerator = f[self.base_argument] // self.divisor + f[self.base_argument - 1]
        return numerator // f[self.base_argument - 2]

    def __repr__(self) -> str:
        """Представление задания."""
        result = 'Функция F(N) задана соотношениями:\n'
        result += '  F(N) = 1, если N = 1;\n'
        result += '  F(N) = N * F(N - 1), если N > 1.\n'
        n, p = self.base_argument, self.divisor
        result += f'Определить значение выражения (F({n}) / {p} + F({n - 1})) / F({n - 2})'
        return result