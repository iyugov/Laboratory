"""Базовый класс для заданий."""


class Task:
    """Базовый класс для заданий."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        self.__generate_raw()

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> None:
        """Решение задания."""

    def __repr__(self) -> str:
        """Представление задания."""
        return 'Общее задание.'
