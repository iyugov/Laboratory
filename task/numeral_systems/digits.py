"""Задания: системы счисления, цифры"""
from typing import List, Tuple

from task import Task

class TaskNumeralSystemsFindDigitsInSum(Task):
    """Задание: дана сумма чисел в некоторой позиционной системе счисления. Некоторые цифры неизвестны.
    Определить возможные значения суммы, делящиеся на заданное число.
    Ответ - частные от деления этих сумм на это число."""

    regular_digits: str = '123456789'
    """Возможные значения известных цифр"""

    terms_count: int = 3
    """Количество слагаемых."""

    base_min: int = 17
    """Минимальное основание системы счисления."""

    base_max: int =36
    """Максимальное основание системы счисления."""

    base: int = 36
    """Основание системы счисления."""

    digits_in_term_min: int = 4
    """Минимальное количество цифр в числе."""

    digits_in_term_max: int = 5
    """Максимальное количество цифр в числе."""

    unknown_digits: str = 'xy'
    """Неизвестные цифры (независимые)."""

    hidden_digits_count_max: int = 4
    """Максимальное количество скрытых цифр."""

    divisor_min: int = 10
    """Минимальное значение делителя суммы."""

    divisor_max: int = 100
    """Максимальное значение делителя суммы."""

    divisor: int = 100
    """Значение делителя суммы."""

    terms: List[str] = []
    """Слагаемые (строковое представление)."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import randint, choice
        self.base = randint(self.base_min, self.base_max)
        self.divisor = randint(self.divisor_min, self.divisor_max)
        # Генерация слагаемых без неизвестных цифр
        self.terms = []
        for _ in range(self.terms_count):
            new_term_length = randint(self.digits_in_term_min, self.digits_in_term_max)
            new_term = ''.join(choice(self.regular_digits) for _ in range(new_term_length))
            self.terms.append(new_term)
        # Замена цифр
        hiding_ok = False
        terms = []
        while not hiding_ok:
            terms = self.terms.copy()
            processed_term_indices = set()
            processed_unknown_digits = set()
            hidden_digits_count = randint(len(self.unknown_digits), self.hidden_digits_count_max)
            for _ in range(hidden_digits_count):
                hiding_try_ok = False
                while not hiding_try_ok:
                    term_index = randint(0, self.terms_count - 1)
                    digit_index = randint(1, len(terms[term_index]) - 1)
                    if terms[term_index][digit_index] in self.unknown_digits:
                        continue
                    term = terms[term_index]
                    unknown_digit = choice(self.unknown_digits)
                    term = term[:digit_index] + unknown_digit + term[digit_index + 1:]
                    terms[term_index] = term
                    processed_term_indices.add(term_index)
                    processed_unknown_digits.add(unknown_digit)
                    hiding_try_ok = True
            hiding_ok = len(processed_term_indices) == self.terms_count
            hiding_ok = hiding_ok and len(processed_unknown_digits) == len(self.unknown_digits)
        self.terms = terms

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        solution_ok = False
        while not solution_ok:
            self.__generate_raw()
            solution = self.solve()
            solution_ok = len(solution) > 1

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> List[int]:
        """Решение задания."""
        def term_with_substituted_digits(term_with_unknown_digits: str, digits_values: Tuple[int, ...]) -> int:
            term_result = 0
            for digit in term_with_unknown_digits:
                term_result *= self.base
                if digit in self.unknown_digits:
                    term_result += digits_values[self.unknown_digits.index(digit)]
                else:
                    term_result += int(digit)
            return term_result
        from itertools import product
        result = []
        for digits_try in product(range(self.base), repeat=len(self.unknown_digits)):
            total_sum = 0
            for term in self.terms:
                total_sum += term_with_substituted_digits(term, digits_try)
            if total_sum % self.divisor == 0:
                result.append(total_sum // self.divisor)
        return result

    def __repr__(self) -> str:
        """Представление задания."""
        result = f'Сумма чисел, записанных в системе счисления с основанием {self.base}:\n'
        result += ' + '.join(self.terms) + '\n'
        result += f'Определите суммы, делящиеся на {self.divisor}. Ответ - частные от деления сумм на это число.'
        return result

    def formula_for_editor(self) -> str:
        """Представление примера в формате, подходящем для копирования в редактор формул."""
        result = ' + '.join(f'"{term}"_{self.base}' for term in self.terms)
        return result
