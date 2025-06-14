"""Задания: процессы."""

import csv
from typing import List, Tuple
from random import randint, shuffle

from task import Task

class TaskProcessesLongestSimultaneousWithEarliestCompletion(Task):
    """Задание: даны процессы и их взаимозависимости.
    Определить максимальную продолжительность максимального промежутка времени,
    в течение которого возможно выполнение максимального количества процессов,
    при условии как можно более раннего завершения выполнения каждого процесса,
    и количество выполняющихся процессов на каждой единице времени."""

    processes_count_min: int = 20
    """Минимальное число процессов."""

    processes_count_max: int = 25
    """Максимальное число процессов."""

    dependencies_overall_count_min: int = 20
    """Минимальное общее число зависимостей."""

    dependencies_overall_count_max: int = 30
    """Максимальное общее число зависимостей."""

    dependencies_individual_count_max: int = 3
    """Максимальное число зависимостей одного процесса."""

    independent_processes_count_min: int = 1
    """Минимальное число независимых процессов."""

    independent_processes_count_max: int = 6
    """Максимальное число независимых процессов."""

    process_execution_time_min: int = 1
    """Минимальное время выполнения процесса."""

    process_execution_time_max: int = 20
    """Максимальное время выполнения процесса."""

    solution_min: int = 3
    """Минимальное значение ответа."""

    solution_max: int = 20
    """Максимальное значение ответа."""

    solution_processes_count_min: int = 4
    """Минимальное значение количества процессов для ответа."""

    solution_processes_count_max: int = 12
    """Максимальное значение количества процессов для ответа."""

    processes: List[Tuple[int, List[int]]]
    """Данные о процессах."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__()
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        processes_count = randint(self.processes_count_min, self.processes_count_max)
        self.processes = []
        for process_index in range(processes_count):
            process_execution_time = randint(self.process_execution_time_min, self.process_execution_time_max)
            dependencies_count_max = min(process_index, self.dependencies_individual_count_max)
            dependencies_count = randint(0, dependencies_count_max)
            potential_dependencies = list(range(0, process_index))
            shuffle(potential_dependencies)
            self.processes.append((process_execution_time, potential_dependencies[:dependencies_count]))

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        def conditions_ok():
            """Проверка соответствия процессов ограничениям."""
            independent_processes_count = 0
            dependencies_overall_count = 0
            for process in self.processes:
                dependencies_overall_count += len(process[1])
                if not process[1]:
                    independent_processes_count += 1
            if not all([independent_processes_count >= self.independent_processes_count_min,
                        independent_processes_count <= self.independent_processes_count_max,
                        dependencies_overall_count >= self.dependencies_overall_count_min,
                        dependencies_overall_count <= self.dependencies_overall_count_max]):
                return False
            return True
        def non_trivial_solution_ok():
            """Проверка того, чтобы ответ не был равен времени выполнения никакого одного процесса,
            чтобы искомый промежуток был не в самом начале выполнения процессов,
            и соответствия условия ограничениям."""
            solution = self.solve(get_load=True)
            if not self.solution_min <= solution[0] <= self.solution_max:
                return False
            max_load = max(solution[1])
            if not self.solution_processes_count_min <= max_load <= self.solution_processes_count_max:
                return False
            if any(process[0] == solution[0] for process in self.processes):
                return False
            return not all([load == max_load for load in solution[1][:solution[0]]])
        generation_ok = False
        while not generation_ok:
            self.__generate_raw()
            if not conditions_ok():
                continue
            if not non_trivial_solution_ok():
                continue
            generation_ok = True

    def generate(self) -> None:
        """Генерирует параметры условия."""
        self.__generate()

    def solve(self, get_load=False) -> Tuple[int, List[int]] | int:
        """Решение задания."""
        def make_execution_periods(starting_process_index: int | Tuple[int, List[int]]) -> None:
            """Создание периодов наиболее раннего исполнения процессов с учётом зависимостей."""
            if execution_periods[starting_process_index] is not None:
                return
            if not self.processes[starting_process_index][1]:
                execution_periods[starting_process_index] = (0, self.processes[starting_process_index][0])
                return
            max_time_before_start = 0
            for dependent_process in self.processes[starting_process_index][1]:
                make_execution_periods(dependent_process)
                max_time_before_start = max(max_time_before_start, execution_periods[dependent_process][1])
            execution_periods[starting_process_index] = (max_time_before_start, max_time_before_start + self.processes[starting_process_index][0])
        def get_load_by_seconds():
            """Получение загрузки по секундам."""
            load = [0] * max(execution_periods, key=lambda x: x[1])[1]
            for execution_period in execution_periods:
                for load_second in range(*execution_period):
                    load[load_second] += 1
            return load
        def time_chart() -> str:
            """Создание таблицы загрузки процессов по времени.
            Вызывается для отладки."""
            time_span = max(execution_periods, key=lambda x: x[1])[1]
            load = get_load_by_seconds()
            result = ' ' * 5
            for second in load:
                result += str((second + 1) % 10)
            result += '\n'
            result += ' ' * 5
            for second in range(time_span):
                result += str((second + 1) % 10)
            result += '\n'
            for process_number, execution_period in enumerate(execution_periods, 1):
                result += f'{process_number:4} '
                for second in range(time_span):
                    result += '*' if execution_period[0] <= second < execution_period[1] else ' '
                result += '\n'
            return result
        execution_periods: List[None | Tuple[int, int]] = [None] * len(self.processes)
        for process_index in range(len(self.processes)):
            make_execution_periods(process_index)
        load_by_seconds = get_load_by_seconds()
        max_load = max(load_by_seconds)
        max_series_length = 0
        current_series_length = 0
        for load in load_by_seconds:
            if load == max_load:
                current_series_length += 1
                max_series_length = max(max_series_length, current_series_length)
            else:
                current_series_length = 0
        if get_load:
            return max_series_length, load_by_seconds
        return max_series_length

    def __repr__(self) -> str:
        """Представление задания."""
        result = ''
        for process_index in range(len(self.processes)):
            process_line = f'{process_index + 1}'
            process_line += f'\t{self.processes[process_index][0]}'
            if self.processes[process_index][1]:
                dependencies_line = '; '.join(str(dependency + 1) for dependency in self.processes[process_index][1])
            else:
                dependencies_line = '0'
            process_line += f'\t{dependencies_line}'
            result += f'{process_line}\n'
        return result

    def save_to_csv_file(self, file_name: str) -> None:
        """Сохранение данных о графе в файле CSV."""
        with open(file_name, 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            for process_index, process_data in enumerate(self.processes, 1):
                dependencies = '; '.join(str(dependency + 1) for dependency in process_data[1])
                if dependencies == '':
                    dependencies = '0'
                csv_writer.writerow((process_index, process_data[0], dependencies))

