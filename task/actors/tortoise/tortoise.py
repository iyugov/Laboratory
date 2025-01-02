"""Задания: исполнитель Черепаха."""
from typing import Dict

from networkx.algorithms.operators.binary import symmetric_difference

from task import Task


class TaskActorsTortoiseTwoActorsTypeA(Task):
    """Задание: одна Черепаха в начале координат и направлена вверх, вторая - неизвестно где, направлена вправо.
    Обе исполняют одну и ту же программу по рисованию прямоугольника.
    Определить предельные значения для описанных ими областей."""

    rectangle_size_min: int = 5
    """Минимальный размер прямоугольника."""

    rectangle_size_max: int = 40
    """Максимальный размер прямоугольника."""

    rectangle_width: int = 0
    """Ширина прямоугольника."""

    rectangle_height: int = 0
    """Высота прямоугольника."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__()
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без проверки."""
        from random import randint
        self.rectangle_width = randint(self.rectangle_size_min, self.rectangle_size_max)
        self.rectangle_height = randint(self.rectangle_size_min, self.rectangle_size_max)

    def __generate(self) -> None:
        """Генерация задания с проверкой."""
        self.__generate_raw()

    def generate(self) -> None:
        """Генерирует параметры условия."""
        self.__generate()

    def solve(self) -> Dict[str, Dict[str, int]]:
        """Решает задание."""
        def get_values(width: int, height: int, perimeter_only=False, real_coordinates=False) -> Dict[str, int]:
            """Вычисление значений для пересекающихся прямоугольников."""
            result = {}
            if perimeter_only:
                single_set = 2 * (width + height)
                intersection = 4 * min(width, height)
            else:
                single_set = width * height
                intersection = min(width, height) ** 2
            union = 2 * single_set - intersection
            difference = single_set - intersection
            difference_symmetric = 2 * single_set - 2 * intersection
            if real_coordinates:
                result['Пересечение макс., если одно с вещ. коорд.'] = min(width, height) * (min(width, height) + 1)
                result['Пересечение макс., если оба с вещ. коорд.'] = (min(width, height) + 1) ** 2
            result['Пересечение макс.'] = intersection
            result['Объединение мин.'] = union
            if not perimeter_only:
                result['Разность мин.'] = difference
                result['Симм. разность мин.'] = difference_symmetric
            return result
        solution = {
            'Площадь': get_values(self.rectangle_width, self.rectangle_height),
            'Точки принадлежащие': get_values(self.rectangle_width + 1, self.rectangle_height + 1),
            'Точки внутри': get_values(self.rectangle_width - 1, self.rectangle_height - 1, real_coordinates=True),
            'Периметр': get_values(self.rectangle_width, self.rectangle_height, perimeter_only=True)
        }
        return solution

    def __repr__(self) -> str:
        """Представление задания."""
        program = f'Повтори 2 [Вперёд {self.rectangle_height} Направо 90 Вперёд {self.rectangle_width} Направо 90]\n'
        result = f'{self.__doc__}\n'
        result += 'Программа:\n'
        result += program
        return result

