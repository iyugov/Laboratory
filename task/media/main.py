"""Применение заданий: кодирование текстовой, графической и звуковой информации, передача информации."""

from sound import TaskSoundAlbumFindTransmissionTime

task = TaskSoundAlbumFindTransmissionTime(True)

print(task)
print(task.solve())
print(task.solution())