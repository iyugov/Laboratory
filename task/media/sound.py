"""Задания: кодирование звуковой информации."""
from typing import Tuple
from general import quantity_form
from task import Task

class TaskSoundAlbumFindTransmissionTime(Task):
    """Задание: по каналу связи передаётся звуковой альбом с известными параметрами кодирования звука,
    количеством треков и размером заголовков.
    Определить время его передачи по каналу связи с заданной скоростью."""

    track_count_min: int = 10
    """Минимальное количество треков."""

    track_count_max: int = 20
    """Максимальное количество треков."""

    track_count: int = 0
    """Количество треков."""

    header_size_kb_min: int = 50
    """Минимальный размер заголовка в Кб."""

    header_size_kb_max: int = 150
    """Максимальный размер заголовка в Кб."""

    header_size_kb: int = 0
    """Размер заголовка в Кб."""

    overall_time_sec_min: int = 3000
    """Минимальное общее время альбома в секундах."""

    overall_time_sec_max: int = 4000
    """Максимальное общее время альбома в секундах."""

    overall_time_sec: int = 0
    """Общее время альбома в секундах."""

    sampling_rate_values: Tuple[int] = (16000, 24000, 32000, 40000, 44000, 48000, 60000, 96000)
    """Доступные значения частоты дискретизации звука."""

    sampling_rate: int = 0
    """Частота дискретизации звука."""

    bit_depth_values: Tuple[int] = (16, 24, 32, 36, 40, 48)
    """Доступные значения разрядности звука."""

    bit_depth: int = 0
    """Разрядность звука."""

    channel_count_values: Tuple[int] = (1, 2, 4)
    """Доступные значения количества каналов звука."""

    channel_count: int = 0
    """Количество каналов звука."""

    transmission_speed_mbps_min: int = 100
    """Минимальная скорость передачи данных по каналу связи в Мбит/с."""

    transmission_speed_mbps_max: int = 1000
    """Максимальная скорость передачи данных по каналу связи в Мбит/с."""

    transmission_speed_mbps: int = 0
    """Скорость передачи данных по каналу связи в Мбит/с."""

    transmission_time_min: int = 1
    """Минимальное время передачи альбома в секундах."""

    transmission_time_max: int = 1000
    """Максимальное время передачи альбома в секундах."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import randint, choice
        self.track_count = randint(self.track_count_min, self.track_count_max)
        self.header_size_kb = randint(self.header_size_kb_min, self.header_size_kb_max)
        self.overall_time_sec = randint(self.overall_time_sec_min, self.overall_time_sec_max)
        self.sampling_rate = choice(self.sampling_rate_values)
        self.bit_depth = choice(self.bit_depth_values)
        self.channel_count = choice(self.channel_count_values)
        self.transmission_speed_mbps = randint(self.transmission_speed_mbps_min, self.transmission_speed_mbps_max)

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        self.__generate_raw()

    def generate(self) -> None:
        """Генерация параметров условия."""
        solution_ok = False
        while not solution_ok:
            self.__generate()
            solution = self.solve()
            solution_wrong = self.solve_wrong()
            solution_ok = solution != solution_wrong
            solution_ok = solution_ok and self.transmission_time_min <= solution <= self.transmission_time_max

    def solve(self) -> int:
        """Решение задания."""
        sound_size_bit = self.overall_time_sec * self.sampling_rate * self.bit_depth * self.channel_count
        track_headers_size_bit = self.track_count * self.header_size_kb * 8 * 1024
        total_size_bit = sound_size_bit + track_headers_size_bit
        return total_size_bit // (self.transmission_speed_mbps * 1_000_000)

    def solve_wrong(self) -> int:
        """Решение задания: неверное, с игнорированием объёма треков."""
        sound_size_bit = self.overall_time_sec * self.sampling_rate * self.bit_depth * self.channel_count
        return sound_size_bit // (self.transmission_speed_mbps * 1_000_000)

    def solution(self) -> str:
        """Ход решения."""
        result = '1. Определим информационный объём звука по формуле I_зв = t * f * b * k, где\n'
        result += '     I_зв - информационный объём звука в битах,\n'
        minutes = self.overall_time_sec // 60
        seconds = self.overall_time_sec % 60
        result += f'     t - общее время альбома в секундах ({minutes} * 60 + {seconds} = {self.overall_time_sec}),\n'
        result += f'     f - частота дискретизации звука в Гц ({self.sampling_rate}),\n'
        result += f'     b - разрядность звука в битах ({self.bit_depth}),\n'
        result += f'     k - количество каналов звука ({self.channel_count}).\n'
        sound_size_bit = self.overall_time_sec * self.sampling_rate * self.bit_depth * self.channel_count
        result += f'   I_зв = {self.overall_time_sec} * {self.sampling_rate} * {self.bit_depth} * {self.channel_count} '
        result += f'= {sound_size_bit:_d} (бит)\n'
        result += f'2. Определим информационный объём заголовков I_заг:\n'
        track_headers_size_bit = self.track_count * self.header_size_kb * 8 * 1024
        result += f'   I_заг = {self.track_count} * {self.header_size_kb} * 8 * 1024 = {track_headers_size_bit:_d} (бит)\n'
        total_size_bit = sound_size_bit + track_headers_size_bit
        result += f'3. Определим общий информационный объём:\n'
        result += f'   I_общ = I_зв + I_заг = {total_size_bit:_d} (бит)\n'
        result += f'4. Определим время передачи альбома по каналу связи по формуле t = I / V:\n'
        transmission_time = total_size_bit / (self.transmission_speed_mbps * 1_000_000)
        result += f'   t = {total_size_bit:_d} / {self.transmission_speed_mbps * 1_000_000:_d} = '
        result += f'{transmission_time:.5f} (с)\n'
        transmission_time_int = int(transmission_time)
        result += f'5. Целая часть числа {transmission_time:.5f} равна {transmission_time_int}.\n'
        result += f'Ответ: {transmission_time_int}.'

        return result

    def __repr__(self) -> str:
        """Представление задания."""
        channel_values = {1: 'одноканальном (моно)', 2: 'двухканальном (стерео)', 4: 'четырёхканальном (квадро)'}
        result = f'Звуковой альбом закодирован в {channel_values[self.channel_count]} формате с частотой дискретизации '
        result += f'{self.sampling_rate} Гц и разрешением {self.bit_depth} бит без сжатия.\n'
        track_form = quantity_form(self.track_count, ('трек', 'трека', 'треков'))
        minutes = self.overall_time_sec // 60
        minutes_form = quantity_form(minutes, ('минута', 'минуты', 'минут'))
        seconds = self.overall_time_sec % 60
        seconds_form = quantity_form(seconds, ('секунда', 'секунды', 'секунд'))
        time_form = f'{minutes} {minutes_form} {seconds} {seconds_form}'
        result += f'Альбом содержит {self.track_count} {track_form} общей продолжительностью {time_form}. '
        result += f'Каждый трек содержит заголовок объёмом {self.header_size_kb} Кбайт.\n'
        result += f'Определите, сколько секунд будет загружаться альбом по каналу связи со скоростью '
        result += f'{self.transmission_speed_mbps * 1_000_000:_d} бит/с.\n'
        result += f'В ответе запишете только целую часть полученного числа.'
        return result