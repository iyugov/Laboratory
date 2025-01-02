"""Задания: комбинаторика, лексикографический порядок."""

from task import Task

class TaskCombinatoricsShortlexOrderFindNumberOfWord(Task):
    """Задание: все возможные слова, составленные из символов заданного алфавита,
    записаны в shortlex-порядке (A, B, ..., Z, AA, BB, ..., ZZ, AAA, ...) и пронумерованы, начиная с 1.
    Определить порядковый номер заданного слова в этом списке."""

    base_alphabet: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    """Базовый для составления слов."""

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
