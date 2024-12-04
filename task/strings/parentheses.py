"""Задания: обработка строк, скобочные последовательности."""

from typing import Tuple
from random import randint, choice

from task import Task

class TaskStringsParenthesesLongestValid(Task):
    """Задание: дана строка с разными видами скобок.
    Определить максимальную длину её подстроки, являющейся правильной скобочной последовательностью
    без учёта прочих символов. Такая подстрока должна начинаться с открывающий скобки и заканчиваться
    соответствующей закрывающей скобкой."""

    string_length_min: int = 900_000
    """Минимальная длина строки."""

    string_length_max: int = 1_000_000
    """Минимальная длина строки."""

    parentheses_pairs: Tuple[str] = ('()', '[]', '{}')
    """Минимальное общее число зависимостей."""

    other_characters: str = '0123456789+'
    """Прочие символы."""

    string: str = ''
    """Строка для определения подстроки по заданию."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__()
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        string_length = randint(self.string_length_min, self.string_length_max)
        character_set = ''.join(self.parentheses_pairs) + self.other_characters
        self.string = ''.join(choice(character_set) for _ in range(string_length))

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        self.__generate_raw()

    def generate(self) -> None:
        """Генерирует параметры условия."""
        self.__generate()

    def solve(self, get_load=False) -> tuple[int, list[int]] | int:
        """Решение задания."""
        substring_length_max = 0
        stack = []
        opening_parentheses = ''.join(pair[0] for pair in self.parentheses_pairs)
        closing_parentheses = ''.join(pair[1] for pair in self.parentheses_pairs)
        for index, character in enumerate(self.string):
            if character in opening_parentheses:
                stack.append((character, index))
            elif character in closing_parentheses and stack:
                previous_parenthesis = stack[-1][0]
                if previous_parenthesis + character in self.parentheses_pairs:
                    substring_length_max = max(substring_length_max, index - stack.pop()[1] + 1)
                else:
                    stack = []
        return substring_length_max

    def __repr__(self) -> str:
        """Представление задания."""
        result = f'Дана строка со скобками {self.parentheses_pairs}\n'
        result += 'Определить макс. длину подстроки - правильной скобочной последовательности.'
        result += 'Подстрока должна быть в общей паре скобок. Нескобочные символы в правильности не учитывать.'
        return result

    def save_to_file(self, file_name: str) -> None:
        """Запись строки в файл."""
        with open(file_name, 'w') as out_file:
            out_file.write(self.string)

    def load_from_file(self, file_name: str) -> None:
        """Чтение строки из файла."""
        with open(file_name) as in_file:
            self.string = in_file.readline().strip()

