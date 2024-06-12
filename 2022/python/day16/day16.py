import random
from itertools import accumulate
from typing import Union


class Pathfinder:
    path: list[str]
    minutes_passed: list[int]
    next: dict[str, str]

    def __init__(
        self, path: list[str], shortest_paths: dict[str, dict[str, int]]
    ):
        self.path = ['AA'] + path
        self.minutes_passed = list(accumulate([
            shortest_paths[from_valve][to_valve] + 1
            for from_valve, to_valve in zip(self.path, self.path[1:])
        ]))
        self.next = {
            from_valve: to_valve for
            from_valve, to_valve in
            zip(self.path[1:], self.path[2:])
        }
        self.next[self.path[-1]] = self.path[1]

    def fitness(self, vfr: dict):
        return sum([
            vfr[step] * (30-self.minutes_passed[index])
            for index, step in enumerate(self.path[1:])
            if self.minutes_passed[index] < 30
        ])

    def make_child(
        self, other: 'Pathfinder', shortest_paths: dict[str, dict[str, int]]
    ) -> 'Pathfinder':
        next_is_self = True
        path = [other.path[1]]
        full_path_len = len(self.path) - 1
        while len(path) < full_path_len:
            parent = self if next_is_self else other
            next_valve = parent.next[path[-1]]
            while next_valve in path:
                next_valve = parent.next[next_valve]
            next_is_self = not next_is_self
            path.append(next_valve)
        return Pathfinder(path, shortest_paths)

    def mutate(
        self, shortest_paths: dict[str, dict[str, int]]
    ) -> 'Pathfinder':
        if random.randint(0, 100) > 5:
            return self
        mutated_path = self.path[1:]
        for _ in range(random.randint(0, len(self.path[1:]))):
            switch_index = random.randint(0, len(mutated_path) - 1)
            for_index = random.randint(0, len(mutated_path) - 1)
            temp = mutated_path[switch_index]
            mutated_path[switch_index] = mutated_path[for_index]
            mutated_path[for_index] = temp
        return Pathfinder(mutated_path, shortest_paths)


