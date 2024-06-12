def bounds_to_locations(bounds):
    locations = []
    for start, stop in bounds:
        start = (int(start[0]), int(start[1]))
        stop = (int(stop[0]), int(stop[1]))
        if start[0] == stop[0]:
            for y in range(
                min([start[1], stop[1]]), max([start[1], stop[1]]) + 1
            ):
                locations.append((start[0], y))
        if start[1] == stop[1]:
            for x in range(
                min([start[0], stop[0]]), max([start[0], stop[0]]) + 1
            ):
                locations.append((x, stop[1]))
    return locations


def get_falling_directions(sand: tuple[int, int]):
    return [
        (sand[0], sand[1]+1),
        (sand[0]-1, sand[1]+1),
        (sand[0]+1, sand[1]+1)
    ]


def get_sand_at_rest(rock_map: dict, part: int) -> int:
    collision_map = {**rock_map}
    source_location = (500, 0)
    floor = max(y for _, y in collision_map.keys())
    sand_counter = 0
    while True:
        new_sand = source_location
        sand_counter += 1
        while True:
            if new_sand[1] > floor and part == 1:
                return sand_counter - 1
            if new_sand[1] > floor and part == 2:
                collision_map[new_sand] = 'o'
                break
            falling_directions = get_falling_directions(new_sand)
            new_sand = next(
                (d for d in falling_directions if d not in collision_map),
                new_sand
            )
            if new_sand not in falling_directions:
                collision_map[new_sand] = 'o'
                if new_sand == source_location:
                    return sand_counter
                break


with open('day14/input', encoding='utf-8') as f:
    rock_edges_list = [
        [coord.split(',') for coord in line.split(' -> ')]
        for line in f.read().split('\n')
    ]
    rock_bounds_list = [
        list(zip(*[rock_edges, rock_edges[1:]]))
        for rock_edges in rock_edges_list
    ]
    rock_map = {
        location: '#' for location in
        sum([bounds_to_locations(bounds) for bounds in rock_bounds_list], [])
    }
print(f'Part 1: {get_sand_at_rest(rock_map, part=1)}')
print(f'Part 2: {get_sand_at_rest(rock_map, part=2)}')
