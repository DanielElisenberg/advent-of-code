from collections import defaultdict


def generate_vent_map(input: list, ignore_diagonal: bool = True) -> dict:
    vent_map = defaultdict(int)
    for line in input:
        (x1, y1) = [int(coordinate) for coordinate in line[0].split(',')]
        (x2, y2) = [int(coordinate) for coordinate in line[2].split(',')]
        if not(x1 == x2 or y1 == y2) and ignore_diagonal:
            continue

        x_slope = (x2-x1)//abs(x1-x2) if x2-x1 else x2-x1
        y_slope = (y2-y1)//abs(y1-y2) if y2-y1 else y2-y1

        current_point = (x1, y1)
        while current_point != (x2+x_slope, y2+y_slope):
            vent_map[current_point] += 1
            current_point = (
                current_point[0] + x_slope, current_point[1] + y_slope
            )
    return vent_map


if __name__ == "__main__":
    with open('day05/input') as input_file:
        input = [
            line.strip().split() for line in input_file.readlines()
        ]

    vent_map = generate_vent_map(input, ignore_diagonal=True)
    first_solution = len(
        [position for position in vent_map if vent_map[position] > 1]
    )

    vent_map = generate_vent_map(input, ignore_diagonal=False)
    second_solution = len(
        [position for position in vent_map if vent_map[position] > 1]
    )

    print(
        f"""Day 5:
        first solution: {first_solution}
        second solution: {second_solution}"""
    )
