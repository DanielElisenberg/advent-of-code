def read_floor_plan() -> dict[tuple[int, int], str]:
    floor_plan = {}
    with open("src/day4/input", "r") as f:
        for y, line in enumerate(f.readlines()):
            for x, char in enumerate(line.strip()):
                floor_plan[(x, y)] = char
    return floor_plan


def can_move(x, y, floor_plan: dict[tuple[int, int], str]):
    directions = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
        (1, 1),
        (-1, -1),
        (1, -1),
        (-1, 1),
    ]
    occupied_count = 0
    for dx, dy in directions:
        if floor_plan.get((x + dx, y + dy), ".") == "@":
            occupied_count += 1
        if occupied_count > 3:
            return False
    return True


def solve_part_one() -> int:
    floor_plan = read_floor_plan()
    movable = [
        (x, y)
        for ((x, y), char) in floor_plan.items()
        if char == "@" and can_move(x, y, floor_plan)
    ]
    return len(movable)


def solve_part_two() -> int:
    floor_plan = read_floor_plan()
    movable_rolls_exist = True
    total_rolls_moved = 0
    while movable_rolls_exist:
        movable = [
            (x, y)
            for ((x, y), char) in floor_plan.items()
            if char == "@" and can_move(x, y, floor_plan)
        ]
        total_rolls_moved += len(movable)
        if len(movable) == 0:
            movable_rolls_exist = False
        for moved in movable:
            floor_plan[moved] = "."
    return total_rolls_moved


def solve():
    print(f"Part 1: {solve_part_one()}")
    print(f"Part 2: {solve_part_two()}")


if __name__ == "__main__":
    solve()
