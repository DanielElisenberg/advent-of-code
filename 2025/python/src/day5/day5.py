def read_database() -> tuple[list[range], list[int]]:
    with open("src/day5/input", "r") as f:
        content = f.read()
        (fresh_ranges_lines, ingredients) = content.split("\n\n")
        fresh_ranges = [
            range(*[int(number) for number in line.split("-")])
            for line in fresh_ranges_lines.split("\n")
        ]
        ingredients = [
            int(ingredient)
            for ingredient in ingredients.split("\n")
            if ingredient != ""
        ]
    return fresh_ranges, ingredients


def solve_part_one() -> int:
    fresh_ranges, ingredients = read_database()
    return sum(
        1
        for ingredient in ingredients
        if any(ingredient in fresh_range for fresh_range in fresh_ranges)
    )


def overlap(r1: range, r2: range) -> bool:
    return r1.start <= r2.stop and r1.stop >= r2.start


def merge_overlapping(r1: range, r2: range) -> range:
    return range(min(r1.start, r2.start), max(r1.stop, r2.stop))


def solve_part_two() -> int:
    fresh_ranges, _ = read_database()
    overlap_found = True
    merged_ranges = []

    while True:
        current = fresh_ranges.pop()
        while overlap_found:
            overlap_found = False
            new_ranges = []
            for comp in fresh_ranges:
                if overlap(current, comp):
                    current = merge_overlapping(current, comp)
                    overlap_found = True
                else:
                    new_ranges.append(comp)
            fresh_ranges = new_ranges
        overlap_found = True
        merged_ranges.append(current)
        if len(fresh_ranges) == 0:
            return sum(len(merged_range) + 1 for merged_range in merged_ranges)


def solve():
    print(f"Part 1: {solve_part_one()}")
    print(f"Part 2: {solve_part_two()}")


if __name__ == "__main__":
    solve()
