from collections import deque
from copy import deepcopy
import numpy as np


def align_slope(map, angle):
    for y in range(len(map)):
        map[y].rotate(y*-angle)


def trees_encountered(map, angle):
    map = deepcopy(map)
    align_slope(map, angle)
    return len(
        [location[0] for location in map if location[0] == '#']
    )


with open('day03/input.data') as input:
    map = [deque(line) for line in input.read().splitlines()]

print(f'first solution: {trees_encountered(map, 3)}')

total_trees_encountered = np.product(
    [trees_encountered(m, a) for (m, a) in [
     (map, 1), (map, 3), (map, 5), (map, 7), (map[::2], 1)]]
)
print(f'second solution: {total_trees_encountered}')
