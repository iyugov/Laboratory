"""Применение заданий: десятичные исполнители."""

from ip import TaskIPSubnetFindSubnetsByBinaryOnesDivision, ip_to_str

def bin_ip(ip: int) -> str:
    """Преобразование IP-адреса из десятичного вида в двоичный."""
    return '.'.join([bin(int(octet))[2:].zfill(8) for octet in ip_to_str(ip).split('.')])

for _ in range(1):
    task = TaskIPSubnetFindSubnetsByBinaryOnesDivision(True)
    print(task)
    print(bin_ip(task.ip_address))
    solution = task.solve()
    print(solution)
    print(len(solution))
    print()


