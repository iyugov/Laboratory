from typing import List, Tuple, Callable
from math import dist, pi, sin, cos, sqrt, log
from turtle import *
from random import uniform, randint, shuffle, random as rnd

from task import Task

def normal(mean: float=0, stddev:float=1) -> float:
    u1 = rnd()
    u2 = rnd()
    z0 = sqrt(-2.0 * log(u1)) * cos(2.0 * pi * u2)
    return z0 * stddev + mean


class TaskClusterization(Task):
    """Задание: даны координаты точек на плоскости.
    Разбить их на заданное количество кластеров по взаимному расстоянию
    и определить средние арифметические координат центров кластеров."""

    center_coordinate_min: float = 0.0
    """Минимальная координата центра дуги кластера."""

    center_coordinate_max: float = 8.0
    """Максимальная координата центра дуги кластера."""

    radius_min: float = 2.0
    """Минимальный радиус дуги кластера."""

    radius_max: float = 6.0
    """Максимальный радиус дуги кластера."""

    arc_phi_min: float = 5 * pi / 6
    """Минимальный угол дуги кластера."""

    arc_phi_max: float = 7 * pi / 6
    """Максимальный угол дуги кластера."""

    standard_deviation: float = 0.2
    """Стандартное отклонение нормального распределения точек относительно дуги кластера."""

    cluster_size_min: int = 400
    """Минимальный размер кластера."""

    cluster_size_max: int = 500
    """Максимальный размер кластера."""

    clusters_count: int = 3
    """Количество кластеров."""

    points_data: List[Tuple[float, ...]]
    """Набор данных: точки."""

    multiplier: int = 10_000
    """Множитель для целочисленного представления ответа."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        self.points_data = []
        for _ in range(self.clusters_count):
            center_x = uniform(self.center_coordinate_min, self.center_coordinate_max)
            center_y = uniform(self.center_coordinate_min, self.center_coordinate_max)
            radius = uniform(self.radius_min, self.radius_max)
            phi_min = uniform(0, 2 * pi)
            phi_max = phi_min + uniform(self.arc_phi_min, self.arc_phi_max)
            cluster_size = randint(self.cluster_size_min, self.cluster_size_max)
            for _ in range(cluster_size):
                phi = uniform(phi_min, phi_max)
                x, y = radius * cos(phi), radius * sin(phi)
                px, py = normal(x, self.standard_deviation), normal(y, self.standard_deviation)
                self.points_data.append((center_x + px, center_y + py))
        shuffle(self.points_data)

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        self.__generate_raw()

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> Tuple[int, int]:
        """Решение задания."""
        centroids = []
        clusters = self.clusterize_for_clusters_count()
        cx, cy = 0, 0
        for cluster in clusters:
            min_d = float('inf')
            for x1, y1 in cluster:
                d = 0.0
                for x2, y2 in cluster:
                    d += dist((x1, y1), (x2, y2))
                if d < min_d:
                    min_d = d
                    cx, cy = x1, y1
            centroids.append((cx, cy))
        sx, sy = 0.0, 0.0
        for x, y in centroids:
            sx += x
            sy += y
        return int(sx / len(centroids) * self.multiplier), int(sy / len(centroids) * self.multiplier)

    def __repr__(self) -> str:
        """Представление задания."""
        def quantity_form(quantity: int, word_forms: Tuple[str, str, str]) -> str:
            """Определение формы слова для количественного числительного"""
            if quantity // 10 % 10 != 1 and quantity == 1:
                return word_forms[0]
            elif quantity // 10 % 10 != 1 and 2 <= quantity <= 4:
                return word_forms[1]
            else:
                return word_forms[2]
        word_form = quantity_form(self.clusters_count, ('кластер', 'кластера', 'кластеров'))
        result = f'Выполнить кластеризацию данных на {self.clusters_count} {word_form}.\n'
        result += f'Вычислить среднее арифметическое координат центров кластеров с множителем {self.multiplier}.'
        return result

    def load_from_file(self, file_name: str) -> None:
        """Загрузка данных из файла."""
        with open(file_name) as input_file:
            input_file.readline()
            self.points_data = [tuple(map(float, line.replace(',', '.').split())) for line in input_file]

    def write_data_to_file(self, file_name: str) -> None:
        """Запись данных в файл."""
        with open(file_name, 'w') as f:
            f.write('X Y\n')
            for x, y in self.points_data:
                s_x = f'{x:.16f}'.replace('.', ',')
                s_y = f'{y:.16f}'.replace('.', ',')
                f.write(f'{s_x} {s_y}\n')

    def clusterize_dbscan(self, epsilon, distance_function: Callable=dist) -> List[List[Tuple[float, ...]]]:
        """Кластеризация по методу DBSCAN."""
        clusters = []
        data = self.points_data[:]
        while data:
            clusters.append([data.pop()])
            for base_point in clusters[-1]:
                for point in data[:]:
                    if distance_function(base_point, point) < epsilon:
                        clusters[-1].append(point)
                        data.remove(point)
        return clusters

    def clusterize_for_clusters_count(self, distance_function=dist):
        """Кластеризация под требуемое количество кластеров (подбор epsilon)."""
        eps_min = 0
        eps_max = max(max(x, y) for x, y in self.points_data) - min(min(x, y) for x, y in self.points_data)
        eps = 0
        clusterization_ok = False
        while not clusterization_ok:
            eps = (eps_max + eps_min) / 2
            clusters = self.clusterize_dbscan(eps, distance_function)
            if len(clusters) < self.clusters_count:
                eps_max = eps
            elif len(clusters) > self.clusters_count:
                eps_min = eps
            else:
                clusterization_ok = True
        return self.clusterize_dbscan(eps, distance_function)

    @staticmethod
    def visualize(clusters: List[List[Tuple[float, ...]]]) -> None:
        """Изображение кластеров."""
        colors = 'blue', 'red', 'green', 'yellow'
        dot_size = 5
        scale = 30
        while len(colors) < len(clusters):
            colors += [colors[-4]]
        up()
        tracer(0)
        for cluster, cluster_color in zip(clusters, colors):
            for x, y in cluster:
                goto(x * scale, y * scale)
                dot(dot_size, cluster_color)
        update()
        Screen().exitonclick()
