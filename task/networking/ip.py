"""Адресация в сети: IP-адреса."""

from task import Task
from general import quantity_form


def ip_to_str(ip: int) -> str:
    """Преобразование IP-адреса в строку."""
    return '.'.join([str((ip >> shift) & 0xFF) for shift in [24, 16, 8, 0]])

def subnet_mask_to_ip(mask: int) -> int:
    return 2**32 - 2**(32 - mask)

class TaskIPSubnetFindNumberOfAddressesWithoutKSameDigitsInARowInLastByte(Task):
    """Дан хост и маска подсети.
    Определить количество адресов в этой сети, в двоичном представлении последнего байта которых
    не более K одинаковых заданных цифр подряд."""

    ip_address: int = 0
    """IP-адрес хоста."""

    subnet_mask_min: int = 16
    """Минимальная маска подсети."""

    subnet_mask_max: int = 26
    """Максимальная маска подсети."""

    subnet_mask: int = 0
    """Маска подсети."""

    number_of_digits_not_in_a_row: int = 3
    """Недопустимое количество цифр подряд."""

    digit_not_in_a_row: int = 0
    """Цифра, которая не должна встречаться в последнем байте адреса определённое число раз подряд."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import randint
        self.subnet_mask = randint(self.subnet_mask_min, self.subnet_mask_max)
        ip_ok = False
        while not ip_ok:
            ip = 0
            bits_subnet, bits_host = set(), set()
            for bit_index in range(32):
                bit = randint(0, 1)
                ip = (ip << 1) | bit
                if bit_index < self.subnet_mask:
                    bits_subnet.add(bit)
                else:
                    bits_host.add(bit)
            # Проверка на то, что адрес не широковещательный, не является адресом сети и имеет ненулевой старшей байт.
            ip_ok = len(bits_subnet) == 2 and len(bits_host) == 2 and ip >= 2**24
        self.ip_address = ip

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        solution_ok = False
        while not solution_ok:
            self.__generate_raw()
            solution_ok = 0 < self.solve() < 2**(32-self.subnet_mask)

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> int:
        """Решение задания."""
        from ipaddress import ip_network
        addresses_count = 0
        for ip_address in ip_network(f'{ip_to_str(self.ip_address)}/{self.subnet_mask}', False):
            last_byte = f'{ip_address:b}'[-8:]
            if str(self.digit_not_in_a_row) * self.number_of_digits_not_in_a_row not in last_byte:
                addresses_count += 1
        return addresses_count

    def __repr__(self) -> str:
        """Представление задания."""
        subnet = ip_to_str(subnet_mask_to_ip(self.subnet_mask))
        result = f'Адрес и подсеть: {ip_to_str(self.ip_address)}/{subnet} ({self.subnet_mask}).\n'
        result += f'Определить количество адресов в подсети, в последнем байте двоичного представления которых '
        result += f'нет {self.number_of_digits_not_in_a_row} стоящих подряд цифр {self.digit_not_in_a_row}.'
        return result



class TaskIPTwoHostsSameSubnetFindMinHostsWithXBinaryOnes(Task):
    """Даны IP-адреса двух хостов в одной подсети.
    Определить наименьшее количество адресов в подсети, в которой находятся данные хосты,
    имеющих в своей двоичной записи N единиц."""

    subnet_mask_min: int = 4
    """Минимальная маска подсети."""

    subnet_mask_max: int = 28
    """Максимальная маска подсети."""

    subnet_mask: int = 0
    """Маска подсети."""

    ip1: int = 0
    """Первый IP-адрес."""

    ip2: int = 0
    """Второй IP-адрес."""

    ones_count_min: int = 4
    """Минимальное количество единиц."""

    ones_count_max: int = 24
    """Максимальное количество единиц."""

    ones_count: int = 0
    """Количество единиц."""

    addresses_count_min: int = 10
    """Минимальное количество адресов."""

    addresses_count_max: int = 1000
    """Максимальное количество адресов."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import randint
        self.subnet_mask = randint(self.subnet_mask_min, self.subnet_mask_max)
        self.ones_count = randint(self.ones_count_min, self.ones_count_max)
        ip_ok = False
        while not ip_ok:
            ip1, ip2 = 0, 0
            bits1, bits2 = set(), set()
            for bit_index in range(32):
                if bit_index < self.subnet_mask:
                    bit = randint(0, 1)
                    ip1 = (ip1 << 1) | bit
                    ip2 = (ip2 << 1) | bit
                elif bit_index == self.subnet_mask:
                    bit = randint(0, 1)
                    ip1 = (ip1 << 1) | bit
                    ip2 = (ip2 << 1) | (1 - bit)
                    bits1.add(bit)
                    bits2.add(1 - bit)
                else:
                    bit = randint(0, 1)
                    ip1 = (ip1 << 1) | bit
                    bits1.add(bit)
                    bit = randint(0, 1)
                    ip2 = (ip2 << 1) | bit
                    bits2.add(bit)
            # Проверка на то, что среди адресов нет широковещательного адреса и адреса сети.
            ip_ok = len(bits1) == 2 and len(bits2) == 2
        self.ip1, self.ip2 = ip1, ip2

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        solution_ok = False
        while not solution_ok:
            self.__generate_raw()
            solution_ok = self.addresses_count_min <= self.solve() <= self.addresses_count_max

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> int:
        """Решение задания."""
        from math import comb
        ones_in_network_part = 0
        for bit_index in range(32):
            if bit_index < self.subnet_mask:
                ones_in_network_part += (self.ip1 >> (31 - bit_index)) & 1
        if ones_in_network_part > self.ones_count:
            return 0
        return comb(32 - self.subnet_mask, self.ones_count - ones_in_network_part)

    def __repr__(self) -> str:
        """Представление задания."""
        result = f'Даны IP-адреса двух хостов в одной подсети:\n'
        result += f'IP1: {ip_to_str(self.ip1)}\n'
        result += f'IP2: {ip_to_str(self.ip2)}\n'
        result += f'Определить наименьшее количество адресов в подсети, в которой находятся данные хосты,\n'
        form = quantity_form(self.ones_count, ('единицу', 'единицы', 'единиц'))
        result += f'имеющих в своей двоичной записи {self.ones_count} {form}.'
        return result

    def solution(self) -> str:
        """Ход решения."""
        def ip_to_str_bin(ip: int) -> str:
            """Преобразование IP-адреса в строку с двоичными значениями."""
            return '.'.join([bin((ip >> shift) & 0xFF)[2:].zfill(8) for shift in [24, 16, 8, 0]])

        from math import comb
        result = 'Представим IP-адреса в двоичной системе счисления:\n'
        s1 = f'{self.ip1:032b}'
        s2 = f'{self.ip2:032b}'
        result += f'1-й IP-адрес: {ip_to_str_bin(self.ip1)} -> {s1}\n'
        result += f'2-й IP-адрес: {ip_to_str_bin(self.ip2)} -> {s2}\n'
        result += f'Просматривая биты адресов слева направо, отделим максимально совпадающую часть адресов.\n'
        result += f'Эта часть соответствует адресу сети минимального размера, в которой находятся оба хоста.\n'
        split_index = 0
        ones = 0
        while s1[split_index] == s2[split_index]:
            ones += int(s1[split_index])
            split_index += 1
        result += f'1-й IP-адрес: {s1[:split_index]} | {s1[split_index:]}\n'
        result += f'2-й IP-адрес: {s2[:split_index]} | {s2[split_index:]}\n'
        result += f'Количество двоичных единиц в адресе сети равно {ones}. '
        form = quantity_form(self.ones_count, ('единицу', 'единицы', 'единиц'))
        result += f'Всего в полном адресе должно быть {self.ones_count} {form}.\n'
        if ones > self.ones_count:
            result += f'Так как в адресе сети больше единиц, чем требуется, ни один адрес в такой сети не подходит.\n'
            result += f'Ответ: 0.\n'
            return result
        host_bits_count = 32 - split_index
        form = quantity_form(host_bits_count, ('бит', 'бита', 'бит'))
        result += f'В индивидуальной части адреса 32 - {split_index} = {host_bits_count} {form}. '
        host_ones_count = self.ones_count - ones
        form = quantity_form(host_ones_count, ('единица', 'единицы', 'единиц'))
        result += f'Среди них должно быть ровно {self.ones_count} - {ones} = {host_ones_count} {form}.\n'
        answer = comb(host_bits_count, host_ones_count)
        form = quantity_form(answer, ('адрес', 'адреса', 'адресов'))
        result += f'Количество адресов равно С({host_bits_count}, {host_ones_count}) = {answer} '
        result += f'(сюда могут быть включены адрес сети и широковещательный адрес).\n'
        result += f'Ответ: {answer}\n'
        return result


