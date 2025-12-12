def read_graph() -> dict[str, list[str]]:
    with open("src/day11/input") as f:
        lines = [line.strip() for line in f.read().splitlines()]
        return {
            line.split(":")[0]: [
                item.strip() for item in line.split(":")[1].split()
            ]
            for line in lines
        }


def solve_part_one():
    graph = read_graph()

    def ways_out(current: str) -> int:
        if current == "out":
            return 1
        return sum(ways_out(next) for next in graph[current])

    return ways_out("you")


def solve_part_two():
    graph = read_graph()
    cache = {}
    def ways_out(current: str, visited: set[str]) -> int:
        dac_visited_bit = 1 if "dac" in visited else 0
        fft_visited_bit = 1 if "fft" in visited else 0
        hash = f"{current}{dac_visited_bit}{fft_visited_bit}"
        if current == "out":
            return 1 if hash == "out11" else 0 
        if hash in cache.keys():
            return cache[hash]
        visited.add(current)
        result = sum(ways_out(next, visited.copy()) for next in graph[current])
        cache[hash] = result
        return result

    return ways_out("svr", set())


def solve():
    print(f"Part 1: {solve_part_one()}")
    print(f"Part 2: {solve_part_two()}")

if __name__ == "__main__":
    solve()
