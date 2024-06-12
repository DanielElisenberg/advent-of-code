from itertools import groupby


def parse_carried_calories(lines: list[str]) -> list[int]:
    return [
        sum(int(item) for item in group)
        for filter, group in groupby(lines, lambda line: line != '')
        if filter
    ]


with open('day01/input', encoding='utf-8') as f:
    lines = [line.strip() for line in f]

calories_carried = parse_carried_calories(lines)
calories_carried.sort()
print(f'Part 1: {calories_carried[-1]}')
print(f'Part 2: {sum(calories_carried[-3:])}')
