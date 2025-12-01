from collections import deque


def read_instructions() -> list[int]:
    with open("src/day1/input", "r") as f:
        return [
            (-1 if line[0] == "R" else 1) * int(line.strip()[1:])
            for line in f.readlines()
        ]


def generate_dial() -> deque[int]:
    dial = deque(list(range(0, 100)))
    dial.rotate(50)
    return dial


def solve_part_one() -> int:
    def count_zeros(dial: deque[int], turn: int) -> int:
        dial.rotate(turn)
        return 1 if dial[0] == 0 else 0

    dial = generate_dial()
    return sum(count_zeros(dial, turn) for turn in read_instructions())


def solve_part_two() -> int:
    def count_zeros(dial: deque[int], turn: int) -> int:
        last_dial = dial[0]
        dial.rotate(turn)
        current_dial = dial[0]
        zeros = abs(turn) // 100
        if 0 < turn and last_dial < current_dial and last_dial != 0:
            return zeros + 1
        if turn < 0 and current_dial < last_dial:
            return zeros + 1
        if current_dial == 0:
            return zeros + 1
        return zeros

    dial = generate_dial()
    return sum(count_zeros(dial, turn) for turn in read_instructions())


def solve():
    print(f"Part 1: {solve_part_one()}")
    print(f"Part 2: {solve_part_two()}")


if __name__ == "__main__":
    solve()
