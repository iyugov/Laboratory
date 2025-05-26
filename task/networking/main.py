"""Применение заданий: десятичные исполнители."""

from ip import TaskIPSubnetFindSubnetIfIPIsNotSpecial, ip_to_str

def bin_ip(ip: int) -> str:
    """Преобразование IP-адреса из десятичного вида в двоичный."""
    return '.'.join([bin(int(octet))[2:].zfill(8) for octet in ip_to_str(ip).split('.')])

for _ in range(50):
    task = TaskIPSubnetFindSubnetIfIPIsNotSpecial(True)
    print(task)
    print(bin_ip(task.ip_address))
    print(task.solve())
    print()
    print()


