"""Задания: кодирование видео."""
from typing import Tuple, List
from general import quantity_form
from task import Task


class TaskVideoFindTransferTime(Task):
    """Задание: даны параметры передачи видео:
    - параметры кодирования кадров как изображений;
    - параметры количества кадров;
    - параметры дополнительного сжатия видео;
    - параметры кодирования звука;
    - параметры сжатия звука;
    - параметры передачи данных (скорость).
    Определить время передачи видео."""

    frame_resolutions: Tuple[Tuple[int, int], ...] = ((640, 480), (1280, 720), (1920, 1080), (3840, 2160))
    """Размеры кадра в пикселях."""

    frame_resolution: Tuple[int, int] = (640, 480)
    """Размер кадра в пикселях."""

    frame_bit_depth_min: int = 4
    """Минимальная глубина цвета (число бит на пиксель)."""

    frame_bit_depth_max: int = 32
    """Максимальная глубина цвета (число бит на пиксель)."""

    frame_bit_depth: int = 24
    """Глубина цвета (число бит на пиксель)."""

    frames_compression_rate_min: int = 5
    """Минимальный коэффициент сжатия видеоряда в процентах."""

    frames_compression_rate_max: int = 100
    """Максимальный коэффициент сжатия видеоряда в процентах."""

    frames_compression_rate: int = 50
    """Коэффициент сжатия видеоряда в процентах."""

    frames_per_second_values: Tuple[int, ...] = (24, 25, 30, 50, 60, 120)
    """Доступные значения частоты кадров в секунду."""

    frames_per_second: int = 30
    """Частота кадров в секунду."""

    video_time_min: int = 10
    """Минимальное время видео в секундах."""

    video_time_max: int = 3600
    """Максимальное время видео в секундах."""

    video_time: int = 60
    """Время видео в секундах."""

    audio_bit_depth_min: int = 8
    """Минимальная глубина звука (число бит на сэмпл)."""

    audio_bit_depth_max: int = 32
    """Максимальная глубина звука (число бит на сэмпл)."""

    audio_bit_depth: int = 16
    """Глубина звука (число бит на сэмпл)."""

    audio_sample_rate_values: Tuple[int, ...] = (8000, 11025, 16000, 22050, 44100, 48000, 96000, 192000)
    """Доступные значения частоты дискретизации звука (Гц)."""

    audio_sample_rate: int = 44100
    """Частота дискретизации звука (Гц)."""

    audio_compression_rate_min: int = 10
    """Минимальный коэффициент сжатия звука в процентах."""

    audio_compression_rate_max: int = 80
    """Максимальный коэффициент сжатия звука в процентах."""

    audio_compression_rate: int = 50
    """Коэффициент сжатия звука в процентах."""

    audio_channels_values: Tuple[int, ...] = (2, 4, 6, 8)
    """Доступные значения числа каналов звука."""

    audio_channels: int = 2
    """Число каналов звука."""

    data_transfer_rate_min: int = 1_000_000
    """Минимальная скорость передачи данных в битах в секунду."""

    data_transfer_rate_max: int = 1_000_000_000
    """Максимальная скорость передачи данных в битах в секунду."""

    data_transfer_divisor: int = 100_000
    """Делитель для округления скорости передачи данных в битах в секунду."""

    data_transfer_rate: int = 10_000_000
    """Скорость передачи данных в битах в секунду."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import randint, choice
        self.frame_resolution = choice(self.frame_resolutions)
        self.frame_bit_depth = randint(self.frame_bit_depth_min, self.frame_bit_depth_max)
        self.frames_compression_rate = randint(self.frames_compression_rate_min, self.frames_compression_rate_max)
        self.frames_per_second = choice(self.frames_per_second_values)
        self.video_time = randint(self.video_time_min, self.video_time_max)
        self.audio_bit_depth = randint(self.audio_bit_depth_min, self.audio_bit_depth_max)
        self.audio_sample_rate = choice(self.audio_sample_rate_values)
        self.audio_compression_rate = randint(self.audio_compression_rate_min, self.audio_compression_rate_max)
        self.audio_channels = choice(self.audio_channels_values)
        self.data_transfer_rate = randint(self.data_transfer_rate_min, self.data_transfer_rate_max)
        self.data_transfer_rate = (self.data_transfer_rate // self.data_transfer_divisor) * self.data_transfer_divisor


    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        bytes_ok = False
        while not bytes_ok:
            self.__generate_raw()
            frame_size = (self.frame_resolution[0] * self.frame_resolution[1] * self.frame_bit_depth)
            if frame_size % 8 != 0:
                continue
            frames_size = frame_size * self.frames_per_second * self.video_time
            if frames_size % self.frames_compression_rate != 0:
                continue
            frames_size_compressed = frames_size // self.frames_compression_rate
            if frames_size_compressed % 8 != 0:
                continue
            audio_size = (self.audio_sample_rate * self.audio_bit_depth * self.audio_channels * self.video_time)
            if audio_size % 8 != 0:
                continue
            if audio_size % (100 - self.audio_compression_rate) != 0:
                continue
            audio_size_compressed = audio_size * (100 - self.audio_compression_rate) // 100
            if audio_size_compressed % 8 != 0:
                continue
            bytes_ok = True
        self.__generate_raw()

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> int:
        """Решение задания."""
        frame_size = (self.frame_resolution[0] * self.frame_resolution[1] * self.frame_bit_depth)
        frames_size = frame_size * self.frames_per_second * self.video_time
        frames_size_compressed = frames_size // self.frames_compression_rate
        audio_size = (self.audio_sample_rate * self.audio_bit_depth * self.audio_channels * self.video_time)
        audio_size_compressed = audio_size * (100 - self.audio_compression_rate) // 100
        total_size = frames_size_compressed + audio_size_compressed
        transfer_time = total_size // self.data_transfer_rate
        return int(transfer_time)


    def __repr__(self) -> str:
        """Представление задания."""
        result = f'Время видео: {self.video_time // 60} м {self.video_time % 60} сек.\n'
        result += f'Скорость передачи данных: {self.data_transfer_rate // 1000} Кбит/сек.\n'
        result += f'Частота кадров: {self.frames_per_second} кадр/сек.\n'
        result += f'Разрешение кадра: {self.frame_resolution[0]}x{self.frame_resolution[1]} пикселей.\n'
        result += f'Глубина цвета: {self.frame_bit_depth} бит/пиксель.\n'
        result += f'Коэффициент сжатия видеоряда: {self.frames_compression_rate} раз.\n'
        result += f'Число каналов звука: {self.audio_channels}.\n'
        result += f'Частота дискретизации звука: {self.audio_sample_rate} Гц.\n'
        result += f'Глубина звука: {self.audio_bit_depth} бит/сэмпл.\n'
        result += f'Сжатие уменьшило размер звука на {self.audio_compression_rate}%.\n'
        result += 'Определить время передачи видео в секундах. '
        result += 'Результат округлять вниз.'
        return result

    def solution(self) -> str:
        """Ход решения."""
        result = 'Решение:\n'
        frame_size = (self.frame_resolution[0] * self.frame_resolution[1] * self.frame_bit_depth)
        result += f'Размер кадра: {self.frame_resolution[0]} * {self.frame_resolution[1]} * {self.frame_bit_depth} бит = {frame_size} бит '
        frames_size = frame_size * self.frames_per_second * self.video_time
        result += f'Размер видеоряда: {self.frames_per_second} кадр/сек * {self.video_time} сек = {frames_size} бит.\n'
        frames_size_compressed = frames_size // self.frames_compression_rate
        result += f'Сжатый видеоряд: {frames_size} бит / {self.frames_compression_rate} = {frames_size_compressed} бит ({frames_size_compressed / 8} байт).\n'
        audio_size = (self.audio_sample_rate * self.audio_bit_depth * self.audio_channels * self.video_time)
        result += f'Размер звука: {self.audio_sample_rate} Гц * {self.audio_bit_depth} бит/сэмпл * {self.audio_channels} каналов * {self.video_time} сек = {audio_size} бит.\n'
        audio_size_compressed = audio_size * (100 - self.audio_compression_rate) // 100
        result += f'Сжатый звук: {audio_size} бит * (100 - {self.audio_compression_rate}) / 100 = {audio_size_compressed} бит ({audio_size_compressed / 8} байт).\n'
        total_size = frames_size_compressed + audio_size_compressed
        result += f'Общий размер: {frames_size_compressed} бит + {audio_size_compressed} бит = {total_size} бит ({total_size / 8} байт).\n'
        transfer_time = total_size / self.data_transfer_rate
        result += f'Время передачи: {total_size} бит / {self.data_transfer_rate} бит/сек = {transfer_time:1.4f} сек.\n'
        result += f'\nОтвет: {int(transfer_time)} сек.'
        return result
