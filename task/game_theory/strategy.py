"""Задания: выигрышная стратегия."""

from typing import Tuple, List

from task import Task

class TaskGameTheoryStrategyStoneHeaps(Task):
    """Задание: даны правила игры с кучами камней.
    Определить, в каких игровых ситуациях игроки имеют выигрышные стратегии в определённое число ходов."""

    player_names: Tuple[str, str] = ('Петя', 'Вася')
    """Имена игроков."""

    starting_position: Tuple[int | None, ...] = (7, None)
    """Стартовая позиция (задаёт количество куч и неизвестное значение)."""

    solution_interval: Tuple[int, ...] = (1, 92)
    """Интервал для поиска решений."""

    moves_count_range: Tuple[int, ...] = (1, 20)
    """Интервал количества ходов (в полуходах)."""

    def next_positions(self, position: Tuple[int, ...]) -> Tuple[Tuple[int, ...], ...]:
        """Получение позиций после возможных ходов."""
        a, b = position
        return (a + 1, b), (a * 2, b), (a, b + 1), (a, b * 2)

    def is_won(self, position: Tuple[int | None, ...]) -> bool:
        """Критерий признания игры выигранной."""
        return sum(position) >= 100

    def is_lost(self, position: Tuple[int | None, ...]) -> bool:
        return False
    """Критерий признания игры проигранной (приоритет над признанием выигранной)."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        self.__generate_raw()

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> str:
        """Решение задания."""

        def intervals(values_list: List[int]) -> str:
            """Возвращает отсортированный список чисел в виде строки, объединяя подряд идущие числа в интервал"""
            if not values_list:
                return ''
            intervals_list = [values_list[0]]
            for v in values_list[1:]:
                last_item = intervals_list[-1]
                if isinstance(last_item, int) and (last_item + 1 == v):
                    intervals_list[-1] = (last_item, v)
                elif isinstance(last_item, tuple) and (last_item[1] + 1 == v):
                    intervals_list[-1] = (last_item[0], v)
                else:
                    intervals_list.append(v)
            return ', '.join([str(x) if isinstance(x, int) else f'{x[0]}-{x[1]}' for x in intervals_list])

        def get_starting_position_by_value(position_value: int) -> tuple[int | None, ...]:
            """Получение начальной позиции по заданному значению."""
            return tuple((position_value if value is None else value) for value in self.starting_position)

        def solve_for_position(position: Tuple[int, ...]) -> Tuple[int, ...]:
            """Решение задания относительно заданного значения в позиции."""
            if self.is_lost(position):
                return 1, 0
            if self.is_won(position):
                return -1, 0
            if position in position_cache:
                return position_cache[position]
            side = -1
            status_min, status_max = float('inf'), float('-inf')
            for next_position in self.next_positions(position):
                position_result = solve_for_position(next_position)
                if position_result[0] == -1:
                    status_min = min(status_min, position_result[1])
                    side = 1
                else:
                    status_max = max(status_max, position_result[1])
            move = (status_min if side == 1 else status_max) + 1
            position_cache[position] = (side, move)
            return position_cache[position]

        solution_range = range(self.solution_interval[0], self.solution_interval[1] + 1)
        position_cache = {}
        for starting_position_value in solution_range:
            starting_position = get_starting_position_by_value(starting_position_value)
            solve_for_position(starting_position)

        starting_position_common = f'({', '.join('S' if n is None else str(n) for n in self.starting_position)})'
        moves_count_range = range(self.moves_count_range[0], self.moves_count_range[1] + 1)
        solution_range = range(self.solution_interval[0], self.solution_interval[1] + 1)
        result = ''
        for moves_count in moves_count_range:
            for side in 1, -1:
                values_list = []
                for starting_position_value in solution_range:
                    starting_position = get_starting_position_by_value(starting_position_value)
                    if starting_position in position_cache and position_cache[starting_position] == (side, moves_count):
                        values_list.append(starting_position_value)
                values_list.sort()
                if values_list:
                    player_name = self.player_names[0] if side == 1 else self.player_names[1]
                    player_move_count = (moves_count + 1) // 2
                    values = intervals(values_list)
                    result += f'{player_name} выигрывает своим {player_move_count}-м ходом '
                    result += f'в позиции {starting_position_common} при значениях S: {values}\n'
        return result

    def __repr__(self) -> str:
        """Представление задания."""
        result = ''
        result += f'Два игрока, {self.player_names[0]} и {self.player_names[1]}, играют в игру.\n'
        starting_position = f'({', '.join('S' if n is None else str(n) for n in self.starting_position)})'
        result += f'Начальная позиция: {starting_position}.'

        return result