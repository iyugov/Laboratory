"""Задания: кодирование графической информации."""
from typing import Tuple, List
from general import quantity_form
from task import Task


class TaskImagesBatchFindHeader(Task):
    """Задание: даны параметры изображений (разрешение, число бит на пиксель), количество изображений в пакете
    и его информационный объём. Определить количество дополнительной информации об одном изображении."""

    resolution_power_min: int = 5
    """Минимальное значение степени двойки для разрешения."""

    resolution_power_max: int = 10
    """Максимальное значение степени двойки для разрешения."""

    resolution_multiplier_min: int = 1
    """Минимальное значение множителя для разрешения."""

    resolution_multiplier_max: int = 10
    """Максимальное значение множителя для разрешения."""

    resolution_x: int = 1024
    """Разрешение по X."""

    resolution_y: int = 768
    """Разрешение по Y."""

    bits_per_pixel_min: int = 1
    """Минимальное значение числа бит на пиксель."""

    bits_per_pixel_max: int = 12
    """Максимальное значение числа бит на пиксель."""

    bits_per_pixel: int = 8
    """Значение числа бит на пиксель."""

    files_in_batch_min: int = 50
    """Минимальное число файлов в пакете."""

    files_in_batch_max: int = 500
    """Максимальное число файлов в пакете."""

    files_in_batch: int = 100
    """Число файлов в пакете."""

    header_size_kb_min: int = 15
    """Минимальный размер заголовка файла в килобайтах."""

    header_size_kb_max: int = 200
    """Максимальный размер заголовка файла в килобайтах."""

    header_size_kb: int = 50
    """Размер заголовка файла в килобайтах."""

    batch_size_mb: int = 0
    """Размер пакета изображений в мегабайтах."""

    header_ratio_max: float = 0.2
    """Максимальное отношение заголовка к основному объёму файла."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import randint
        BITS_TO_BYTES = 8
        BYTES_TO_KB = KB_TO_MB = 1024
        batch_size_kb = 0
        batch_size_is_integer_mb = False
        while not batch_size_is_integer_mb:
            image_size_kb_without_header = 0
            header_ratio_ok = False
            while not header_ratio_ok:
                image_size_bits = 0
                image_size_is_integer_kb = False
                while not image_size_is_integer_kb:
                    resolution_power = randint(self.resolution_power_min, self.resolution_power_max)
                    resolution_multiplier = randint(self.resolution_multiplier_min, self.resolution_multiplier_min)
                    self.resolution_x = resolution_multiplier * 2 ** resolution_power
                    resolution_power = randint(self.resolution_power_min, self.resolution_power_max)
                    resolution_multiplier = randint(self.resolution_multiplier_min, self.resolution_multiplier_min)
                    self.resolution_y = resolution_multiplier * 2 ** resolution_power
                    self.bits_per_pixel = randint(self.bits_per_pixel_min, self.bits_per_pixel_max)
                    image_size_bits = self.resolution_x * self.resolution_y * self.bits_per_pixel
                    image_size_is_integer_kb = image_size_bits % (BITS_TO_BYTES * BYTES_TO_KB) == 0
                image_size_kb_without_header = image_size_bits // (BITS_TO_BYTES * BYTES_TO_KB)
                self.header_size_kb = randint(self.header_size_kb_min, self.header_size_kb_max)
                header_ratio_ok = self.header_size_kb / image_size_kb_without_header <= self.header_ratio_max
            image_size_kb = image_size_kb_without_header + self.header_size_kb
            self.files_in_batch = randint(self.files_in_batch_min, self.files_in_batch_max)
            batch_size_kb = image_size_kb * self.files_in_batch
            batch_size_is_integer_mb = batch_size_kb % KB_TO_MB == 0
        self.batch_size_mb = batch_size_kb // KB_TO_MB

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        self.__generate_raw()

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> int:
        """Решение задания."""
        MB_TO_KB = BYTES_TO_KB = 1024
        BITS_TO_BYTES = 8
        batch_size_kb = self.batch_size_mb * MB_TO_KB
        image_size_kb = batch_size_kb // self.files_in_batch
        image_size_without_header = self.resolution_x * self.resolution_y * self.bits_per_pixel
        image_size_without_header_kb = image_size_without_header // (BITS_TO_BYTES * BYTES_TO_KB)
        header_kb = image_size_kb - image_size_without_header_kb
        return header_kb


    def __repr__(self) -> str:
        """Представление задания."""
        result = f'Изображения: {self.resolution_x}x{self.resolution_y}, '
        colors = 2 ** self.bits_per_pixel
        result += f'{colors} {quantity_form(colors, ('цвет', 'цвета', 'цветов'))}. '
        result += f'Изображений в пакете: {self.files_in_batch}. '
        result += f'Объём пакета: {self.batch_size_mb} Мбайт.\n'
        result += 'Определить размер заголовка одного файла.'
        return result

    def solution(self) -> str:
        """Ход решения."""
        MB_TO_KB = BYTES_TO_KB = 1024
        BITS_TO_BYTES = 8
        result = '1. Переведём объём пакета изображений в килобайты:\n'
        batch_size_kb = self.batch_size_mb * MB_TO_KB
        result += f'   {self.batch_size_mb} * {MB_TO_KB} = {batch_size_kb} (Кбайт)\n'
        result += '2. Определим объём одного изображения в килобайтах:\n'
        image_size_kb = batch_size_kb // self.files_in_batch
        result += f'   {batch_size_kb} : {self.files_in_batch} = {image_size_kb} (Кбайт)\n'
        result += '3. Определим число бит на пиксель (глубину цвета) по числу цветов:\n'
        result += f'   {2 ** self.bits_per_pixel} = 2^{self.bits_per_pixel}, '
        result += f'   глубина цвета - {self.bits_per_pixel} {quantity_form(self.bits_per_pixel, ('бит', 'бита', 'бит'))}.\n'
        result += '4. Определим объём изображения без заголовка в битах по формуле I = H * W * b, где:\n'
        result += '   I - информационный объём изображения в битах,\n'
        result += '   H - вертикальное разрешение изображения,\n'
        result += '   W - горизонтальное разрешение изображения,\n'
        result += '   b - число бит на пиксель (глубина цвета):\n'
        image_size_without_header = self.resolution_x * self.resolution_y * self.bits_per_pixel
        result += f'   {self.resolution_x} * {self.resolution_y} * {self.bits_per_pixel} '
        result += f'= {image_size_without_header} (бит)\n'
        result += '5. Переведём объём изображения без заголовка в килобайты:\n'
        image_size_without_header_kb = image_size_without_header // (BITS_TO_BYTES * BYTES_TO_KB)
        result += f'   {image_size_without_header} : {BITS_TO_BYTES} : {BYTES_TO_KB} '
        result += f'= {image_size_without_header_kb} (Кбайт)\n'
        result += '6. Определим размер заголовка изображения:\n'
        header_kb = image_size_kb - image_size_without_header_kb
        result += f'   {image_size_kb} - {image_size_without_header_kb} = {header_kb} (Кбайт)\n'
        result += f'Ответ: {header_kb}'
        return result


class TaskImagesConversionAndCompressionFindCompressionPercentage(Task):
    """Задание: даны параметры изображения (разрешение, информационный объём, процент сжатия) в двух вариантах.
    Цветовая глубина и геометрические размеры изображений одинаков. Один процент сжатия неизвестен. Найти его."""

    dpi_values: Tuple[int] = (72, 96, 150, 300, 600, 1200, 2400, 4800)
    """Доступные значения разрешения изображения (dpi)."""

    compression_rate_min: int = 5
    """Минимальный коэффициент сжатия изображения в процентах."""

    compression_rate_max: int = 95
    """Максимальный коэффициент сжатия изображения в процентах."""

    amount_mb_min: int = 1
    """Минимальный информационный объём изображения в Мб."""

    amount_mb_max: int = 200
    """Максимальный информационный объём изображения в Мб."""

    dpi: List[int] = []
    """Разрешение изображений."""

    compression_rate: int = 0
    """Процент сжатия первого изображения."""

    amount_of_information_mb: List[int] = []
    """Информационный объём изображений."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import randint, choice
        dpi1, dpi2 = 0, 0
        while dpi1 == dpi2:
            dpi1 = choice(self.dpi_values)
            dpi2 = choice(self.dpi_values)
        self.dpi = [dpi1, dpi2]
        amount_mb1, amount_mb2 = 0, 0
        while amount_mb1 == amount_mb2:
            amount_mb1 = randint(self.amount_mb_min, self.amount_mb_max)
            amount_mb2 = randint(self.amount_mb_min, self.amount_mb_max)
        self.amount_mb = [amount_mb1, amount_mb2]
        self.compression_rate = randint(self.compression_rate_min, self.compression_rate_max)

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        solution_ok = False
        while not solution_ok:
            self.__generate_raw()
            solution = self.solve()
            solution_ok = self.compression_rate_min <= solution <= self.compression_rate_max

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> int:
        """Решение задания."""
        mb1, mb2 = self.amount_mb
        dpi1, dpi2 = self.dpi
        rate = self.compression_rate
        return round(100 * (1 - mb2 * dpi1**2 * (1 - rate / 100) / mb1 / dpi2**2))

    def __repr__(self) -> str:
        """Представление задания."""
        result = f'Изображение №1: {self.dpi[0]} dpi, сжато на {self.compression_rate}%, {self.amount_mb[0]} Мб.\n'
        result += f'Изображение №2: {self.dpi[1]} dpi, сжато на X%, {self.amount_mb[1]} Мб.\n'
        result += 'Найти X. Результат округлять до ближайшего целого.'
        return result