class TaskIPSubnetFindSubnetIfIPIsNotSpecial(Task):
    """Дан адрес хоста в сети (не адрес сети и не широковещательный).
    Определить максимальное число двоичных единиц в маске подсети."""

    ip_address: int = 0
    """IP-адрес хоста."""

    subnet_mask_min: int = 10
    """Минимальная маска подсети."""

    subnet_mask_max: int = 28
    """Максимальная маска подсети."""

    subnet_mask: int = 24
    """Маска подсети."""

    special_means_broadcast: bool = True
    """Специальный адрес - широковещательный (или же это адрес сети)."""

    def __init__(self, generate: bool = False):
        """Конструктор."""
        super().__init__(generate)
        if generate:
            self.generate()

    def __generate_raw(self) -> None:
        """Генерация задания без основной проверки."""
        from random import randint, choice
        self.subnet_mask = randint(self.subnet_mask_min, self.subnet_mask_max)
        self.special_means_broadcast = choice([True, False])
        ip = randint(0, 2 ** 32 - 1)
        ip &= (2 ** 32 - 2 ** (32 - self.subnet_mask))
        if self.special_means_broadcast:
            ip -= 1
        self.ip_address = ip

    def __generate(self) -> None:
        """Генерация задания с основной проверкой."""
        solution_ok = False
        while not solution_ok:
            self.__generate_raw()
            solution_ok = 0 < self.solve() < 2**(32-self.subnet_mask)

    def generate(self) -> None:
        """Генерация параметров условия."""
        self.__generate()

    def solve(self) -> int:
        """Решение задания."""
        ip = self.ip_address
        last_bit = ip % 2
        last_bits_count = 0
        while ip % 2 == last_bit:
            last_bits_count += 1
            ip >>= 1
        return 31 - last_bits_count

    def __repr__(self) -> str:
        """Представление задания."""
        special_type = 'широковещательный адрес' if self.special_means_broadcast else 'адрес сети'
        result = f'Адрес {ip_to_str(self.ip_address)} в подсети - не {special_type}.\n'
        result += f'Определить максимальное количество двоичных единиц в маске подсети.\n'
        return result