"""Задания: исполнитель Редактор, тип A."""

from task import Task


class TaskActorsEditorTypeA(Task):
    """Задание: Редактор получает произвольную строку из символов двух видов - A и B, и изменяет её так,
    чтобы она не содержала ни K подряд идущих символов A, ни даже двух подряд идущих символов B.
    Определить число результирующих строк, содержащих ровно N символов B."""

    alphabet: str = '0123456789'
    """Алфавит."""

    character_a: str = '0'
    """Символ A."""

    character_b: str = '1'
    """Символ B."""

    count_a_adjacent_min: int = 2
    """Минимальное недопустимое количество символов A подряд."""

    count_a_adjacent_max: int = 6
    """Максимальное недопустимое количество символов A подряд."""

    count_a_adjacent: int = 3
    """Недопустимое символов A подряд."""

    count_b_required_min: int = 1
    """Минимальное требуемое количество символов."""

    count_b_required_max: int = 10
    """Максимальное требуемое количество символов."""

    count_b_required: int = 2
    """Требуемое количество символов A."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__()
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без проверки."""
        from random import choice, randint
        self.character_a, self.character_b = choice(self.alphabet), choice(self.alphabet)
        while self.character_a == self.character_b:
            self.character_b = choice(self.alphabet)
        self.count_a_adjacent = randint(self.count_a_adjacent_min, self.count_a_adjacent_max)
        self.count_b_required = randint(self.count_b_required_min, self.count_b_required_max)


    def __generate(self) -> None:
        """Генерация задания с проверкой."""
        self.__generate_raw()

    def generate(self) -> None:
        """Генерирует параметры условия."""
        self.__generate()

    def solve(self) -> int:
        """Решает задание."""
        n, k = self.count_a_adjacent, self.count_b_required
        return n**2 * (n - 1) ** (k - 1)

    def __repr__(self) -> str:
        """Представление задания."""
        a, b = self.character_a, self.character_b
        result = 'Программа:\n'
        result += '---\n'
        result += f'ПОКА нашлось ({a * self.count_a_adjacent}) или нашлось ({b * 2})\n'
        result += f'  заменить ({a * self.count_a_adjacent}, {b})\n'
        result += f'  заменить ({b * 2}, {a})\n'
        result += 'КОНЕЦ ПОКА\n'
        result += '---\n'
        result += f'Определить, сколько различных строк, содержащих ровно {self.count_b_required} символов "{b}",\n'
        result += f'может получить Редактор из строк, содержащих только символы "{a}" и "{b}".'
        return result