class PathfinderWithElephant:
    path: list[str]
    elephant_path: list[str]
    minutes_passed: list[int]
    elephant_minutes_passed: list[int]
    next: dict[str, str]

    def __init__(
        self,
        path: list[str],
        shortest_paths: dict[str, dict[str, int]],
    ):
        self.path = ['AA'] + path[:(len(path)//2)]
        self.elephant_path = ['AA'] + path[(len(path)//2):]
        self.minutes_passed = list(accumulate([
            shortest_paths[from_valve][to_valve] + 1
            for from_valve, to_valve in zip(self.path, self.path[1:])
        ]))
        self.elephant_minutes_passed = list(accumulate([
            shortest_paths[from_valve][to_valve] + 1
            for from_valve, to_valve in
            zip(self.elephant_path, self.elephant_path[1:])
        ]))
        self.next = {
            from_valve: to_valve for
            from_valve, to_valve in
            zip(path, path[1:])
        }
        self.next[path[-1]] = self.path[1]

    def fitness(self, vfr: dict):
        path_sum = sum([
            vfr[step] * (26-self.minutes_passed[index])
            for index, step in enumerate(self.path[1:])
            if self.minutes_passed[index] < 30
        ])
        elephant_sum = sum([
            vfr[step] * (26-self.elephant_minutes_passed[index])
            for index, step in enumerate(self.elephant_path[1:])
            if self.elephant_minutes_passed[index] < 30
        ])
        return elephant_sum + path_sum

    def make_child(
        self,
        other: 'PathfinderWithElephant',
        shortest_paths: dict[str, dict[str, int]]
    ) -> 'PathfinderWithElephant':
        next_is_self = True
        path = [other.path[1]]
        full_path_len = len(self.path[1:]) + len(self.elephant_path[1:])
        while len(path) < full_path_len:
            parent = self if next_is_self else other
            next_valve = parent.next[path[-1]]
            while next_valve in path:
                next_valve = parent.next[next_valve]
            next_is_self = not next_is_self
            path.append(next_valve)
        return PathfinderWithElephant(path, shortest_paths)

    def mutate(
        self, shortest_paths: dict[str, dict[str, int]]
    ) -> 'PathfinderWithElephant':
        if random.randint(0, 100) > 10:
            return self
        if random.randint(0, 1) == 1:
            return PathfinderWithElephant(
                (
                    self.elephant_path[1:-1]
                    + self.path[1:]
                    + [self.elephant_path[-1]]
                ),
                shortest_paths
            )
        mutated_path = self.path[1:] + self.elephant_path[1:]
        for _ in range(random.randint(0, len(mutated_path))):
            switch_index = random.randint(0, len(mutated_path) - 1)
            for_index = random.randint(0, len(mutated_path) - 1)
            temp = mutated_path[switch_index]
            mutated_path[switch_index] = mutated_path[for_index]
            mutated_path[for_index] = temp
        return PathfinderWithElephant(mutated_path, shortest_paths)


def generate_pathfinders(
    valves: list[str],
    shortest_paths: dict[str, dict[str, int]],
    vfr: dict[str, int],
    amount: int,
    with_elephant: bool = False
) -> Union[list[Pathfinder], list[PathfinderWithElephant]]:
    def generate_pathfinder(
        valves: list[str],
        shortest_paths: dict[str, dict[str, int]],
        with_elephant: bool
    ) -> Union[Pathfinder, PathfinderWithElephant]:
        if with_elephant:
            return PathfinderWithElephant(
                random.sample(list(valves), len(valves)), shortest_paths
            )
        return Pathfinder(
            random.sample(list(valves), len(valves)), shortest_paths
        )
    return sorted(
        [
            generate_pathfinder(valves, shortest_paths, with_elephant)
            for _ in range(amount)
        ],
        key=lambda x: x.fitness(vfr)
    )


def find_shortest_paths(
    valve_leads_to: dict[str, list[str]]
) -> dict[dict[str, int]]:
    def find_shortest_path(valve, other, valve_leads_to, visited):
        new_visited = [valve, *visited]
        if other == valve:
            return 0
        if other in valve_leads_to[valve]:
            return 1
        paths = [
            find_shortest_path(
                next_valve, other, valve_leads_to, new_visited
            ) + 1
            for next_valve in valve_leads_to[valve]
            if next_valve not in visited
        ]
        if not paths:
            return 10_000_000
        return min(paths)
    return {
        valve: {
            other: find_shortest_path(valve, other, valve_leads_to, [])
            for other in valve_leads_to
        } for valve in valve_leads_to
    }


def solve(
    pathfinders: Union[list[Pathfinder], list[PathfinderWithElephant]],
    shortest_paths: dict[str, dict[str, int]],
    vfr: dict[str, int]
) -> int:
    max_score = pathfinders[-1].fitness(vfr)
    for gen in range(50000):
        # print(f'Generation {gen}: {max_score}')
        top_pathfinders = pathfinders[400:]
        parents = list(zip(top_pathfinders[:50], top_pathfinders[50:]))
        children = [
            mother.make_child(father, shortest_paths)
            for mother, father in parents
        ]
        pathfinders = sorted(
            [
                pathfinder.mutate(shortest_paths)
                for pathfinder in pathfinders[50:] + children
            ],
            key=lambda x: x.fitness(vfr)
        )
        gen_score = pathfinders[-1].fitness(vfr)
        max_score = gen_score if gen_score > max_score else max_score
    return max_score


with open('day16/input', encoding='utf-8') as f:
    lines = [line.strip().split(' ') for line in f]
valve_leads_to = {
    line[1]: [valve.strip(',') for valve in line[9:]]
    for line in lines
}
vfr = {
    line[1]: int(line[4].strip('rate=').strip(';')) for line in lines
}
shortest_paths = find_shortest_paths(valve_leads_to)
non_zero_valves = [valve for valve in valve_leads_to.keys() if vfr[valve] != 0]
pathfinders = generate_pathfinders(
    non_zero_valves, shortest_paths, vfr, 500
)
pathfinders_with_elephants = generate_pathfinders(
    non_zero_valves, shortest_paths, vfr, 500, with_elephant=True
)
print(f'Part 1: {solve(pathfinders, shortest_paths, vfr)}')
print(f'Part 2: {solve(pathfinders_with_elephants, shortest_paths, vfr)}')
