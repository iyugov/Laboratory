"""Задания: двоичные исполнители, тип B."""

from task import Task


class TaskActorsBinaryTypeC(Task):
    """Задание: определено преобразование натурального числа N в натуральное число R по следующему правилу:
    1) строится двоичная запись числа N;
    2) если число N чётное, то в полученной записи удваивается каждая единица, иначе - каждый нуль;
    3) полученная запись является двоичной записью числа R.
    Определить максимально возможное число R, не превышающее некоторого ограничения и не равное N."""

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
            solution_wrong = self.solve_wrong()
            solution_ok = 0 < solution < solution_wrong

    def generate(self) -> None:
        """Генерирует параметры условия."""
        self.__generate()

    def solve(self) -> int:
        """Решает задание."""
        result = 0
        for n in range(self.initial_number_min, self.initial_number_max + 1):
            r = self.actor_function(n)
            if r <= self.target and r != n:
                result = max(result, r)
        return result

    def solve_wrong(self) -> int:
        """Решает задание неверно - без проверки на неравенство R и N."""
        result = 0
        result = 0
        for n in range(self.initial_number_min, self.initial_number_max + 1):
            r = self.actor_function(n)
            if r <= self.target:
                result = max(result, r)
        return result

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
            s = s.replace('1', '11')
        else:
            s = s.replace('0', '00')
        return int(s, 2)