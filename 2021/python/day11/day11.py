from typing import Tuple
from copy import deepcopy


GRID_SIZE = 10


def run_step(octopus_map: dict) -> int:
    for point in octopus_map.keys():
        octopus_map[point] += 1
        if octopus_map[point] == 10:
            flash(octopus_map, point)

    flash_counter = 0
    for point in octopus_map.keys():
        if octopus_map[point] > 9:
            flash_counter += 1
            octopus_map[point] = 0
    return flash_counter


def flash(octopus_map: dict, flash_point: Tuple[int, int]) -> None:
    (flash_point_y, flash_point_x) = flash_point
    surrounding_points = [
        (-1, -1), (-1, 0), (-1, 1),
        (1, -1), (1, 0), (1, 1),
        (0, -1), (0, 1)
    ]
    surrounding_octopi = [
        (flash_point_y + y, flash_point_x + x)
        for (y, x) in surrounding_points
        if flash_point[0] + y in range(GRID_SIZE) and
        flash_point[1] + x in range(GRID_SIZE)
    ]
    for point in surrounding_octopi:
        octopus_map[point] += 1
        if octopus_map[point] == 10:
            flash(octopus_map, point)


def count_flashes(octopus_map: dict, steps: int) -> int:
    flash_count = 0
    for _ in range(100):
        flash_count += run_step(octopus_map)
    return flash_count


def find_synchronization_step(octopus_map: dict) -> int:
    all_flash = False
    counter = 0
    while not all_flash:
        counter += 1
        run_step(octopus_map)
        all_flash = all([
            energy_level == 0 for energy_level in octopus_map.values()
        ])
    return counter


if __name__ == "__main__":
    with open('day11/input') as input_file:
        octopus_grid = [
            [int(char) for char in line.strip()]
            for line in input_file.readlines()
        ]
        octopus_map = {}
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                octopus_map[(x, y)] = octopus_grid[y][x]

    print(
        f"""Day 11:
        first solution: {count_flashes(deepcopy(octopus_map), steps=100)}
        second solution: {find_synchronization_step(deepcopy(octopus_map))}"""
    )
