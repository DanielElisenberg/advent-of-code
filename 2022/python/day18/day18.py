def get_adjacent_cubes(
    cube: tuple[int, int, int]
) -> list[tuple[int, int, int]]:
    transforms = [
        (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)
    ]
    x, y, z = cube
    return [
        (x+x_transform, y+y_transform, z+z_transform)
        for x_transform, y_transform, z_transform in transforms
    ]


def inside_bounds(
    cube: tuple[int, int, int],
    min_bound: tuple[int, int, int],
    max_bound: tuple[int, int, int]
) -> bool:
    x, y, z = cube
    return (
        (min_bound[0] <= x <= max_bound[0])
        and (min_bound[1] <= y <= max_bound[1])
        and (min_bound[2] <= z <= max_bound[2])
    )


def map_exterior(
    blocking_cubes: list[tuple[int, int, int]]
) -> list[tuple[int, int, int]]:
    x_coordinates = [x for x, _, _ in blocking_cubes]
    y_coordinates = [y for _, y, _ in blocking_cubes]
    z_coordinates = [z for _, _, z in blocking_cubes]
    min_bound = (
        min(x_coordinates)-1, min(y_coordinates)-1, min(z_coordinates)-1
    )
    max_bound = (
        max(x_coordinates)+1, max(y_coordinates)+1, max(z_coordinates)+1
    )
    traversables = [min_bound]
    visited = []
    while traversables:
        current = traversables[0]
        traversables = traversables[1:]
        visited.append(current)
        new_traversables = get_adjacent_cubes(current)
        traversables += [
            traversable for traversable in new_traversables
            if traversable not in blocking_cubes + visited + traversables
            and inside_bounds(traversable, min_bound, max_bound)
        ]
    return visited


with open('day18/input', encoding='utf-8') as f:
    coordinates = [line.strip().split(',') for line in f]
    cubes = [(int(x), int(y), int(z)) for x, y, z in coordinates]

exposed_sides = sum([
    len([
        adjacent for adjacent in get_adjacent_cubes(cube)
        if adjacent not in cubes
    ])
    for cube in cubes
])
print(f'Part 1: {exposed_sides}')

exterior = map_exterior(cubes)
exposed_exterior_sides = sum([
    len([
        adjacent for adjacent in get_adjacent_cubes(cube)
        if adjacent not in cubes and adjacent in exterior
    ])
    for cube in cubes
])
print(f'Part 2: {exposed_exterior_sides}')
