"""Количество информации: составные данные."""

from task.task import Task

class TaskInfoAmountCompositeDataTypeA(Task):
    """Количество информации, составные расчёты, тип A:
    Предприятие выпускает партии изделий. Каждая партия получает номер заданной длины из заданного алфавита.
    Изделия в партии получают порядковые номера. Запись о каждом изделии в информационной системе содержит
    код изделия и заданной объём дополнительной информации. Код изделия состоит из номера партии и порядкового номера,
    для этого используется целое число байт. Есть ограничение на общий объём информации, который можно использовать.
    Определить максимальное количество изделий в партии."""

    batch_code_alphabet_length: int = 26
    """Мощность алфавита для кода изделия."""

    batch_code_length_min: int = 10
    """Минимальная кода номера партии."""

    batch_code_length_max: int = 20
    """Максимальная кода номера партии."""

    batch_code_length: int = 0
    """Длина кода партии."""

    total_info_amount_kb_min: int = 10
    """Минимальный общий объём информации, Кбайт."""

    total_info_amount_kb_max: int = 200
    """Максимальный общий объём информации, Кбайт."""

    total_info_amount_kb: int = 0
    """Общий объём информации, Кбайт."""

    extra_info_amount_min: int = 5
    """Минимальный объём дополнительной информации, байт."""

    extra_info_amount_max: int = 100
    """Максимальный объём дополнительной информации, байт."""

    extra_info_amount: int = 0
    """Объём дополнительной информации, байт."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import randint
        self.batch_code_length = randint(self.batch_code_length_min, self.batch_code_length_max)
        self.total_info_amount_kb = randint(self.total_info_amount_kb_min, self.total_info_amount_kb_max)
        self.extra_info_amount = randint(self.extra_info_amount_min, self.extra_info_amount_max)

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        self.__generate_raw()

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> int:
        """Решение задания."""
        from math import ceil
        bits_per_batch_code = len(bin(self.batch_code_alphabet_length - 1)[2:]) * self.batch_code_length

        products_count_ok = True
        products_count = 0
        while products_count_ok:
            products_count += 1
            bits_per_number = len(bin(products_count - 1)[2:])
            bytes_per_product =  ceil((bits_per_batch_code + bits_per_number) / 8) + self.extra_info_amount
            products_count_ok = bytes_per_product * products_count <= self.total_info_amount_kb * 1024
        return products_count - 1


    def __repr__(self) -> str:
        """Представление задания."""
        result = f'Мощность алфавита для кода изделия: {self.batch_code_alphabet_length}.\n'
        result += f'Длина кода партии: {self.batch_code_length}.\n'
        result += f'Объём дополнительной информации: {self.extra_info_amount} байт.\n'
        result += f'Общий объём информации, не более: {self.total_info_amount_kb} Кбайт.\n'
        result += f'Определить максимальное количество изделий в партии.'
        return result


class TaskInfoAmountCompositeDataTypeB(Task):
    """Количество информации, составные расчёты, тип B:
    Известна длина сообщения, составленного из символов некоторого алфавита. Известно, что для хранения N сообщений
    необходимо более X килобайт памяти. Определить минимально возможную мощность алфавита."""

    alphabet_length_min: int = 4
    """Минимальная мощность алфавита."""

    alphabet_length_max: int = 5000
    """Максимальная мощность алфавита."""

    alphabet_length: int = 26
    """Мощность алфавита."""

    message_length_min: int = 10
    """Минимальная длина сообщения."""

    message_length_max: int = 500
    """Максимальная длина сообщения."""

    message_length: int = 100
    """Длина сообщения."""

    message_count_min: int = 10
    """Минимальное количество сообщений."""

    message_count_max: int = 1000
    """Максимальное количество сообщений."""

    message_count: int = 100
    """Количество сообщений."""

    total_info_amount_kb_min: int = 100
    """Минимальный общий объём информации, Кбайт."""

    total_info_amount_kb_max: int = 10_000
    """Максимальный общий объём информации, Кбайт."""

    total_info_amount_kb: int = 1_000
    """Общий объём информации, Кбайт."""


    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import randint
        self.message_length = randint(self.message_length_min, self.message_length_max)
        self.message_count = randint(self.message_count_min, self.message_count_max)
        self.total_info_amount_kb = randint(self.total_info_amount_kb_min, self.total_info_amount_kb_max)

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        solution_ok = False
        while not solution_ok:
            self.__generate_raw()
            solution = self.solve()
            solution_ok = self.alphabet_length_min <= solution <= self.alphabet_length_max

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> int:
        """Решение задания."""
        from math import ceil
        bits_per_symbol = 1
        bits_ok = False
        while not bits_ok:
            if ceil(self.message_length * bits_per_symbol / 8) * self.message_count > self.total_info_amount_kb * 1024:
                bits_ok = True
            else:
                bits_per_symbol += 1
        return (1 << (bits_per_symbol - 1)) + 1


    def __repr__(self) -> str:
        """Представление задания."""
        result = f'Длина сообщения: {self.message_length}.\n'
        result += f'Количество сообщений: {self.message_count}.\n'
        result += f'Общий объём информации, более: {self.total_info_amount_kb} Кбайт.\n'
        result += f'Определить минимально возможную мощность алфавита.'
        return result


class TaskInfoAmountCompositeDataTypeC(Task):
    """Количество информации, составные расчёты, тип C:
    Известна длина сообщения, составленного из символов некоторого алфавита. Известно, что для хранения N сообщений
    необходимо не более X килобайт памяти. Определить максимально возможную мощность алфавита."""

    alphabet_length_min: int = 4
    """Минимальная мощность алфавита."""

    alphabet_length_max: int = 5000
    """Максимальная мощность алфавита."""

    alphabet_length: int = 26
    """Мощность алфавита."""

    message_length_min: int = 10
    """Минимальная длина сообщения."""

    message_length_max: int = 500
    """Максимальная длина сообщения."""

    message_length: int = 100
    """Длина сообщения."""

    message_count_min: int = 10
    """Минимальное количество сообщений."""

    message_count_max: int = 1000
    """Максимальное количество сообщений."""

    message_count: int = 100
    """Количество сообщений."""

    total_info_amount_kb_min: int = 100
    """Минимальный общий объём информации, Кбайт."""

    total_info_amount_kb_max: int = 10_000
    """Максимальный общий объём информации, Кбайт."""

    total_info_amount_kb: int = 1_000
    """Общий объём информации, Кбайт."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import randint
        self.message_length = randint(self.message_length_min, self.message_length_max)
        self.message_count = randint(self.message_count_min, self.message_count_max)
        self.total_info_amount_kb = randint(self.total_info_amount_kb_min, self.total_info_amount_kb_max)

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        solution_ok = False
        while not solution_ok:
            self.__generate_raw()
            solution = self.solve()
            solution_ok = self.alphabet_length_min <= solution <= self.alphabet_length_max

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> int:
        """Решение задания."""
        from math import ceil
        bits_per_symbol = 1
        while ceil(self.message_length * bits_per_symbol / 8) * self.message_count <= self.total_info_amount_kb * 1024:
            bits_per_symbol += 1
        return 1 << (bits_per_symbol - 1)

    def __repr__(self) -> str:
        """Представление задания."""
        result = f'Длина сообщения: {self.message_length}.\n'
        result += f'Количество сообщений: {self.message_count}.\n'
        result += f'Общий объём информации, не более: {self.total_info_amount_kb} Кбайт.\n'
        result += f'Определить максимально возможную мощность алфавита.'
        return result

