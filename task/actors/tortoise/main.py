"""Применение заданий: исполнитель Черепаха."""

from tortoise import TaskActorsTortoiseTwoActorsTypeA

task = TaskActorsTortoiseTwoActorsTypeA(True)
solution = task.solve()
print(task)
for key, value in solution.items():
    print(key)
    for key2, value2 in value.items():
        print('\t', key2, value2)