"""Задания: символьные последовательности, подпоследовательности."""
from typing import Tuple

from task import Task


class TaskCharSequenceTypeA(Task):
    """Тип A: дана символьная последовательность.
    Определить наибольшую длину её непрерывной подпоследовательности из попарно повторяющихся символов.
    Пример подходящей подпоследовательности: 'AACCBBBBDDAABBAA'.
    """

    alphabet: str = 'ABCD'

    sequence_length_min: int = 900_000
    """Минимальная длина последовательности."""

    sequence_length_max: int = 1_000_000
    """Максимальная длина последовательности."""

    sequence: str = ''
    """Заданная последовательность."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import choice, randint
        sequence_length = randint(self.sequence_length_min, self.sequence_length_max)
        self.sequence = ''.join([choice(self.alphabet) for _ in range(sequence_length)])

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        self.__generate_raw()

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> int:
        """Решение задания."""
        from re import finditer
        regexp = r'(([' + self.alphabet + r'])\2)+'
        max_length_substring = ''
        for match in finditer(regexp, self.sequence):
            max_length_substring = max(max_length_substring, match.group(0), key=lambda x: len(x))
        index = self.sequence.index(max_length_substring)
        # Отрабатываем возможное перекрытие: AABBBCCDD -> 6 (BBCCDD)
        if index < 2:
            return len(max_length_substring)
        if self.sequence[index - 1] == self.sequence[index - 2]:
            return len(max_length_substring) + 2

    def __repr__(self) -> str:
        """Представление задания."""
        return self.__doc__

    def write_to_file(self, file_name: str) -> None:
        """Запись последовательности в файл."""
        with open(file_name, 'w') as file_out:
            file_out.write(f'{self.sequence}')

    def read_from_file(self, file_name: str) -> None:
        """Чтение последовательности из файла."""
        with open(file_name, 'r') as file_in:
            self.sequence = file_in.readline().strip()
        self.alphabet = ''.join(set(self.sequence))


class TaskCharSequenceTypeB(Task):
    """Тип B: дана последовательность из десятичных цифр.
    Определить наибольшую длину её непрерывной подпоследовательности, состоящей сначала из не менее чем одной
    чётной цифры, затем - не менее чем одной нечётной цифры.
    """

    sequence_length_min: int = 900_000
    """Минимальная длина последовательности."""

    sequence_length_max: int = 1_000_000
    """Максимальная длина последовательности."""

    sequence: str = ''
    """Заданная последовательность."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import choice, randint
        sequence_length = randint(self.sequence_length_min, self.sequence_length_max)
        alphabet = ''.join(str(x) for x in range(10))
        self.sequence = ''.join([choice(alphabet) for _ in range(sequence_length)])

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        self.__generate_raw()

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> int:
        """Решение задания."""
        from re import finditer
        regexp = r'[02468]+[13579]+'
        max_length_substring = ''
        for match in finditer(regexp, self.sequence):
            max_length_substring = max(max_length_substring, match.group(0), key=lambda x: len(x))
        return len(max_length_substring)

    def __repr__(self) -> str:
        """Представление задания."""
        return self.__doc__

    def write_to_file(self, file_name: str) -> None:
        """Запись последовательности в файл."""
        with open(file_name, 'w') as file_out:
            file_out.write(f'{self.sequence}')

    def read_from_file(self, file_name: str) -> None:
        """Чтение последовательности из файла."""
        with open(file_name, 'r') as file_in:
            self.sequence = file_in.readline().strip()


class TaskCharSequenceTypeC(Task):
    """Тип C: дана последовательность из цифр и заглавных латинских букв.
    Определить наибольшую длину её непрерывной подпоследовательности, в которой чередуются буквы и цифры.
    """

    alphabet_letters: str = 'ABCDEFGHIJKLMONOQRSTUVWXYZ'
    """Алфавит заглавных латинских букв."""

    alphabet_digits: str = '0123456789'
    """Алфавит цифр."""

    sequence_length_min: int = 900_000
    """Минимальная длина последовательности."""

    sequence_length_max: int = 1_000_000
    """Максимальная длина последовательности."""

    sequence: str = ''
    """Заданная последовательность."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import choice, randint
        sequence_length = randint(self.sequence_length_min, self.sequence_length_max)
        alphabet = self.alphabet_letters + self.alphabet_digits
        self.sequence = ''.join([choice(alphabet) for _ in range(sequence_length)])

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        self.__generate_raw()

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> int:
        """Решение задания."""
        from re import finditer
        regexp = r'[0-9]?([A-Z][0-9])+[A-Z]?'
        max_length_substring = ''
        for match in finditer(regexp, self.sequence):
            max_length_substring = max(max_length_substring, match.group(0), key=lambda x: len(x))
        return len(max_length_substring)

    def __repr__(self) -> str:
        """Представление задания."""
        return self.__doc__

    def write_to_file(self, file_name: str) -> None:
        """Запись последовательности в файл."""
        with open(file_name, 'w') as file_out:
            file_out.write(f'{self.sequence}')

    def read_from_file(self, file_name: str) -> None:
        """Чтение последовательности из файла."""
        with open(file_name, 'r') as file_in:
            self.sequence = file_in.readline().strip()


class TaskCharSequenceTypeD(Task):
    """Тип D: дана строка с разными видами скобок.
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
        from random import randint, choice
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


