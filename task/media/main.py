"""Применение заданий: кодирование текстовой, графической и звуковой информации, передача информации."""

from video import TaskVideoFindTransferTime

for _ in range(30):
    task = TaskVideoFindTransferTime(True)
    print(task)
    print(task.solve())
    print('===')
    print(task.solution())