import math
from dataclasses import dataclass
from enum import StrEnum


class Operation(StrEnum):
    MULTIPLY = "*"
    ADD = "+"


@dataclass
class Problem:
    numbers: list[int]
    operation: Operation

    def solve(self):
        match self.operation:
            case Operation.MULTIPLY:
                return math.prod(self.numbers)
            case Operation.ADD:
                return sum(self.numbers)


def read_homework() -> list[Problem]:
    with open("src/day6/input", "r") as f:
        split_lines = [line.strip().split() for line in f.readlines()]
        return [
            Problem(
                numbers=list(int(char) for char in line[:-1]),
                operation=Operation(line[-1]),
            )
            for line in zip(*split_lines)
        ]


def read_homework_cephelopod_style() -> list[Problem]:
    def convert_to_cephalopod_numbers(numbers: list[str]) -> list[int]:
        return [
            int("".join(digit for digit in number if digit != " "))
            for number in zip(*numbers)
            if not all(digit == " " for digit in number)
        ]

    with open("src/day6/input", "r") as f:
        lines = [line.strip("\n") for line in f.readlines()]
        chunk_indices = [
            i for i, char in enumerate(lines[-1].strip("\n")) if char != " "
        ] + [len(lines[-1])]
        chunk_ranges = list(zip(chunk_indices, chunk_indices[1:]))
        split_lines = [
            [line[start:stop] for (start, stop) in chunk_ranges]
            for line in lines
        ]
        return [
            Problem(
                numbers=convert_to_cephalopod_numbers(list(line[:-1])),
                operation=Operation(line[-1].strip()),
            )
            for line in zip(*split_lines)
        ]


def solve_part_one() -> int:
    return sum(problem.solve() for problem in read_homework())


def solve_part_two() -> int:
    return sum(problem.solve() for problem in read_homework_cephelopod_style())


def solve():
    print(f"Part 1: {solve_part_one()}")
    print(f"Part 2: {solve_part_two()}")


if __name__ == "__main__":
    solve()
