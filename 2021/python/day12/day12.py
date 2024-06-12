from collections import defaultdict
from copy import copy


def traverse_one(map: dict, path: list, paths_to_end: list) -> None:
    if path[-1] == "end":
        paths_to_end.append(path)
        return
    next_steps = [
        cave for cave in map[path[-1]]
        if cave.isupper() or (cave.islower() and cave not in path)
    ]
    for step in next_steps:
        traverse_one(map, copy(path) + [step], paths_to_end)


def traverse_two(map: dict, path: list, paths_to_end: list) -> None:
    if path[-1] == "end":
        paths_to_end.append(path)
        return
    small_caves_in_path = [cave for cave in path if cave.islower()]
    small_cave_visited_twice = (
        len(small_caves_in_path) - len(set(small_caves_in_path))
    )
    next_steps = [
        cave for cave in map[path[-1]]
        if cave.isupper() or
        (cave.islower() and cave not in path) or
        (cave.islower() and not small_cave_visited_twice and cave != "start")
    ]
    for step in next_steps:
        traverse_two(map, copy(path) + [step], paths_to_end)


if __name__ == "__main__":
    with open('day12/input') as input_file:
        cave_connections = [
            line.strip().split("-") for line in input_file.readlines()
        ]
        map = defaultdict(list)
        for (cave_one, cave_two) in cave_connections:
            map[cave_one].append(cave_two)
            map[cave_two].append(cave_one)

    paths_to_end_one = []
    paths_to_end_two = []
    traverse_one(map, ['start'], paths_to_end_one)
    traverse_two(map, ['start'], paths_to_end_two)

    print(
        f"""Day 12:
        first solution: {len(paths_to_end_one)}
        second solution: {len(paths_to_end_two)}"""
    )
