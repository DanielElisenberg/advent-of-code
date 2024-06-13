from collections import defaultdict


def generate_coordinate_list(lines):
    coordinates = []
    for line in lines:
        coordinates.append(
            (int(line.split(",")[0]), int(line.split(", ")[1].strip("\n")))
        )
    return coordinates


def find_closest_coordinate(point, coordinates):
    coordinate_distances = {}

    for coordinate in coordinates:
        distance = (abs(coordinate[0] - point[0]), abs(coordinate[1] - point[1]))
        manhattan_distance = distance[0] + distance[1]
        coordinate_distances[coordinate] = manhattan_distance

    closest_coordinates = [
        k
        for k, v in coordinate_distances.items()
        if v == min([v for k, v in coordinate_distances.items()])
    ]
    if len(closest_coordinates) > 1:
        raise RuntimeError("Two points are equally close!")
    else:
        return closest_coordinates[0]


def sum_of_all_distances(point, coordinates):
    total_distance = 0
    for coordinate in coordinates:
        total_distance += abs(coordinate[0] - point[0]) + abs(coordinate[1] - point[1])
    return total_distance


def find_areas(coordinates, plane_size):
    areas = defaultdict(int)
    for y in plane_size:
        for x in plane_size:
            try:
                closest_point = find_closest_coordinate((x, y), coordinates)
            except RuntimeError:
                continue
            areas[closest_point] += 1
    return areas


def problem_two(coordinates):
    region_size = 0
    for y in range(-500, 500):
        for x in range(-500, 500):
            if sum_of_all_distances((x, y), coordinates) < 10000:
                region_size += 1
    return region_size


def problem_one(coordinates):
    areas_first = find_areas(coordinates, range(-500, 500))
    areas_second = find_areas(coordinates, range(-600, 600))
    stable_areas = []

    for coordinate, size in areas_first.items():
        if size == areas_second[coordinate]:
            stable_areas.append(size)

    return max(stable_areas)


input = open("day06/input", "r")
lines = input.readlines()

coordinates = generate_coordinate_list(lines)

print(f"answer #1: {problem_one(coordinates)}")
print(f"answer #2:{problem_two(coordinates)}")
