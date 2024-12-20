"""Задания: логика, таблицы истинности."""
from itertools import product, permutations
from random import choice, shuffle, randint
from typing import Dict, Callable, List, Tuple

from task import Task

class TaskLogicTruthTableMatchColumnsAndVariables(Task):
    """Задание: дано логическое выражение и несколько частично заполненных строк его таблицы истинности.
    Определить, какому столбцу таблицы истинности соответствует каждая логическая переменная выражения."""

    variables_letters: str = 'wxyz'
    """Буквы переменных."""

    operations_count: int = 5
    """Количество операций."""

    rows_count: int = 3
    """Количество строк таблицы истинности."""

    empty_cells_count: int = 4
    """Количество пустых ячеек в таблице истинности."""

    unary_operations: Dict[str, Callable] = {'~': lambda x: not x}
    """Унарные операции."""

    binary_operations: Dict[str, Callable] = {
        '*': lambda x, y: x and y,
        '+': lambda x, y: x or y,
        '#': lambda x, y: x != y,
        '->': lambda x, y: x <= y,
        '=': lambda x, y: x == y
    }
    """Бинарные операции."""

    same_result_in_rows: bool = True
    """Одинаковый результат в строках таблицы истинности."""

    solutions_count_min: int = 1
    """Минимальное количество решений."""

    solutions_count_max: int = 1
    """Максимальное количество решений."""

    function_tree: str | Tuple = tuple()
    """Дерево функции."""

    truth_table_part: List[Dict] = []
    """Часть таблицы истинности."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__()
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        generation_ok = False
        while not generation_ok:
            # Генерация дерева функции
            self.generate_function_tree()
            # Вычисление полной таблицы истинности с перемешиванием строк и столбцов
            raw_results = []
            letters_list = list(self.variables_letters)
            shuffle(letters_list)
            for value_vector in product([0, 1], repeat=len(letters_list)):
                values = dict(zip(letters_list, value_vector))
                raw_results.append([list(value_vector), self.apply_function_tree(values)])
            # Предварительное обеспечение того, что не все значения функции в строках полной таблицы одинаковы
            raw_results_true = [value for value in raw_results if value[1]]
            raw_results_false = [value for value in raw_results if not value[1]]
            if len(raw_results_true) < self.rows_count or len(raw_results_false) < self.rows_count:
                continue
            if self.same_result_in_rows:
                # Выбор истинного или ложного значения для функции в выбранных строках
                raw_results = raw_results_true if randint(0, 1) == 1 else raw_results_false
            else:
                # Просто перемешивание строк для дальнейшего выбора
                shuffle(raw_results)
            # Получение части таблицы истинности
            self.truth_table_part = [{'variables': line[:-1][0], 'result': line[-1]} for line in raw_results[:self.rows_count]]
            # Проверка на неодинаковый результат в строках таблицы истинности
            if not self.same_result_in_rows:
                if all(row['result'] for row in self.truth_table_part) or not any(row['result'] for row in self.truth_table_part):
                    continue
            shuffle(self.truth_table_part)
            # Удаление значений из таблицы истинности
            for _ in range(self.empty_cells_count):
                first = True
                row_index, column_index = 0, 0
                while first or self.truth_table_part[row_index]['variables'][column_index] is None:
                    row_index = randint(0, self.rows_count - 1)
                    column_index = randint(0, len(letters_list) - 1)
                    first = False
                self.truth_table_part[row_index]['variables'][column_index] = None
            generation_ok = True

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        solution_ok = False
        while not solution_ok:
            self.__generate_raw()
            solutions = self.solve()
            solution_ok = self.solutions_count_min <= len(solutions) <= self.solutions_count_max

    def generate(self) -> None:
        """Генерирует параметры условия."""
        self.__generate()

    def solve(self) -> List[str]:
        """Решение задания."""
        solutions = []
        for fill_vector in product([0, 1], repeat=self.empty_cells_count):
            fill_index = 0
            temporary_table = []
            results = []
            for row_index in range(self.rows_count):
                new_row = self.truth_table_part[row_index]['variables'].copy()
                for column_index in range(len(self.variables_letters)):
                    if new_row[column_index] is None:
                        new_row[column_index] = fill_vector[fill_index]
                        fill_index += 1
                temporary_table.append(tuple(new_row))
                results.append(self.truth_table_part[row_index]['result'])
            # Проверка уникальности строк таблицы истинности
            if len(temporary_table) == len(set(temporary_table)):
                for order in permutations(self.variables_letters):
                    if [self.apply_function_tree(dict(zip(order, row))) for row in temporary_table] == results:
                        solutions.append((temporary_table, ''.join(order)))
                if len(solutions) > self.solutions_count_max:
                    return []
        return solutions if len(solutions) >= self.solutions_count_min else []

    def __repr__(self) -> str:
        """Представление задания."""
        result = 'Дано логическое выражение:\n'
        result += f'{self.function_str_representation()}\n'
        result += 'Частично заполненная таблица истинности:\n'
        for row in self.truth_table_part:
            variables_line = ''.join('-' if item is None else str(item) for item in row['variables'])
            function_value = row['result']
            result += f'{variables_line} {function_value}\n'
        result += 'Определить, какому столбцу таблицы истинности соответствует каждая логическая переменная выражения.'
        return result

    def generate_function_tree(self) -> None:
        """Генерация дерева функции."""
        tree: List[str | Tuple] = []
        while len(set(tree)) != len(self.variables_letters):
            tree = [choice(self.variables_letters) for _ in range(len(self.variables_letters))]
        while len(tree) != 1:
            item1, item2 = '', ''
            operation = choice(list(self.unary_operations.keys()) + list(self.binary_operations.keys()))
            if operation in self.unary_operations:
                item = choice(tree)
                # Проверка на унарную операцию перед унарной операцией
                if isinstance(item, tuple) and item[0] in self.unary_operations:
                    continue
                tree.remove(item)
                tree.append((operation, item))
            elif operation in self.binary_operations:
                while item1 == item2:
                    item1, item2 = choice(tree), choice(tree)
                tree.remove(item1)
                tree.remove(item2)
                tree.append((operation, item1, item2))
        self.function_tree = tree[0]

    def function_str_representation(self) -> str:
        """Представление дерева функции в виде строки."""
        return self.function_str_representation_recursive(self.function_tree)

    def function_str_representation_recursive(self, function_tree: List | str) -> str:
        """Представление дерева функции в виде строки (рекурсивно)."""
        if isinstance(function_tree, str):
            return function_tree
        if function_tree[0] in self.unary_operations:
            result = self.function_str_representation_recursive(function_tree[1])
            return f'{function_tree[0]} {result}'
        elif function_tree[0] in self.binary_operations:
            result1 = self.function_str_representation_recursive(function_tree[1])
            result2 = self.function_str_representation_recursive(function_tree[2])
            return f'({result1} {function_tree[0]} {result2})'
        else:
            return function_tree[0] # операция не из списка унарных или бинарных

    def apply_function_tree(self, values: Dict[str, int]) -> int:
        """Применение дерева функции к набору значений переменных."""
        return self.apply_function_tree_recursive(self.function_tree, values)

    def apply_function_tree_recursive(self, function_tree: List | str, values: Dict[str, int]) -> int:
        """Применение дерева функции к набору значений переменных (рекурсивно)."""
        if isinstance(function_tree, str):
            return values[function_tree]
        if function_tree[0] in self.unary_operations:
            result = self.apply_function_tree_recursive(function_tree[1], values)
            return int(self.unary_operations[function_tree[0]](result))
        elif function_tree[0] in self.binary_operations:
            result1 = self.apply_function_tree_recursive(function_tree[1], values)
            result2 = self.apply_function_tree_recursive(function_tree[2], values)
            return int(self.binary_operations[function_tree[0]](result1, result2))
        else:
            return int(values[function_tree[0]]) # операция не из списка унарных или бинарных

