
from composite_data import TaskInfoAmountCompositeDataTypeC

for _ in range(50):
    task = TaskInfoAmountCompositeDataTypeC(False)
    task.generate()
    print(task)
    print(task.solve())
    print()