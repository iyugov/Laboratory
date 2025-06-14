"""Задания: комбинаторика, лексикографический порядок."""
from typing import Callable, Dict

from task import Task

class TaskCombinatoricsLexOrderFindNumberOfWordByCondition(Task):
    """Задание: все возможные слова, составленные из символов заданного алфавита,
    записаны в лексикографическом порядке (A, AA, ..., B, ...) и пронумерованы, начиная с 1.
    Определить первый номер, последний номер и количество номеров слов по условиям на номер и слово."""

    alphabet: str = 'ТЕОРИЯ'
    """Алфавит для составления слов."""

    word_length: int = 5
    """Длина слова."""

    word_condition: Callable = lambda self, word: word[0] not in 'РТЯ' and word.count('И') >= 2
    """Условие на слово."""

    number_condition: Callable = lambda self, number: number % 2 == 1
    """Условие на номер."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        pass

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        self.__generate_raw()

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> Dict[str, int]:
        """Решение задания."""
        from itertools import product
        words = []
        for number, letters in enumerate(product(sorted(self.alphabet), repeat=self.word_length), 1):
            word = ''.join(letters)
            if self.word_condition(word) and self.number_condition(number):
                words.append((number, word))
        return {'min': min(words), 'max': max(words), 'count': len(words)} if words else {}

    def __repr__(self) -> str:
        """Представление задания."""
        from itertools import product
        result = f'Задание: все {self.word_length}-буквенные слова, составленные из символов алфавита "{self.alphabet}",\n'
        result += f'записаны в лексикографическом порядке и пронумерованы, начиная с 1.\n'
        result += 'Вот начало этого списка:'
        for number, letters in enumerate(product(sorted(self.alphabet), repeat=self.word_length), 1):
            word = ''.join(letters)
            result += f'\n{number}. {word}'
            if number == len(self.alphabet) + 1:
                result += '\n...\n'
                break
        result += f'Определить первый номер, последний номер и количество номеров слов по условиям на номер и слово.'
        return result

class TaskCombinatoricsShortlexOrderFindNumberOfWord(Task):
    """Задание: все возможные слова, составленные из символов заданного алфавита,
    записаны в shortlex-порядке (A, B, ..., Z, AA, BB, ..., ZZ, AAA, ...) и пронумерованы, начиная с 1.
    Определить порядковый номер заданного слова в этом списке."""

    base_alphabet: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    """Базовый алфавит для составления слов."""

    alphabet: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    """Используемый алфавит для составления слов."""

    alphabet_length_min: int = 5
    """Минимальная длина алфавита."""

    alphabet_length_max: int = 26
    """Максимальная длина алфавита."""

    word_length_min: int = 4
    """Минимальная длина слова."""

    word_length_max: int = 6
    """Максимальная длина слова."""

    word: str = ''
    """Заданное слово."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import randint, choice
        self.alphabet = self.base_alphabet[:randint(self.alphabet_length_min, self.alphabet_length_max)]
        self.word = ''.join([choice(self.alphabet) for _ in range(randint(self.word_length_min, self.word_length_max))])

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        self.__generate_raw()

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> None:
        """Решение задания."""
        alphabet = sorted(self.alphabet)
        index = 1
        for length in range(1, len(self.word)):
            index += len(alphabet) ** length
        for pos, char in enumerate(self.word):
            char_index = alphabet.index(char)
            remaining_positions = len(self.word) - pos - 1
            index += char_index * (len(alphabet) ** remaining_positions)
        return index

    def __repr__(self) -> str:
        """Представление задания."""
        result = f'Задание: все возможные слова, составленные из символов алфавита "{self.alphabet}",\n'
        result += f'записаны в shortlex-порядке и пронумерованы, начиная с 1.\n'
        result += f'Определить порядковый номер слова "{self.word}" в этом списке.'
        return result
