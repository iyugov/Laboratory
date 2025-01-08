"""Применение заданий: кодирование текстовой, графической и звуковой информации, передача информации."""

from image import TaskImagesBatchFindHeader

task = TaskImagesBatchFindHeader(True)

print(task)
print(task.solve())
# print(task.solution())