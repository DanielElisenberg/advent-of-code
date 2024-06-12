def generate_height_map(input: list) -> dict:
    height_map = {}
    for y, line in enumerate(input):
        for x, char in enumerate(line):
            height_map[(x, y)] = int(char)
    return height_map


def find_low_points(height_map: dict, size: int) -> list:
    low_points = []
    for y in range(size):
        for x in range(size):
            height = height_map[(x, y)]
            surrounding_heights = [
                height_map.get((x, y-1), 10),
                height_map.get((x, y+1), 10),
                height_map.get((x-1, y), 10),
                height_map.get((x+1, y), 10)
            ]
            if min(surrounding_heights) > height:
                low_points.append((x, y))
    return low_points


def explore_basins(basins: list[list], height_map: dict) -> list[list]:
    for basin in basins:
        keep_going = True
        while keep_going:
            new_points = []
            for point in basin:
                surrounding_points = [
                    (point[0],   point[1]-1),
                    (point[0]-1, point[1]),
                    (point[0]+1, point[1]),
                    (point[0],   point[1]+1)
                ]
                found_points = [
                    found_point for found_point in surrounding_points
                    if found_point not in basin + new_points
                    and height_map.get(found_point, 10) < 9
                ]
                new_points += found_points
            keep_going = True if new_points else False
            basin += new_points
    return basins


if __name__ == "__main__":
    with open('day09/input') as input_file:
        input = [
            line.strip() for line in input_file.readlines()
        ]

    basins = []
    low_points = []
    size = len(input)
    height_map = generate_height_map(input)

    low_points = find_low_points(height_map, size)
    basins = explore_basins(
        [[low_point] for low_point in low_points],
        height_map
    )

    first_solution = sum([
        height_map[low_point]+1 for low_point in low_points
    ])

    basin_sizes = [len(basin) for basin in basins]
    basin_sizes.sort()
    second_solution = basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]

    print(
        f"""Day 9:
        first solution: {first_solution}
        second solution: {second_solution}"""
    )