class TaskCharSequenceTypeE(Task):
    """Тип E: дана символьная последовательность, состоящая из заглавных латинских букв.
    Определить минимальную длину её непрерывной подпоследовательности, в которой разность количества символов A
    и количества символов B максимальна. В качестве ответа дать длину этой подпоследовательности.
    """

    alphabet: str = 'ABCD'
    """Алфавит."""

    sequence_length_min: int = 900_000
    """Минимальная длина последовательности."""

    sequence_length_max: int = 1_000_000
    """Максимальная длина последовательности."""

    sequence: str = ''
    """Заданная последовательность."""

    first_letter: str = 'A'
    """Первая буква (её количество - уменьшаемое)."""

    second_letter: str = 'B'
    """Вторая буква (её количество - вычитаемое)."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import choice, randint
        letters_ok = False
        while not letters_ok:
            self.first_letter = choice(self.alphabet)
            self.second_letter = choice(self.alphabet)
            letters_ok = self.first_letter != self.second_letter
        sequence_length = randint(self.sequence_length_min, self.sequence_length_max)
        sequence_ok = False
        while not sequence_ok:
            self.sequence = ''.join([choice(self.alphabet) for _ in range(sequence_length)])
            sequence_ok = self.sequence.count(self.first_letter) > 0 and self.sequence.count(self.second_letter) > 0

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        self.__generate_raw()

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> int:
        """Решение задания."""
        difference = 0
        max_difference = 0
        length = 0
        min_length = float('inf')
        for letter in self.sequence:
            if letter == self.first_letter:
                difference += 1
            elif letter == self.second_letter:
                difference -= 1
            if difference > 0:
                length += 1
                if difference > max_difference:
                    max_difference = difference
                    min_length = length
                elif difference == max_difference:
                    min_length = min(min_length, length)
            else:
                difference = 0
                length = 0
        return min_length

    def solve_slow(self) -> int:
        """Решение задания (неоптимальное, перебором подстрок)."""
        max_difference = 0
        min_length = float('inf')
        for index_start in range(len(self.sequence)):
            for index_end in range(index_start, len(self.sequence)):
                substring = self.sequence[index_start:index_end + 1]
                count_first_letter = substring.count(self.first_letter)
                count_second_letter = substring.count(self.second_letter)
                if count_first_letter - count_second_letter > max_difference:
                    max_difference = count_first_letter - count_second_letter
                    min_length = len(substring)
                elif count_first_letter - count_second_letter == max_difference and max_difference > 0:
                    min_length = min(min_length, len(substring))
        return min_length

    def __repr__(self) -> str:
        """Представление задания."""
        result = 'Дана символьная последовательность, состоящая из заглавных латинских букв.\n'
        result += ' Определить минимальную длину её непрерывной подпоследовательности,\n'
        a, b =  self.first_letter, self.second_letter
        result += f'в которой разность количества символов {a} и количества символов {b} максимальна.\n'
        result += 'В качестве ответа дать длину этой подпоследовательности.'
        return result

    def write_to_file(self, file_name: str) -> None:
        """Запись последовательности в файл."""
        with open(file_name, 'w') as file_out:
            file_out.write(f'{self.sequence}')

    def read_from_file(self, file_name: str) -> None:
        """Чтение последовательности из файла."""
        with open(file_name, 'r') as file_in:
            self.sequence = file_in.readline().strip()
        self.alphabet = ''.join(set(self.sequence))


class TaskCharSequenceTypeF(Task):
    """Тип F: дана символьная последовательность, состоящая из заглавных латинских букв.
    Определить максимальную длину её непрерывной подпоследовательности, состоящей из строк нескольких видов.
    Строки могут перекрываться.
    """

    chunks: Tuple[str] = ('ABA', 'BAB')
    """Элементы строки."""

    sequence_length_min: int = 900_000
    """Минимальная длина последовательности."""

    sequence_length_max: int = 1_000_000
    """Максимальная длина последовательности."""

    sequence: str = ''
    """Заданная последовательность."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import choice, randint
        alphabet = tuple(set(''.join(self.chunks)))
        sequence_length = randint(self.sequence_length_min, self.sequence_length_max)
        self.sequence = ''.join([choice(alphabet) for _ in range(sequence_length)])

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        self.__generate_raw()

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> int:
        """Решение задания."""
        def check(substring: str) -> None:
            """Проверка подстроки с рекурсивным расширением и обновление ."""
            nonlocal max_substring
            if substring in self.sequence:
                if len(substring) > len(max_substring):
                    max_substring = substring
                for chunk in self.chunks:
                    check(substring + chunk)
        max_substring = ''
        check('')
        return len(max_substring)

    def __repr__(self) -> str:
        """Представление задания."""
        result = 'Дана символьная последовательность, состоящая из заглавных латинских букв.\n'
        result += f'Определить максимальную длину её непрерывной подпоследовательности, состоящей из элементов {self.chunks}.'
        return result

    def write_to_file(self, file_name: str) -> None:
        """Запись последовательности в файл."""
        with open(file_name, 'w') as file_out:
            file_out.write(f'{self.sequence}')

    def read_from_file(self, file_name: str) -> None:
        """Чтение последовательности из файла."""
        with open(file_name, 'r') as file_in:
            self.sequence = file_in.readline().strip()