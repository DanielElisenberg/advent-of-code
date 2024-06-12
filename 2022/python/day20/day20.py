from collections import deque


def mix(encrypted_file: deque[int]):
    for index in range(len(encrypted_file)):
        while encrypted_file[-1][0] != index:
            encrypted_file.rotate(1)
        _, popped = encrypted_file.pop()
        encrypted_file.rotate(popped)
        encrypted_file.append((index, popped))


def grove_coordinates(encrypted_file: deque[int]):
    while encrypted_file[-1][1] != 0:
        encrypted_file.rotate(1)
    grove_coordinates_sum = 0
    for _ in range(3):
        encrypted_file.rotate(1000)
        grove_coordinates_sum += encrypted_file[-1][1]
    return grove_coordinates_sum


with open('day20/input', encoding='utf-8') as f:
    file_numbers = [int(line.strip()) for line in f]

encrypted_file = deque(reversed([
    (index, number)
    for index, number in enumerate(file_numbers)
]))
mix(encrypted_file)
print(f'Part 1: {grove_coordinates(encrypted_file)}')

decryption_key = 811589153
encrypted_file = deque(reversed([
    (index, number*decryption_key)
    for index, number in enumerate(file_numbers)
]))
for _ in range(10):
    mix(encrypted_file)
print(f'Part 2: {grove_coordinates(encrypted_file)}')
