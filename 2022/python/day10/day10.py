from itertools import chain
from itertools import accumulate


with open('day10/input', encoding='utf-8') as f:
    instructions = [line.strip().split(' ') for line in f]
add_per_cycle = chain(
    *[[1]] + [
        [0] if instruction == ['noop'] else [0, int(instruction[1])]
        for instruction in instructions
    ]
)
cycles = list(accumulate(add_per_cycle, lambda x1, x2: x1+x2))

signal_strength_sum = sum([
    x*(index+1) for index, x in enumerate(cycles)
    if index+1 in [20, 60, 100, 140, 180, 220]
])
print(f'Part 1: {signal_strength_sum}')

pixels = ''.join([
    '#' if index % 40 in range(x-1, x+2) else '.'
    for index, x in enumerate(cycles)
])
display = '\n'.join(pixels[(row*40): (row*40)+39] for row in range(6))
print(f'Part 2:\n{display}')
