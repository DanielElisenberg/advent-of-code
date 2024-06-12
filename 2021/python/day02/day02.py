import numpy as np


def resolve_position_part_one(actions):
    direction_map = {
        "forward": np.array([1, 0]),
        "down": np.array([0, 1]),
        "up": np.array([0, -1])
    }
    my_position = sum([
        direction_map[direction] * int(amount)
        for (direction, amount) in actions
    ])
    return my_position[0]*my_position[1]


def resolve_position_part_two(actions):
    my_position = np.array([0, 0])
    aim = 0
    for (direction, amount) in actions:
        if direction == "up":
            aim -= int(amount)
        if direction == "down":
            aim += int(amount)
        if direction == "forward":
            my_position += np.array([int(amount), int(amount)*aim])
    return my_position[0] * my_position[1]


if __name__ == "__main__":
    with open('day02/input') as input_file:
        actions = [
            line.strip('\n').split(" ") for line in input_file.readlines()
        ]

    print(
        f"""Day 2:
        first solution: {resolve_position_part_one(actions)}
        second solution: {resolve_position_part_two(actions)}"""
    )
