from math import prod
from functools import cmp_to_key

from typing import Union


def compare(left: Union[list, int], right: Union[list, int]) -> bool:
    if isinstance(left, int) and isinstance(right, int):
        return (right - left) // (abs(right-left) if abs(right-left) else 1)
    left = [left] if isinstance(left, int) else left
    right = [right] if isinstance(right, int) else right
    shortest = min(len(left), len(right))
    for index in range(shortest):
        result = compare(left[index], right[index])
        if result != 0:
            return result
    return compare(len(left), len(right))


def find_decoder_key(pairs: list) -> int:
    divider_packets = [[[2]], [[6]]]
    packets = sum(pairs, []) + divider_packets
    sorted_packets = sorted(packets, key=cmp_to_key(compare), reverse=True)
    return prod(
        index + 1 for index, packet in enumerate(sorted_packets)
        if packet in divider_packets
    )


with open('day13/input', encoding='utf-8') as f:
    pairs = [
        [eval(line.split('\n')[0]), eval(line.split('\n')[1])]
        for line in f.read().split('\n\n')
    ]

ordered_pair_indices = [
    index+1 for index, pair in enumerate(pairs)
    if compare(pair[0], pair[1]) == 1
]
print(f'Part 1: {sum(ordered_pair_indices)}')
print(f'Part 2: {find_decoder_key(pairs)}')
