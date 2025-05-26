"""Задания: соотнесение таблицы и графа."""

from csv import writer
from itertools import permutations
from random import randint, shuffle
from typing import Tuple

import networkx
import matplotlib.pyplot

from task import Task


class TaskGraphsMatchTable(Task):
    """Задание: неориентированный граф и таблица истинности с перепутанными строками.
    Соотнести вершины в таблице и в графе."""

    alphabet: str = 'ABCDEFGHIJKLONOPQRSTUVWXYZ'
    # Алфавит для обозначения вершин

    edges: str = 'AB AC AD BD BE CD CF DE EG FG'
    # Рёбра графа в виде пар вершин, разделённые пробелами

    weighted: bool = True
    # Является ли граф взвешенным

    shuffled_matrix: list[list[int | float]]
    # Перепутанная весовая матрица

    solve_for_weights_sum: tuple[str, ...] = ()
    # Что нужно найти: сумма весов конкретных рёбер (в частности, вес одного ребра)

    solve_for_vertices: str = ''
    # Что нужно найти: конкретные вершины

    solve_for_shortest_distance: str = ''
    # Что нужно найти: кратчайшее расстояние между конкретными вершинами

    bad_edge_present: bool = False
    # Есть ли в таблице неправильное ребро

    shuffled_matrix_file_name: str = 'graph.csv'
    # Имя файла для сохранения перепутанной весовой матрицы

    solution_count_min: int = 1
    # Минимальное требуемое число решений

    solution_count_max: int = 1
    # Максимальное требуемое число решений

    constraints: Tuple[str] = tuple()
    # Ограничения на соотношения между весами рёбер (проверяется их конъюнкция)

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__()
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без проверки."""

        def make_weights_matrix(matrix: list[list[int]]) -> list[list[int | float]]:
            """Создание весовой матрицы по матрице смежности."""

            def generate_weights(weights_count: int, unique_pairwise_sums: bool = False):
                """Генерация весов рёбер так, чтобы и они сами, и их попарные суммы были уникальными."""
                if weights_count == 0:
                    return []
                if unique_pairwise_sums:
                    # Максимальная разница весов рёбер
                    weight_max_gap = 2
                    generated_weights = [randint(1, weight_max_gap)]
                    weight_to_try = generated_weights[-1] + randint(1, weight_max_gap)
                    pairwise_sums = set()
                    for _ in range(weights_count - 1):
                        sums_are_unique = False
                        while not sums_are_unique:
                            sums_are_unique = True
                            for current_weight in generated_weights:
                                if (current_weight + weight_to_try) in pairwise_sums:
                                    sums_are_unique = False
                                    break
                            if not sums_are_unique:
                                weight_to_try += randint(1, weight_max_gap)
                        for current_weight in generated_weights:
                            pairwise_sums.add(current_weight + weight_to_try)
                        generated_weights.append(weight_to_try)
                else:
                    # Максимальная разница весов рёбер
                    weight_max_gap = 5
                    generated_weights = [randint(1, weight_max_gap)]
                    for _ in range(weights_count - 1):
                        generated_weights.append(generated_weights[-1] + randint(1, weight_max_gap))
                shuffle(generated_weights)
                return generated_weights

            edges_count = 0
            for row in range(len(matrix)):
                for col in range(row + 1, len(matrix)):
                    if adjacency_matrix[row][col] == 1:
                        edges_count += 1
            if self.weighted:
                weights = generate_weights(edges_count, unique_pairwise_sums=len(self.solve_for_weights_sum) > 1)
            else:
                weights = [1] * edges_count
            result = [[float('inf')] * len(matrix) for _ in range(len(matrix))]
            weight_index = 0
            for row in range(len(matrix)):
                for col in range(row + 1, len(matrix)):
                    if adjacency_matrix[row][col] == 1:
                        result[row][col] = weights[weight_index]
                        result[col][row] = weights[weight_index]
                        weight_index += 1
            return result

        def make_shuffled_matrix(matrix: list[list[int | float]]) -> list[list[int | float]]:
            """Перепутывание вершин в матрице."""
            pointers: list[int] = list(range(len(matrix)))
            shuffle(pointers)
            result: list[list[int | float]] = [[0] * len(matrix) for _ in range(len(matrix))]
            for row in range(len(matrix)):
                for col in range(len(matrix)):
                    result[pointers[row]][pointers[col]] = matrix[row][col]
            return result

        # Преобразование и проверка списка рёбер
        edges_list = self.make_edges_list(self.edges)
        # Создание матрицы смежности
        adjacency_matrix = self.make_adjacency_matrix(edges_list)
        # Создание весов рёбер
        weights_matrix = make_weights_matrix(adjacency_matrix)
        # Создание перепутанной весовой матрицы
        self.shuffled_matrix = make_shuffled_matrix(weights_matrix)
        if self.bad_edge_present:
            edge_changed = False
            while not edge_changed:
                vertices_count = len(self.shuffled_matrix)
                vertex_start = randint(1, vertices_count) - 1
                vertex_end_old = randint(1, vertices_count) - 1
                vertex_end_new = randint(1, vertices_count) - 1
                vertices = {vertex_start, vertex_end_old, vertex_end_new}
                if len(vertices) < 3:
                    continue
                if self.shuffled_matrix[vertex_start][vertex_end_old] == float('inf'):
                    continue
                if self.shuffled_matrix[vertex_start][vertex_end_new] < float('inf'):
                    continue
                weight = self.shuffled_matrix[vertex_start][vertex_end_old]
                self.shuffled_matrix[vertex_start][vertex_end_old] = float('inf')
                self.shuffled_matrix[vertex_end_old][vertex_start] = float('inf')
                self.shuffled_matrix[vertex_start][vertex_end_new] = weight
                self.shuffled_matrix[vertex_end_new][vertex_start] = weight
                edge_changed = True

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        solution_ok = False
        while not solution_ok:
            self.__generate_raw()
            solution = self.solve()
            solution_ok = self.solution_count_min <= len(solution) <= self.solution_count_max
        # Запись перепутанной весовой матрицы в файл
        self.write_matrix_to_file(self.shuffled_matrix, self.weighted, self.shuffled_matrix_file_name)

    def generate(self) -> None:
        """Генерация задания."""
        self.__generate()

    def solve(self) -> set[int | str]:
        """Решение задания."""
        edges = self.make_edges_list(self.edges)
        adjacency_matrix = self.make_adjacency_matrix(edges)
        vertices_count = len(self.shuffled_matrix)
        result = set()
        for permutation in permutations(list(range(vertices_count))):
            mismatches = []
            for row in range(vertices_count):
                for col in range(row + 1, vertices_count):
                    has_edge1 = self.shuffled_matrix[row][col] < float('inf')
                    has_edge2 = adjacency_matrix[permutation[row]][permutation[col]] == 1
                    if has_edge1 != has_edge2:
                        mismatches.append((row, col, self.shuffled_matrix[row][col]))
            if not mismatches or self.bad_edge_present and len(mismatches) == 2:
                ordered_matrix = self.make_ordered_matrix(self.shuffled_matrix, list(permutation))
                missing_weight = 0
                for row, col, weight in mismatches:
                    if weight < float('inf'):
                        missing_weight = weight
                        ordered_matrix[permutation[row]][permutation[col]] = float('inf')
                for row, col, weight in mismatches:
                    if weight == float('inf'):
                        ordered_matrix[permutation[row]][permutation[col]] = missing_weight
                if self.solve_for_weights_sum:
                    weights_sum = 0
                    for edge in self.solve_for_weights_sum:
                        assert len(edge) == 2 and edge[0] in self.alphabet and edge[1] in self.alphabet
                        row = self.alphabet.index(edge[0])
                        col = self.alphabet.index(edge[1])
                        assert row != col and ordered_matrix[row][col] < float('inf')
                        weights_sum += ordered_matrix[row][col]
                    if self.constraints_satisfied(ordered_matrix, self.constraints):
                        result.add(weights_sum)
                if self.solve_for_vertices:
                    temp_result = []
                    for vertex in self.solve_for_vertices:
                        index = self.alphabet.index(vertex)
                        temp_result.append(permutation.index(index))
                    if self.constraints_satisfied(ordered_matrix, self.constraints):
                        result.add(''.join(sorted([str(index + 1) for index in temp_result])))
                if self.solve_for_shortest_distance:
                    shortest_distances = self.make_shortest_distances_matrix(ordered_matrix)
                    edge = self.solve_for_shortest_distance
                    assert len(edge) == 2 and edge[0] in self.alphabet and edge[1] in self.alphabet
                    row = self.alphabet.index(edge[0])
                    col = self.alphabet.index(edge[1])
                    if self.constraints_satisfied(ordered_matrix, self.constraints):
                        result.add(shortest_distances[row][col])
        return result

    @staticmethod
    def make_edges_list(edges: str):
        result = edges.split()
        alphabet = TaskGraphsMatchTable.alphabet
        for edge in result:
            assert len(edge) == 2 and edge[0] in alphabet and edge[1] in alphabet
        return result

    @staticmethod
    def make_matrix_text(matrix: list[list[int | float]], show_numbers: bool, weighted: bool) -> str:
        result = ' ' * 4
        for col in range(len(matrix)):
            result += f'{f"П{col + 1}": >4}' if show_numbers else f'{chr(col): >4}'
        result += '\n'
        for col in range(len(matrix)):
            result += f'{f"П{col + 1}": >4}' if show_numbers else f'{chr(col): >4}'
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

    @staticmethod
    def make_adjacency_matrix(edges: list[str]) -> list[list[int]]:
        """Создание матрицы смежности по списку рёбер."""
        vertices_count = 0
        alphabet = TaskGraphsMatchTable.alphabet
        for edge in edges:
            vertices_count = max(vertices_count, alphabet.index(edge[0]) + 1)
            vertices_count = max(vertices_count, alphabet.index(edge[1]) + 1)
        result = [[0] * vertices_count for _ in range(vertices_count)]
        for edge in edges:
            row = alphabet.index(edge[0])
            col = alphabet.index(edge[1])
            assert row != col and result[row][col] != 1
            result[row][col] = 1
            result[col][row] = 1
        return result

    @staticmethod
    def make_ordered_matrix(matrix: list[list[int | float]], pointers: list[int]) -> list[list[int | float]]:
        """Обратная перестановка вершин в матрице."""
        result: list[list[int | float]] = [[0] * len(matrix) for _ in range(len(matrix))]
        for row in range(len(matrix)):
            for col in range(len(matrix)):
                result[pointers[row]][pointers[col]] = matrix[row][col]
        return result

    @staticmethod
    def make_shortest_distances_matrix(matrix: list[list[int | float]]) -> list[list[int | float]]:
        """Создание матрицы кратчайших расстояний по весовой матрице."""
        result = [[float('inf')] * len(matrix) for _ in range(len(matrix))]
        for row in range(len(matrix)):
            for col in range(len(matrix)):
                result[row][col] = matrix[row][col]
            result[row][row] = 0
        for k in range(len(matrix)):
            for i in range(len(matrix)):
                for j in range(len(matrix)):
                    result[i][j] = min(result[i][j], result[i][k] + result[k][j])
        return result

    @staticmethod
    def constraints_satisfied(matrix: list[list[int | float]], constraints: Tuple[str]) -> bool:
        """Проверка выполнения ограничений на веса рёбер."""
        for constraint in constraints:
            edge1, sign, edge2 = constraint.split()
            row1 = TaskGraphsMatchTable.alphabet.index(edge1[0])
            col1 = TaskGraphsMatchTable.alphabet.index(edge1[1])
            row2 = TaskGraphsMatchTable.alphabet.index(edge2[0])
            col2 = TaskGraphsMatchTable.alphabet.index(edge2[1])
            if sign == '<' and matrix[row1][col1] >= matrix[row2][col2]:
                return False
            elif sign == '>' and matrix[row1][col1] <= matrix[row2][col2]:
                return False
            elif sign == '=' and matrix[row1][col1] != matrix[row2][col2]:
                return False
            elif sign == '!=' and matrix[row1][col1] == matrix[row2][col2]:
                return False
            elif sign == '<=' and matrix[row1][col1] > matrix[row2][col2]:
                return False
            elif sign == '>=' and matrix[row1][col1] < matrix[row2][col2]:
                return False
        return True

    def __repr__(self) -> str:
        """Представление задания."""
        result = f'Неориентированный граф задан рёбрами: {self.edges}\n'
        if self.weighted:
            result += 'Перепутанная весовая матрица:\n'
        else:
            result += 'Перепутанная матрица смежности:\n'
        result += self.make_matrix_text(self.shuffled_matrix, show_numbers=True, weighted=self.weighted)
        if self.bad_edge_present:
            result += 'Одно ребро в таблице указано неверно.\n'
        if self.solve_for_weights_sum:
            result += 'Найти ребро или сумму рёбер: '
            result += f'{", ".join([edge for edge in self.solve_for_weights_sum])}\n'
        if self.solve_for_vertices:
            result += 'Найти номера вершин, по возрастанию: '
            result += f'{", ".join([edge for edge in self.solve_for_vertices])}\n'
        if self.solve_for_shortest_distance:
            result += f'Найти кратчайшее расстояние между вершинами: {self.solve_for_shortest_distance}\n'
        result += f'Матрица также сохранена в файле {self.shuffled_matrix_file_name}\n'
        return result

    def draw_graph(self):
        """Визуализация графа."""
        graph = networkx.Graph()
        edges_list = self.edges.split()
        graph.add_edges_from(edges_list)
        networkx.draw_networkx(graph)
        matplotlib.pyplot.show()

    def generate_edges(self, vertices_count: int, additional_edges_count: int):
        """Генерация связного неориентированного невзвешенного графа."""
        vertices = list(range(vertices_count))
        shuffle(vertices)
        edges = set()
        for index in range(1, vertices_count):
            new_edge = None
            while new_edge is None or new_edge in edges:
                prev_index = randint(0, index - 1)
                new_edge = self.alphabet[index] + self.alphabet[prev_index]
            edges.add(new_edge)
        for _ in range(additional_edges_count):
            new_edge = None
            while new_edge is None or new_edge in edges or new_edge[::-1] in edges or new_edge[0] == new_edge[1]:
                index1 = randint(0, vertices_count - 1)
                index2 = randint(0, vertices_count - 1)
                new_edge = self.alphabet[index1] + self.alphabet[index2]
            edges.add(new_edge)
        self.edges = ' '.join(edge for edge in edges)

    def graph_signature(self):
        """Сигнатура неориентированного графа (учитывает изоморфизм)."""
        edges_list = self.edges.split()
        vertices_count = 0
        alphabet = TaskGraphsMatchTable.alphabet
        for edge in edges_list:
            vertices_count = max(vertices_count, alphabet.index(edge[0]) + 1)
            vertices_count = max(vertices_count, alphabet.index(edge[1]) + 1)
        alphabet = alphabet[:vertices_count]
        signature = ' '.join(edges_list)
        for p in permutations(alphabet):
            new_edges_list = []
            for vertex in edges_list:
                x = p[alphabet.index(vertex[0])]
                y = p[alphabet.index(vertex[1])]
                new_edges_list.append(x + y if x < y else y + x)
            signature = min(signature, ' '.join(sorted(new_edges_list)))
        return signature
