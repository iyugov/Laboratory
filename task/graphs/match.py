"""Задания: соотнесение таблицы и графа."""

from random import randint, shuffle
from csv import writer
from itertools import permutations

from task import Task


class TaskGraphsMatchTable(Task):
    """Задание: неориентированный граф и таблица истинности с перепутанными строками.
    Соотнести вершины в таблице и в графе."""

    edges: str = "ab ac ad bd be cd cf de eg fg"
    # Рёбра графа в виде пар вершин, обозначенных буквами (a, b, c...), разделённые пробелами

    weighted: bool = True
    # Является ли граф взвешенным

    tries_limit: int = 1000
    # Число попыток случайной генерации весов рёбер

    shuffled_matrix: list[list[int | float]]
    # Перепутанная весовая матрица

    solve_for_weights_sum: tuple[str] = ()
    # Что нужно найти: сумма весов конкретных рёбер (в частности, вес одного ребра)

    solve_for_vertices: str = ''
    # Что нужно найти: конкретные вершины

    solve_for_shortest_distance: str = ''
    # Что нужно найти: кратчайшее расстояние между конкретными вершинами

    bad_edge_present: bool = False
    # Есть ли в таблице неправильное ребро

    shuffled_matrix_file_name: str = 'graph.csv'
    # Имя файла для сохранения перепутанной весовой матрицы

    solution_count: int = 1
    # Требуемое число решений

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__()
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без проверки."""

        def make_weights_matrix(matrix: list[list[int]]) -> list[list[int | float]]:
            """Создание весовой матрицы по матрице смежности."""

            def generate_weights(weights_count: int, unique_pair_sums: bool = False):
                """Генерация весов рёбер так, чтобы и они сами, и их попарные суммы были уникальными."""
                weight_limit = 1
                success = False
                generated_weights = []
                while not success:
                    tries_count = 0
                    while not success and tries_count < self.tries_limit:
                        tries_count += 1
                        generated_weights = [randint(1, weight_limit) for _ in range(weights_count)]
                        success = len(generated_weights) == len(set(generated_weights))
                        if success and unique_pair_sums:
                            pair_sums = []
                            for index1 in range(len(generated_weights)):
                                for index2 in range(index1 + 1, len(generated_weights)):
                                    pair_sums.append(generated_weights[index1] + generated_weights[index2])
                            max_pair_count = len(generated_weights) * (len(generated_weights) - 1) // 2
                            success = success and len(set(pair_sums)) == max_pair_count
                    if not success:
                        weight_limit += 1
                return generated_weights

            edges_count = 0
            for row in range(len(matrix)):
                for col in range(row + 1, len(matrix)):
                    if adjacency_matrix[row][col] == 1:
                        edges_count += 1
            if self.weighted:
                weights = generate_weights(edges_count, unique_pair_sums=len(self.solve_for_weights_sum) > 1)
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
            solution_ok = len(solution) == self.solution_count
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
                        edge = edge.upper()
                        assert len(edge) == 2 and edge.isalpha()
                        row = ord(edge[0]) - ord('A')
                        col = ord(edge[1]) - ord('A')
                        assert row != col and ordered_matrix[row][col] < float('inf')
                        weights_sum += ordered_matrix[row][col]
                    result.add(weights_sum)
                if self.solve_for_vertices:
                    temp_result = []
                    for vertex in self.solve_for_vertices.upper():
                        index = ord(vertex) - ord('A')
                        temp_result.append(permutation.index(index))
                    result.add(''.join(sorted([str(index + 1) for index in temp_result])))
                if self.solve_for_shortest_distance:
                    shortest_distances = self.make_shortest_distances_matrix(ordered_matrix)
                    edge = self.solve_for_shortest_distance.upper()
                    assert len(edge) == 2 and edge.isalpha()
                    row = ord(edge[0]) - ord('A')
                    col = ord(edge[1]) - ord('A')
                    result.add(shortest_distances[row][col])
        return result

    @staticmethod
    def make_edges_list(edges: str):
        result = edges.upper().split()
        for edge in result:
            assert len(edge) == 2 and edge.isalpha()
        return result

    @staticmethod
    def make_matrix_text(matrix: list[list[int | float]], show_numbers: bool, weighted: bool) -> str:
        result = ' ' * 4
        for col in range(len(matrix)):
            result += f'{f"П{col + 1}": >4}' if show_numbers else f'{chr(ord("A") + col): >4}'
        result += '\n'
        for col in range(len(matrix)):
            result += f'{f"П{col + 1}": >4}' if show_numbers else f'{chr(ord("A") + col): >4}'
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
        for edge in edges:
            vertices_count = max(vertices_count, ord(edge[0]) - ord('A') + 1, ord(edge[1]) - ord('A') + 1)
        result = [[0] * vertices_count for _ in range(vertices_count)]
        for edge in edges:
            row = ord(edge[0]) - ord('A')
            col = ord(edge[1]) - ord('A')
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

    def __repr__(self) -> str:
        """Представление задания."""
        result = f'Неориентированный граф задан рёбрами: {self.edges.upper()}\n'
        if self.weighted:
            result += 'Перепутанная весовая матрица:\n'
        else:
            result += 'Перепутанная матрица смежности:\n'
        result += self.make_matrix_text(self.shuffled_matrix, show_numbers=True, weighted=self.weighted)
        if self.bad_edge_present:
            result += 'Одно ребро в таблице указано неверно.\n'
        if self.solve_for_weights_sum:
            result += 'Найти ребро или сумму рёбер: '
            result += f'{", ".join([edge.upper() for edge in self.solve_for_weights_sum])}\n'
        if self.solve_for_vertices:
            result += 'Найти номера вершин, по возрастанию: '
            result += f'{", ".join([edge.upper() for edge in self.solve_for_vertices])}\n'
        if self.solve_for_shortest_distance:
            result += f'Найти кратчайшее расстояние между вершинами: {self.solve_for_shortest_distance.upper()}\n'
        result += f'Матрица также сохранена в файле {self.shuffled_matrix_file_name}\n'
        return result
