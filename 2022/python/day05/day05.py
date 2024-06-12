from enum import Enum

import numpy


class Method(str, Enum):
    ONE_BY_ONE = "one by one"
    ALL = "all"


def move_crates(
    moves: list[str], stacks: list[list[int]], method: Method
) -> str:
    for move in moves:
        amount = int(move.split(' ')[1])
        from_stack = int(move.split(' ')[3]) - 1
        to_stack = int(move.split(' ')[5]) - 1
        crates = stacks[from_stack][0:amount]
        stacks[from_stack] = stacks[from_stack][amount:]
        if method == Method.ONE_BY_ONE:
            stacks[to_stack] = list(reversed(crates)) + stacks[to_stack]
        if method == Method.ALL:
            stacks[to_stack] = crates + stacks[to_stack]
    return ''.join([stack[0] for stack in stacks])


with open('day05/input', encoding='utf-8') as f:
    lines = [line for line in f]

stacks = [
    [crate for crate in stack if crate != ' ']
    for stack in numpy.array([
        [pl[(i*4)+1] for i in range(0, 9)]
        for pl in lines[:8]
    ]).T.tolist()
]
moves = lines[10:]

print(f'Part 1: {move_crates(moves, stacks.copy(), Method.ONE_BY_ONE)}')
print(f'Part 2: {move_crates(moves, stacks.copy(), Method.ALL)}')
