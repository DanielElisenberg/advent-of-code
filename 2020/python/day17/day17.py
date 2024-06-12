from collections import defaultdict
import simulation


with open('day17/input.data') as input:
    lines = [line for line in input.read().split('\n')]
    pocket_dimension_3D = defaultdict(int)
    pocket_dimension_4D = defaultdict(int)
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            pocket_dimension_3D[(x, y, 0)] = 1 if ch == '#' else 0
            pocket_dimension_4D[(x, y, 0, 0)] = 1 if ch == '#' else 0

print(
    f'first solution: {simulation.run_boot_process_3D(pocket_dimension_3D)}'
)
print(
    f'second solution: {simulation.run_boot_process_4D(pocket_dimension_4D)}'
)
