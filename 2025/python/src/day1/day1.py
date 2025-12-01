from typing import Literal
from collections import deque


dir = Literal["L"] | Literal["R"]


def read_instructions() -> list[tuple[dir, int]]:
    with open("src/day1/input", "r") as f:
        return [
            ("R" if line[0] == "R" else "L", int(line.strip()[1:]))
            for line in f.readlines()
        ]


def generate_dial() -> deque:
    dial = deque(list(range(0, 100)))
    dial.rotate(50)
    return dial


def solve_part_one() -> int:
    sum = 0
    dial = generate_dial()
    for direction, amount in read_instructions():
        match direction:
            case "R":
                dial.rotate(-amount)
            case "L":
                dial.rotate(amount)
        if dial[0] == 0:
            sum += 1
    return sum


def solve_part_two() -> int:
    dial = generate_dial()
    sum = 0
    for direction, amount in read_instructions():
        last_dial = dial[0]
        match direction:
            case "R":
                dial.rotate(-amount)
            case "L":
                dial.rotate(amount)
        current_dial = dial[0]
        sum = sum + (amount // 100)
        if direction == "L" and last_dial < current_dial and last_dial != 0:
            sum += 1
        elif direction == "R" and last_dial > current_dial:
            sum += 1
        elif last_dial == 0 and current_dial == 0:
            sum -= 1
        elif current_dial == 0:
            sum += 1
    return sum


def solve():
    print(f"Part 1: {solve_part_one()}")
    print(f"Part 2: {solve_part_two()}")


if __name__ == "__main__":
    solve()
