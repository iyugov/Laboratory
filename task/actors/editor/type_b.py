"""Задания: исполнитель Редактор, тип A."""
from typing import Tuple, List, Dict

from task import Task


class TaskActorsEditorTypeB(Task):
    """Задание: Редактор получает произвольную строку из цифр нескольких видов, среди которых есть два специальных
    символа - одна в начале и одна в конце. Спецсимвол из начала при исполнении алгоритма как бы проходит сквозь строку
    и заменяет одни группы цифр другими (с возможным ходом назад) пока не встретит другой спецсимвол в конце строки.
    Известно количество цифр каждого вида в результирующей строке.
    Определить количество символов каждого вида в исходной строке."""

    base_digits: str = '123'
    """Набор основных цифр."""

    special_character: str = '0'
    """Специальный символ, который проходит сквозь строку."""

    replacement_length_min: int = 2
    """Минимальная длина замены."""

    replacement_length_max: int = 4
    """Максимальная длина замены."""

    replacements: Tuple[Tuple[str, str], ...] = tuple()
    """Замены, которые будут выполнены."""

    digit_count_min: int = 10
    """Минимальное количество цифр в результирующей строке."""

    digit_count_max: int = 100
    """Максимальное количество цифр в результирующей строке."""

    final_counts: Dict[str, int] = dict()
    """Итоговые количества цифр в результирующей строке."""

    replacements_limit: int = 20
    """Максимальное количество замен, которое может быть выполнено, для определения циклов."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__()
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без проверки."""
        from random import randint, choice
        def has_cycle(replacements):
            """Определение цикла в графе замен."""
            test_string = self.special_character + self.base_digits + self.special_character
            replacements_limit = self.replacements_limit
            while (self.special_character * 2) not in test_string:
                for _old, _new in replacements:
                    test_string = test_string.replace(_old, _new, 1)
                replacements_limit -= 1
                if replacements_limit == 0:
                    return True
            return False

        old: List[str] = [self.special_character + digit for digit in self.base_digits]
        new: List[str] = []
        all_ok = False
        while not all_ok:
            ok = True
            new = []
            for _ in self.base_digits:
                s = ''.join(choice(self.special_character + self.base_digits) for _ in range(randint(2, 4)))
                if s.count(self.special_character) != 1 or s[0] == self.special_character:
                    ok = False
                    break
                new.append(s)
            if not (ok and len(set(new)) == 3):
                continue
            final_set = set(''.join(item for item in new))
            if len(final_set) < len(self.base_digits) + 1:
                continue
            if not any(x[-1] != self.special_character for x in new):
                continue
            if has_cycle(tuple(zip(old, new))):
                continue
            all_ok = ok
        self.replacements = tuple(zip(old, new))
        initial_counts = {digit: randint(self.digit_count_min, self.digit_count_max) for digit in self.base_digits}
        s = ''.join(digit * initial_counts[digit] for digit in self.base_digits)
        s = self.special_character + s + self.special_character
        while (self.special_character * 2) not in s:
            for old_item, new_item in self.replacements:
                s = s.replace(old_item, new_item, 1)
        self.final_counts = {digit: s.count(digit) for digit in self.base_digits}

    def __generate(self) -> None:
        """Генерация задания с проверкой."""
        solution_ok = False
        while not solution_ok:
            self.__generate_raw()
            solution_ok = self.solve() is not None

    def generate(self) -> None:
        """Генерирует параметры условия."""
        self.__generate()

    def solve(self) -> List[int] | None:
        """Решает задание."""
        def solve_kramer(_matrix, b):
            """Решение системы линейных уравнений методом Крамера."""
            def determinant(_matrix):
                """Вычисление определителя матрицы."""
                if len(_matrix) == 1:
                    return _matrix[0][0]
                _det = 0
                for c in range(len(_matrix)):
                    _det += ((-1) ** c) * _matrix[0][c] * determinant([row[:c] + row[c + 1:] for row in _matrix[1:]])
                return _det
            def replace_column(_matrix, column, new_column):
                """Замена столбца в матрице."""
                return [row[:column] + [new_column[col]] + row[column + 1:] for col, row in enumerate(_matrix)]
            det = determinant(_matrix)
            if det == 0:
                return None
            result = []
            for i in range(len(_matrix)):
                new_matrix = replace_column(_matrix, i, b)
                result.append(determinant(new_matrix) // det)
            return result
        replacements = dict()
        for digit in self.base_digits:
            s = self.special_character + digit + self.special_character
            while (self.special_character * 2) not in s:
                for old, new in self.replacements:
                    s = s.replace(old, new, 1)
            replacements[digit] = ''.join([item for item in s if item != self.special_character])
        matrix = [[None] * len(self.base_digits) for _ in range(len(self.base_digits))]
        for digit in self.base_digits:
            for digit2 in self.base_digits:
                matrix[self.base_digits.index(digit2)][self.base_digits.index(digit)] = replacements[digit].count(digit2)
        return solve_kramer(matrix, list(self.final_counts.values()))

    def __repr__(self) -> str:
        """Представление задания."""
        result = f'Редактор получает строку, состоящую из цифр {tuple(self.base_digits)}\n'
        result += f'и содержащую по одному символу {self.special_character} в начале и в конце.\n'
        result += 'Редактор выполнил программу:\n'
        result += '---\n'
        result += f'ПОКА НЕ нашлось ({self.special_character * 2})\n'
        for old, new in self.replacements:
            result += f'  заменить ({old}, {new})\n'
        result += 'КОНЕЦ ПОКА\n'
        result += '---\n'
        result += 'Конечная строка содержит:\n'
        for digit, count in self.final_counts.items():
            result += f'  цифр {digit}: {count}\n'
        result += 'Определить исходное количество всех цифр в строке.\n'

        return result

