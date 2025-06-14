"""Применение заданий: графы."""

from processes import TaskProcessesLongestSimultaneousWithEarliestCompletion

task = TaskProcessesLongestSimultaneousWithEarliestCompletion(True)

print(task)
solution = task.solve(get_load=True)
print(solution[0], max(solution[1]))
times = list(enumerate(solution[1], 1))
for time in times:
    print(f'{time[0]:3}', end=' ')
print()
for time in times:
    print(f'{time[1]:3}', end=' ')