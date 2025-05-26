"""Применение заданий: комбинаторика."""

from subsequences import TaskCharSequenceTypeF


task = TaskCharSequenceTypeF(False)
task.chunks = ('ABC', 'BCA', 'CAB')
task.generate()
print(task)
print(task.solve())
task.write_to_file('0400.txt')