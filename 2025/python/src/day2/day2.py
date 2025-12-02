def read_ranges() -> list[range]:
    with open("src/day2/input", "r") as f:
        return [
            range(int(pid_range[0]), int(pid_range[1]) + 1)
            for pid_range in [
                pid_range.split("-") for pid_range in f.read().strip().split(",")
            ]
        ]


def solve_part_1(pid_range: range) -> int:
    def is_invalid(id: str) -> bool:
        return id[: len(id) // 2] == id[len(id) // 2 :]

    return sum([int(id) for id in pid_range if is_invalid(str(id))])


def solve_part_2(pid_range: range) -> int:
    def is_invalid(id: str) -> bool:
        for size in range(1, (len(id) // 2)+1):
            if len(id) % size != 0:
                continue
            id_chunks = [id[start:start+size] for start in range(0, len(id), size)]
            if all(id_chunk == id_chunks[0] for id_chunk in id_chunks):
                return True
        return False
    return sum([int(id) for id in pid_range if is_invalid(str(id))])


print(f"Part 1: {sum(solve_part_1(pid_range) for pid_range in read_ranges())}")
print(f"Part 2: {sum(solve_part_2(pid_range) for pid_range in read_ranges())}")
