"""Задания: двоичные исполнители, тип E."""

from task import Task


class TaskActorsBinaryTypeE(Task):
    """Задание: определено преобразование натурального числа N в натуральное число R по следующему правилу:
    1) строится двоичная запись числа N;
    2) если число N делится на 3, то к этой записи дописываются его три двоичные цифры;
    3) если число N не делится на 3, то остаток от деления умножается на 3, переводится в двоичную запись
    и дописывается в конец числа.
    Определить максимально возможное число N, для которого результат меньше заданного ограничения."""

    initial_number_min: int = 4
    """Минимальное значение исходного числа."""

    initial_number_max: int = 20_000
    """Максимальное значение исходного числа."""

    target_min: int = 80
    """Минимальное значение ориентира результата."""

    target_max: int = 200
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
            solution_ok = 0 < solution < self.target_max

    def generate(self) -> None:
        """Генерирует параметры условия."""
        self.__generate()

    def solve(self) -> int:
        """Решает задание."""
        m = 0
        for n in range(self.initial_number_min, self.initial_number_max + 1):
            r = self.actor_function(n)
            if r < self.target:
                m = n
        return m

    def __repr__(self) -> str:
        """Представление задания."""
        result = f'{self.__doc__}\n'
        result += f'Ограничение - {self.target}.'
        return result

    @staticmethod
    def actor_function(n: int) -> int:
        """Функция преобразования исполнителя."""
        s = bin(n)[2:]
        if n % 3 == 0:
            s += s[-3:]
        else:
            s += bin(n % 3 * 3)[2:]
        return int(s, 2)