class Point:
    def __init__(self, x, y, risk):
        self.x = x
        self.y = y
        self.risk = risk

    def __eq__(self, other) -> bool:
        return self.risk == other.risk

    def __lt__(self, other) -> bool:
        return self.risk < other.risk


def generate_extended_risk_map(risk_map: dict, map_size: int) -> dict:
    new_risk_map = {}
    for (x, y), risk in risk_map.items():
        for i in range(5):
            for j in range(5):
                new_risk = (risk + i + j) % 9
                new_risk_map[(i*map_size+x, j*map_size+y)] = (
                    new_risk if new_risk != 0 else 9
                )
    return new_risk_map


def pathfinding(risk_map: dict, map_size: int) -> int:
    explored_points = [Point(x=0, y=0, risk=0)]
    visited = set()

    while True:
        move_from = min(explored_points)
        visited.add((move_from.x, move_from.y))
        explored_points = [
            point for point in explored_points
            if (point.x, point.y) != (move_from.x, move_from.y)
        ]
        move_to = [
            (move_from.x+1, move_from.y),
            (move_from.x, move_from.y+1),
            (move_from.x-1, move_from.y),
            (move_from.x, move_from.y-1)
        ]
        move_to = [
            p for p in move_to
            if p not in visited and p in risk_map.keys()
        ]
        for (x, y) in move_to:
            if (x, y) == (map_size-1, map_size-1):
                return move_from.risk + risk_map[(x, y)]
            move_to_risk = move_from.risk + risk_map[(x, y)]
            explored_points.append(Point(x=x, y=y, risk=move_to_risk))


if __name__ == "__main__":
    with open('day15/input') as input_file:
        risk_grid = [
            [int(num) for num in line.strip()]
            for line in input_file.readlines()
        ]
        risk_map = {}
        for x in range(len(risk_grid)):
            for y in range(len(risk_grid)):
                risk_map[(x, y)] = risk_grid[y][x]
        bigger_risk_map = generate_extended_risk_map(risk_map, len(risk_grid))

    print(
        f"""Day 15:
        first solution: {pathfinding(risk_map, len(risk_grid))}
        second solution: {pathfinding(bigger_risk_map, len(risk_grid)*5)}"""
    )
