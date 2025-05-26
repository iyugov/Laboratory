"""Применение заданий: кодирование текстовой, графической и звуковой информации, передача информации."""

from image import TaskImagesConversionBatchFindSavedSpace

for _ in range(30):
    task = TaskImagesConversionBatchFindSavedSpace(True)
    print(task)
    print(task.solve())
    print('===')