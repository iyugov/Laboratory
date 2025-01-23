"""Задания: двоичные исполнители, тип D."""

from task import Task


class TaskActorsBinaryTypeD(Task):
    """Задание: определено преобразование натурального числа N в натуральное число R по следующему правилу:
    1) строится двоичная запись числа N;
    2) если число N чётное, то все имеющиеся в его двоичной записи нули дублируются справа;
    3) если число N нечётное, то все имеющиеся в его двоичной записи единицы дублируются слева.
    Определить минимально возможное число N, для которого результат превышает заданное ограничение."""

    initial_number_min: int = 1
    """Минимальное значение исходного числа."""

    initial_number_max: int = 11_000
    """Максимальное значение исходного числа."""

    target_min: int = 10
    """Минимальное значение ориентира результата."""

    target_max: int = 10_000
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
            solution_ok = 0 < solution

    def generate(self) -> None:
        """Генерирует параметры условия."""
        self.__generate()

    def solve(self) -> int:
        """Решает задание."""
        for n in range(self.initial_number_min, self.initial_number_max + 1):
            r = self.actor_function(n)
            if r > self.target:
                return n
        return 0

    def __repr__(self) -> str:
        """Представление задания."""
        result = f'{self.__doc__}\n'
        result += f'Ограничение - {self.target}.'
        return result

    @staticmethod
    def actor_function(n: int) -> int:
        """Функция преобразования исполнителя."""
        s = bin(n)[2:]
        if n % 2 == 0:
            s += '0' * s.count('0')
        else:
            s = '1' * s.count('1') + s
        return int(s, 2)