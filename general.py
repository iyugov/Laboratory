"""Общие функции для всех модулей."""

from typing import Tuple


def quantity_form(quantity: int, word_forms: Tuple[str, str, str]) -> str:
    """Определение формы слова для количественного числительного"""
    if quantity // 10 % 10 != 1 and quantity % 10 == 1:
        return word_forms[0]
    elif quantity // 10 % 10 != 1 and 2 <= quantity % 10 <= 4:
        return word_forms[1]
    else:
        return word_forms[2]


