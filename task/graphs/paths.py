"""Задания: пути по графу и матрице."""
from csv import writer
from typing import Any

from task import Task

class TaskGraphPath(Task):
    """Задание: дана весовая матрица неориентированного графа.
    Определить длину кратчайшего пути между двумя вершинами, проходящего через заданную промежуточную вершину."""

    vertices_count: int = 7
    """Количество вершин в графе."""

    edges_count_min: int = 9
    """Минимальное количество рёбер в графе."""

    edges_count_max: int = 13
    """Максимальное количество рёбер в графе."""

    edges_count: int = 10
    """Количество рёбер в графе."""

    edge_weight_min: int = 1
    """Минимальный вес рёбер в графе."""

    edge_weight_max: int = 15
    """Максимальный вес рёбер в графе."""

    weights_matrix: list[list[int | float]] = []
    """Весовая матрица."""

    start_vertex: int = 0
    """Начальная вершина пути (индекс)."""

    end_vertex: int = 5
    """Конечная вершина пути (индекс)."""

    intermediate_vertex: int = 2
    """Промежуточная вершина пути (индекс)."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__()
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без проверки."""
        from random import randint, shuffle
        vertices = list(range(self.vertices_count))
        shuffle(vertices)
        self.start_vertex = vertices[0]
        self.end_vertex = vertices[1]
        self.intermediate_vertex = vertices[2]
        self.edges_count = randint(self.edges_count_min, self.edges_count_max)
        edges = {}
        weights = set()
        while len(edges) < self.edges_count:
            row = randint(0, self.vertices_count - 1)
            col = randint(0, self.vertices_count - 1)
            weight = randint(self.edge_weight_min, self.edge_weight_max)
            if row != col and (row, col) not in edges and (col, row) not in edges and weight not in weights:
                edges[(row, col)] = weight
                weights.add(weight)
        self.weights_matrix = [[float('inf')] * self.vertices_count for _ in range(self.vertices_count)]
        for (row, col), weight in edges.items():
            self.weights_matrix[row][col] = weight
            self.weights_matrix[col][row] = weight


    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        solution_ok = False
        while not solution_ok:
            self.__generate_raw()
            start_vertex, end_vertex, intermediate_vertex = self.start_vertex, self.end_vertex, self.intermediate_vertex
            all_paths = self.generate_all_paths(start_vertex, end_vertex, intermediate_vertex, None)
            if not all_paths:
                continue
            best_path = min(all_paths,  key=lambda x: x[1])
            solution = best_path[1]
            paths_without_intermediate = self.generate_all_paths(start_vertex, end_vertex, None, None)
            if not paths_without_intermediate:
                continue
            best_path_without_intermediate = min(paths_without_intermediate, key=lambda x: x[1])
            solution_without_intermediate = best_path_without_intermediate[1]
            if solution == solution_without_intermediate:
                continue
            all_paths_first = self.generate_all_paths(start_vertex, intermediate_vertex, None, end_vertex)
            if not all_paths_first:
                continue
            best_path_first = min(all_paths_first, key=lambda x: x[1])
            solution_first = best_path_first[1]
            all_paths_second = self.generate_all_paths(intermediate_vertex, end_vertex, None, start_vertex)
            if not all_paths_second:
                continue
            best_path_second = min(all_paths_second, key=lambda x: x[1])
            solution_second = best_path_second[1]
            if solution_first + solution_second >= solution:
                continue
            solution_ok = True
        self.write_matrix_to_file(self.weights_matrix, True, 'weights_matrix.csv')


    def generate(self) -> None:
        """Генерация задания."""
        self.__generate()

    def solve(self) -> int | None:
        """Решение задания."""
        all_paths = self.generate_all_paths(self.start_vertex, self.end_vertex, self.intermediate_vertex, None)
        return min(all_paths, key=lambda x: x[1])[1] if all_paths else None

    def get_path_weight(self, path: list[int]) -> int:
        """Вычисление веса пути."""
        weight = 0
        for i in range(len(path) - 1):
            weight += self.weights_matrix[path[i]][path[i + 1]]
        return weight

    def generate_all_paths(self, start: int, end: int, intermediate: int | None, excluded: int | None) -> list[tuple[list[int], int]]:
        """Генерация всех возможных путей от start до end через intermediate."""

        def generate_all_paths_recursive(_current: int, _end: int, _intermediate: int | None, _excluded: int | None) -> list[tuple[list[int], int]]:
            if _current == _end and (_intermediate in visited or _intermediate is None) and (_excluded is None or _excluded not in visited):
                return [(current_path.copy(), self.get_path_weight(current_path))]
            paths = []
            for next_vertex in range(self.vertices_count):
                if next_vertex not in visited and self.weights_matrix[_current][next_vertex] != float('inf'):
                    visited.add(next_vertex)
                    current_path.append(next_vertex)
                    paths.extend(generate_all_paths_recursive(next_vertex, _end, _intermediate, _excluded))
                    current_path.pop()
                    visited.remove(next_vertex)
            return paths

        visited = {start}
        current_path = [start]
        return generate_all_paths_recursive(start, end, intermediate, excluded)


    @staticmethod
    def make_matrix_text(matrix: list[list[int | float]], show_numbers: bool = False, weighted: bool = True) -> str:
        result = ' ' * 4
        for col in range(len(matrix)):
            result += f'{f"П{col + 1}": >4}' if show_numbers else f'{chr(col + ord('A')): >4}'
        result += '\n'
        for col in range(len(matrix)):
            result += f'{f"П{col + 1}": >4}' if show_numbers else f'{chr(col + ord('A')): >4}'
            if weighted:
                result += ''.join([f'{item: >4}' if item != float('inf') else f'{"-": >4}' for item in matrix[col]])
            else:
                result += ''.join([f'{"*": >4}' if item != float('inf') else f'{"-": >4}' for item in matrix[col]])
            result += '\n'
        return result

    @staticmethod
    def write_matrix_to_file(matrix: list[list[int | float]], weighted: bool, file_name: str) -> None:
        """Запись матрицы в файл CSV."""
        text_matrix = [[''] * len(matrix) for _ in range(len(matrix))]
        with open(file_name, 'w') as file_out:
            csv_writer = writer(file_out, delimiter=',')
            for row in range(len(matrix)):
                for col in range(len(matrix)):
                    if row == col:
                        text_matrix[row][col] = '—'
                    elif matrix[row][col] == float('inf'):
                        text_matrix[row][col] = ''
                    elif not weighted:
                        text_matrix[row][col] = '*'
                    else:
                        text_matrix[row][col] = str(matrix[row][col])
            csv_writer.writerows(text_matrix)

    def __repr__(self) -> str:
        """Представление задания."""
        start_vertex = chr(self.start_vertex + ord('A'))
        end_vertex = chr(self.end_vertex + ord('A'))
        intermediate_vertex = chr(self.intermediate_vertex + ord('A'))
        result = f'Весовая матрица графа:\n'
        result += self.make_matrix_text(self.weights_matrix)
        result += f'Найти кратчайший путь от вершины {start_vertex} до вершины {end_vertex},\n'
        result += f'проходящий через вершину {intermediate_vertex}.\n'
        return result

