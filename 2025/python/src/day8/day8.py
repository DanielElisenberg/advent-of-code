import math
from dataclasses import dataclass


@dataclass
class JunctionBox:
    x: int
    y: int
    z: int

    def distance_to(self, other: "JunctionBox") -> float:
        return math.dist((self.x, self.y, self.z), (other.x, other.y, other.z))


@dataclass
class Connection:
    ids: list[int]
    distance: float


@dataclass
class Circuits:
    data: list[set[int]]

    @staticmethod
    def from_connections(connections: list[Connection]) -> "Circuits":
        circuits = Circuits(data=[])
        for connection in connections:
            circuits.include(connection)
        circuits.data.sort(key=lambda x: -len(x))
        return circuits

    def _get_connected_circuits(self, ids: list[int]) -> list[int]:
        connected_circuits = [
            next(
                (
                    circuit_index
                    for circuit_index, circuit in enumerate(self.data)
                    if id in circuit
                ),
                None,
            )
            for id in ids
        ]
        return sorted(
                set(
                    circuit_index
                    for circuit_index in connected_circuits
                    if circuit_index is not None
                )
        )

    def include(self, connection: Connection) -> "Circuits":
        connected_circuits = self._get_connected_circuits(connection.ids)
        match connected_circuits:
            case []:
                self.data.append(set(connection.ids))
            case [i]:
                self.data[i] = self.data[i].union(connection.ids)
            case [i, j]:
                circuit_two = self.data.pop(j)
                circuit_one = self.data.pop(i)
                self.data.append(circuit_one.union(circuit_two))
            case _:
                raise RuntimeError("More than 3 circuits connects to the same ids.")
        self.data.sort(key=lambda x: -len(x))
        return self


def read_junction_boxes() -> list[JunctionBox]:
    with open("src/day8/input") as f:
        return [
            JunctionBox(int(x), int(y), int(z))
            for x, y, z in [line.strip().split(",") for line in f.readlines()]
        ]


def generate_possile_connections(
    junction_boxes: list[JunctionBox],
) -> list[Connection]:
    possible_connections = []
    for i in range(len(junction_boxes)):
        for j in range(i + 1, len(junction_boxes)):
            possible_connections.append(
                Connection(
                    distance=junction_boxes[i].distance_to(junction_boxes[j]),
                    ids=[i, j],
                )
            )
    return sorted(possible_connections, key=lambda x: x.distance)


def solve_part_one() -> int:
    possible_connections = generate_possile_connections(read_junction_boxes())
    circuits = Circuits.from_connections(possible_connections[:1000])
    return len(circuits.data[0]) * len(circuits.data[1]) * len(circuits.data[2])


def solve_part_two() -> int:
    junction_boxes = read_junction_boxes()
    possible_connections = generate_possile_connections(junction_boxes)
    circuits = Circuits(data=[])
    for connection in possible_connections:
        circuits.include(connection)
        if len(circuits.data[0]) >= len(junction_boxes):
            return (
                junction_boxes[connection.ids[0]].x
                * junction_boxes[connection.ids[1]].x
            )
    raise RuntimeError("Connections never merged into a single circuit.")


def solve():
    print("Part 1: ", solve_part_one())
    print("Part 2: ", solve_part_two())


if __name__ == "__main__":
    solve()
