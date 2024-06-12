
import math
from copy import deepcopy


def parse_monkey_string(monkey_lines: str) -> dict:
    monkey_line = monkey_lines.split('\n')
    return {
        'items': list(
            int(item) for item in monkey_line[1][17:].split(', ')
        ),
        'operation': compile(
            monkey_line[2][19:].replace('old', 'item'), '<string>', 'eval'
        ),
        'test': int(monkey_line[3].split(' ')[-1]),
        'true_monkey': int(monkey_line[4].split(' ')[-1]),
        'false_monkey': int(monkey_line[5].split(' ')[-1]),
        'items_inspected': 0
    }


def play_rounds(monkeys: list[dict], rounds: int = 20, part: int = 1) -> int:
    lowest_common = math.lcm(*[monkey['test'] for monkey in monkeys])
    for _ in range(rounds):
        for monkey in monkeys:
            monkey['items_inspected'] += len(monkey['items'])
            for item in monkey['items']:
                worry_level = (
                    (eval(monkey['operation']) // 3) if part == 1
                    else (eval(monkey['operation']) % lowest_common)
                )
                next_monkey = (
                    monkeys[monkey['true_monkey']]
                    if worry_level % monkey['test'] == 0
                    else monkeys[monkey['false_monkey']]
                )
                next_monkey['items'].append(worry_level)
            monkey['items'] = []
    monkey_business = sorted([monkey['items_inspected'] for monkey in monkeys])
    return monkey_business[-1] * monkey_business[-2]


with open('day11/input', encoding='utf-8') as f:
    monkeys = [
        parse_monkey_string(string)
        for string in f.read().strip().split('\n\n')
    ]

print(f'Part 1: {play_rounds(deepcopy(monkeys))}')
print(f'Part 2: {play_rounds(monkeys, rounds=10_000, part=2)}')
