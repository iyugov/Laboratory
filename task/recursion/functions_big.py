"""Рекурсия и рекуррентные соотношения: функции с очень большими результатами."""
from markdown.test_tools import recursionlimit

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

    def solve(self) -> int:
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

class TaskRecursionFunctionsBigTypeB(Task):
    """Задана функция от натурального N:
    F(N) = 1, если N = 1;
    F(N) = N + F(N - 1), если N > 1.
    Определить значение выражения F(A) - F(B)."""

    argument_min: int = 1000
    """Минимальное значение аргумента функции."""

    argument_max: int = 10000
    """Максимальное значение аргумента функции."""

    argument1: int = 1000
    """Значение первого аргумента функции."""

    argument2: int = 2000
    """Значение первого аргумента функции."""

    argument_difference_min: int = 1000
    """Минимальная разность аргументов функции."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import randint
        arguments_ok = False
        while not arguments_ok:
            self.argument1 = randint(self.argument_min, self.argument_max)
            self.argument2 = randint(self.argument_min, self.argument_max)
            arguments_ok = self.argument1 - self.argument2 >= self.argument_difference_min


    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        self.__generate_raw()

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> int:
        """Решение задания."""
        a, b = self.argument1, self.argument2
        return (a - b) * (a + b + 1) // 2
        # возможно также: sum(x for x in range(self.argument2 + 1, self.argument1 + 1))

    def __repr__(self) -> str:
        """Представление задания."""
        result = 'Функция F(N) задана соотношениями:\n'
        result += '  F(N) = 1, если N = 1;\n'
        result += '  F(N) = N + F(N - 1), если N > 1.\n'
        result += f'Определить значение выражения F({self.argument1})-F({self.argument2}).'
        return result


class TaskRecursionFunctionsBigTypeC(Task):
    """Задана функция от натурального N:
    F(N) = 1, если N >= T;
    F(N) = F(n + A) + F(n + B), если N < T.
    Определить количество различных натуральных чисел в области значений функции."""

    recursion_limit_min: int = 1000
    """Минимальное значение предела рекурсии."""

    recursion_limit_max: int = 10000
    """Максимальное значение предела рекурсии."""

    recursion_limit: int = 1000
    """Предел рекурсии."""

    term_min: int = 2
    """Минимальное значение слагаемого."""

    term_max: int = 100
    """Максимальное значение слагаемого."""

    term1: int = 2
    """Значение первого слагаемого."""

    term2: int = 3
    """Значение второго слагаемого."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import randint
        from math import gcd
        self.recursion_limit = randint(self.recursion_limit_min, self.recursion_limit_max)
        self.term1 = self.term2 = 1
        while gcd(self.term1, self.term2) == 1:
            self.term1 = randint(self.term_min, self.term_max)
            self.term2 = randint(self.term_min, self.term_max)

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        self.__generate_raw()

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> int:
        """Решение задания."""
        from functools import cache
        unique_results = set()
        limit = self.recursion_limit + max(self.term1, self.term2)
        f = [None] * (limit + 1)
        for n in range(limit, 0, -1):
            if n >= self.recursion_limit:
                f[n] = 1
            else:
                f[n] = f[n + self.term1] + f[n + self.term2]
            unique_results.add(f[n])
        return len(unique_results)

    def __repr__(self) -> str:
        """Представление задания."""
        result = 'Функция F(N) от натурального N задана соотношениями:\n'
        result += f'  F(N) = 1, если N >= {self.recursion_limit};\n'
        result += f'  F(N) = F(N + {self.term1}) + F(N + {self.term2}) в остальных случаях.\n'
        result += 'Определить количество различных натуральных чисел в области значений функции.'
        return result
