"""Базовый класс для заданий."""


class Task:
    """Базовый класс для заданий."""

    __generated: bool = False
    __loaded: bool = False

    @property
    def generated(self) -> bool:
        """Свойство - сгенерировано ли задание."""
        return self.__generated

    @property
    def loaded(self) -> bool:
        """Свойство - загружено ли задание из файла."""
        return self.__loaded

    def __init__(self, generate: bool = False):
        """Конструктор подходящего примера."""
        if generate:
            self.generate()

    def solve(self):
        """Решает задание."""
        assert self.generated or self.loaded

    def __generate_raw(self) -> None:
        """Генерирует параметры условия без основной проверки."""

    def __generate(self) -> None:
        """Генерирует параметры условия с основной проверкой."""

    def generate(self) -> None:
        """Генерирует параметры условия."""
        self.__generate()
        self.__generated = True

    def load_from_file(self) -> None:
        """Загружает данные из файла."""
        self.__loaded = True

    def __repr__(self) -> str:
        """Представление задания."""
        return 'Общее задание.' if self.generated or self.loaded else 'Общее задание (не сгенерировано).'
