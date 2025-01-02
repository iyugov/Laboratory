"""Задания: кодирование графической информации."""
from typing import Tuple, List

from oslo_config.cfg import ListOpt

from task import Task

class TaskImagesConversionAndCompressionFindCompressionPercentage(Task):
    """Задание: даны параметры изображения (разрешение, информационный объём, процент сжатия) в двух вариантах.
    Цветовая глубина и геометрические размеры изображений одинаков. Один процент сжатия неизвестен. Найти его."""

    dpi_values: Tuple[int] = (72, 96, 150, 300, 600, 1200, 2400, 4800)
    """Доступные значения разрешения изображения (dpi)."""

    compression_rate_min: int = 5
    """Минимальный коэффициент сжатия изображения в процентах."""

    compression_rate_max: int = 95
    """Максимальный коэффициент сжатия изображения в процентах."""

    amount_mb_min: int = 1
    """Минимальный информационный объём изображения в Мб."""

    amount_mb_max: int = 200
    """Максимальный информационный объём изображения в Мб."""

    dpi: List[int] = []
    """Разрешение изображений."""

    compression_rate: int = 0
    """Процент сжатия первого изображения."""

    amount_of_information_mb: List[int] = []
    """Информационный объём изображений."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import randint, choice
        dpi1, dpi2 = 0, 0
        while dpi1 == dpi2:
            dpi1 = choice(self.dpi_values)
            dpi2 = choice(self.dpi_values)
        self.dpi = [dpi1, dpi2]
        amount_mb1, amount_mb2 = 0, 0
        while amount_mb1 == amount_mb2:
            amount_mb1 = randint(self.amount_mb_min, self.amount_mb_max)
            amount_mb2 = randint(self.amount_mb_min, self.amount_mb_max)
        self.amount_mb = [amount_mb1, amount_mb2]
        self.compression_rate = randint(self.compression_rate_min, self.compression_rate_max)

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        solution_ok = False
        while not solution_ok:
            self.__generate_raw()
            solution = self.solve()
            solution_ok = self.compression_rate_min <= solution <= self.compression_rate_max

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> float:
        """Решение задания."""
        mb1, mb2 = self.amount_mb
        dpi1, dpi2 = self.dpi
        rate = self.compression_rate
        return round(100 * (1 - mb2 * dpi1**2 * (1 - rate / 100) / mb1 / dpi2**2))

    def __repr__(self) -> str:
        """Представление задания."""
        result = f'Изображение №1: {self.dpi[0]} dpi, сжато на {self.compression_rate}%, {self.amount_mb[0]} Мб.\n'
        result += f'Изображение №2: {self.dpi[1]} dpi, сжато на X%, {self.amount_mb[1]} Мб.\n'
        result += 'Найти X. Результат округлять до ближайшего целого.'
        return result