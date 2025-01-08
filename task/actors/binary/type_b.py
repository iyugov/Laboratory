"""Задания: двоичные исполнители, тип B."""

from task import Task


class TaskActorsBinaryTypeB(Task):
    """Задание: определено преобразование натурального числа N в натуральное число R по следующему правилу:
    1) строится двоичная запись числа N;
    2) в этой записи подсчитывается количество единиц (A) и нулей (B);
    3) если число N чётное, то к его двоичной записи справа дописывается двоичная запись числа A, иначе - числа B;
    4) полученная запись является двоичной записью числа R.
    Определить, сколько чисел, принадлежащих отрезку [X; Y], могут быть значением R."""

    initial_number_min: int = 1
    """Минимальное значение исходного числа."""

    initial_number_max: int = 1_000_000
    """Максимальное значение исходного числа."""

    bound_min: int = 10
    """Минимальное значение границы диапазона результата."""

    bound_max: int = 1000
    """Максимальное значение границы диапазона результата."""

    bound_left: int = 0
    """Левая граница диапазона результата."""

    bound_right: int = 0
    """Правая граница диапазона результата."""

    range_length_min: int = 50
    """Минимальное значение количества целых чисел в диапазоне."""

    range_length_max: int = 200
    """Максимальное значение количества целых чисел в диапазоне."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__()
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без проверки."""
        from random import randint
        range_ok = False
        while not range_ok:
            self.bound_left = randint(self.bound_min, self.bound_max)
            self.bound_right = randint(self.bound_min, self.bound_max)
            range_ok = self.range_length_min <= self.bound_right - self.bound_left <= self.range_length_max

    def __generate(self) -> None:
        """Генерация задания с проверкой."""
        self.__generate_raw()

    def generate(self) -> None:
        """Генерирует параметры условия."""
        self.__generate()

    def solve(self) -> int:
        """Решает задание."""
        result = 0
        for n in range(self.initial_number_min, self.initial_number_max + 1):
            function_result = self.actor_function(n)
            if self.bound_left <= function_result <= self.bound_right:
                result += 1
        return result

    def __repr__(self) -> str:
        """Представление задания."""
        result = self.__doc__.replace('X', str(self.bound_left)).replace('Y', str(self.bound_right))
        return result

    @staticmethod
    def actor_function(n: int) -> int:
        """Функция преобразования исполнителя."""
        s = bin(n)[2:]
        a = s.count('1')
        b = s.count('0')
        if n % 2 == 0:
            s += bin(a)[2:]
        else:
            s += bin(b)[2:]
        return int(s, 2)
