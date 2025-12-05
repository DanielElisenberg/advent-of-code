def get_battery_banks() -> list[list[int]]:
    with open("src/day3/input", "r") as f:
        return [
            list(reversed([int(battery) for battery in bank.strip()]))
            for bank in f.readlines()
        ]


def get_bank_joltage(battery_bank: list[int], joltage_size: int) -> int:
    selected_batteries = battery_bank[:joltage_size]
    search_range = (joltage_size, len(battery_bank))
    for battery_index in reversed(range(joltage_size)):
        joltage = selected_batteries[battery_index]
        next_search_start = search_range[0] - 1
        next_search_stop = search_range[0] - 1
        for search_index in range(*search_range):
            if battery_bank[search_index] >= joltage:
                joltage = battery_bank[search_index]
                selected_batteries[battery_index] = joltage
                next_search_stop = search_index
        search_range = (next_search_start, next_search_stop)
    return int(
        "".join(str(joltage) for joltage in reversed(selected_batteries))
    )


def solve_part_one() -> int:
    return sum([
        get_bank_joltage(battery_bank, 2)
        for battery_bank in get_battery_banks()
    ])


def solve_part_two() -> int:
    return sum([
        get_bank_joltage(battery_bank, 12)
        for battery_bank in get_battery_banks()
    ])


def solve():
    print(f"Part 1: {solve_part_one()}")
    print(f"Part 2: {solve_part_two()}")


if __name__ == "__main__":
    solve()
