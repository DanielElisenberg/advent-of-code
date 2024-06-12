from typing import Union
from collections import defaultdict


def manhattan_distance(
    point_a: tuple[int, int], point_b: tuple[int, int]
) -> int:
    return (abs(point_a[0]-point_b[0]) + abs(point_a[1]-point_b[1]))


def merge(
    interval: tuple[int, int], other: tuple[int, int]
) -> Union[tuple[int, int], None]:
    if (
        other[0] <= interval[0] <= other[1] or
        other[0] <= interval[1] <= other[1] or
        interval[0] <= other[0] <= interval[1] or
        interval[0] <= other[1] <= interval[1]
    ):
        return (min(interval[0], other[0]), max(interval[1], other[1]))
    return None


def merge_all_intervals(
    intervals: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    merged = []
    intervals.sort()
    while intervals:
        merged_indices = []
        merged_interval = intervals[0]
        for index, other in enumerate(intervals[1:]):
            new_merge = merge(merged_interval, other)
            if new_merge:
                merged_indices.append(index)
                merged_interval = new_merge
        merged.append(merged_interval)
        intervals = [
            interval for index, interval in enumerate(intervals[1:])
            if index not in merged_indices
        ]
    return merged


def get_explored_rows(
    sensors: dict[tuple[int, int], tuple[int, int]]
) -> dict[int, list[tuple[int, int]]]:
    explored_rows = defaultdict(list)
    for sensor, closest_beacon in sensors.items():
        distance = manhattan_distance(sensor, closest_beacon)
        shrink = 0
        while shrink <= distance:
            explored_rows[sensor[1]+shrink].append(
                (sensor[0]-distance+shrink, sensor[0]+distance+1-shrink)
            )
            explored_rows[sensor[1]-shrink].append(
                (sensor[0]-distance+shrink, sensor[0]+distance+1-shrink)
            )
            shrink += 1
    return {
        y: merge_all_intervals(intervals)
        for y, intervals in explored_rows.items()
    }


def count_explored_locations(
    explored_rows: dict[int, list[tuple[int, int]]],
    sensors: dict[tuple[int, int], tuple[int, int]],
    row_number: int
) -> int:
    explored_row = explored_rows[row_number]
    explored_row_count = sum(
        interval[1]-interval[0] for interval in explored_rows[row_number]
    )
    unique_beacons_row = set(
        x for x, y in sensors.values() if y == row_number
    )
    overlapping_beacons_row = len([
        list for list in [
            ['' for interval in explored_row if interval[0] <= x < interval[1]]
            for x in unique_beacons_row
        ] if list
    ])
    return explored_row_count - overlapping_beacons_row


def find_unexplored_location(explored_rows: dict[int, list[tuple[int, int]]]):
    for y in range(4000001):
        x = 0
        for interval in explored_rows[y]:
            if interval[0] <= x < interval[1]:
                x = interval[1]
                continue
            else:
                return (x*4000000)+y


with open('day15/input', encoding='utf-8') as f:
    lines = [line.strip().split(' ') for line in f.readlines()]
sensors = {
    (int(line[2][2:-1]), int(line[3][2:-1])):
    (int(line[-2][2:-1]), int(line[-1][2:]))
    for line in lines
}
explored_rows = get_explored_rows(sensors)
print(f'Part 1: {count_explored_locations(explored_rows, sensors, 2000000)}')
print(f'Part 2: {find_unexplored_location(explored_rows)}')
