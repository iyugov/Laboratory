"""Применение заданий: кодирование текстовой, графической и звуковой информации, передача информации."""

from image import TaskImagesBatchInStorages

for _ in range(10):
    task = TaskImagesBatchInStorages(True)
    print(task)
    print(task.solve())
    print()