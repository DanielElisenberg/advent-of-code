class Manifold:
    map: dict[tuple[int, int], str]
    starting_point: tuple[int, int]
    max_y: int
    max_x: int

    def __init__(self, map: dict[tuple[int, int], str]):
        self.map = map
        self.max_x = max(x for (x, _) in self.map.keys())
        self.max_y = max(y for (_, y) in self.map.keys())
        self.starting_point = next(
            (x, y) for (x, y) in self.map.keys() if self.map[(x, y)] == "S"
        )


def read_tachyon_manifold() -> Manifold:
    map = {}
    with open("src/day7/input", "r") as f:
        for y, line in enumerate(f.readlines()):
            for x, char in enumerate(line.strip()):
                map[(int(x), int(y))] = char
    return Manifold(map)


def solve_part_one():
    manifold = read_tachyon_manifold()
    splits = 0
    beams = set([(manifold.starting_point[0], manifold.starting_point[1] + 1)])
    while beams:
        new_beams = []
        for beam in beams:
            match manifold.map[beam]:
                case "^":
                    splits += 1
                    new_beams.extend([
                        (beam[0] + 1, beam[1]+1),
                        (beam[0] - 1, beam[1]+1),
                    ])
                case ".":
                    new_beams.extend([(beam[0], beam[1] + 1)])
        beams = set([
            beam for beam in new_beams if manifold.map.get(beam, None) is not None
        ])
    return splits


def solve_part_two():
    many_worlds_cache = {}
    def traverse(manifold: Manifold, beam: tuple[int, int]) -> int:
        if beam in many_worlds_cache:
            return many_worlds_cache[beam]
        if manifold.map.get(beam, None) is None:
            return 1
        match manifold.map[beam]:
            case "^":
                result = traverse(manifold, (beam[0] + 1, beam[1]+1)) + traverse(manifold, (beam[0] - 1, beam[1]+1))
            case ".":
                result = traverse(manifold, (beam[0], beam[1] + 1))
            case _:
                raise ValueError(f"Invalid: {manifold.map[beam]}")
        many_worlds_cache[beam] = result
        return result
    manifold = read_tachyon_manifold()
    return traverse(manifold, (manifold.starting_point[0], manifold.starting_point[1] + 1))


def solve():
    print(f"Part 1: {solve_part_one()}")
    print(f"Part 2: {solve_part_two()}")


if __name__ == "__main__":
    solve()
