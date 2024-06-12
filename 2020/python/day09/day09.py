import itertools


def find_invalid_number(numbers):
    for i in range(25, len(numbers)):
        preamble = list(itertools.combinations(numbers[i-25:i], 2))
        preamble_combinations = [x+y for (x, y) in preamble]
        if numbers[i] not in preamble_combinations:
            return numbers[i]


def find_encryption_weakness(numbers, invalid_number):
    for i in range(len(numbers)):
        for j in range(i+2, len(numbers)):
            summed_set = sum(numbers[i:j])
            if invalid_number == summed_set:
                print(numbers[i:j])
                return min(numbers[i:j])+max(numbers[i:j])
            if invalid_number < summed_set:
                break


with open('day09/input.data') as input:
    numbers = [int(line) for line in input.read().split('\n')]

invalid_number = find_invalid_number(numbers)
print(f"first solution: {invalid_number}")
encryption_weakness = find_encryption_weakness(numbers, invalid_number)
print(f'second solution: {encryption_weakness}')
