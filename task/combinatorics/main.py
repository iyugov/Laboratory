"""Применение заданий: комбинаторика."""

from lexicographic import TaskCombinatoricsLexOrderFindNumberOfWordByCondition

task = TaskCombinatoricsLexOrderFindNumberOfWordByCondition(False)

task.alphabet = 'РАМЕШКИ'
task.word_length = 5
task.word_condition = lambda word: word[0] not in 'ШР' and word.count('МА') >= 1
task.number_condition = lambda number: number % 2 == 0

print(task)
print(task.solve())