from typing import Tuple, Callable


MAP_WIDTH = 139
MAP_HEIGHT = 137


def look_east(x: int, y: int) -> Tuple[int, int]:
    return ((x+1) % MAP_WIDTH, y)


def look_south(x: int, y: int) -> Tuple[int, int]:
    return (x, (y+1) % MAP_HEIGHT)


def move(cucumber_map: dict, character: str, look_forward: Callable) -> dict:
    after_move = {}
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if cucumber_map[(x, y)] == character:
                if cucumber_map[look_forward(x, y)] == '.':
                    after_move[(x, y)] = '.'
                    after_move[look_forward(x, y)] = character
                else:
                    after_move[(x, y)] = character
            else:
                if after_move.get((x, y), None) is None:
                    after_move[(x, y)] = cucumber_map[(x, y)]
    return after_move


if __name__ == "__main__":
    with open('day25/input') as input_file:
        lines = [line.strip() for line in input_file.readlines()]
        cucumber_map = {}
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                cucumber_map[(x, y)] = char

    counter = 0
    while True:
        counter += 1
        new_cucumber_map = move(cucumber_map, '>', look_east)
        new_cucumber_map = move(new_cucumber_map, 'v', look_south)
        if cucumber_map == new_cucumber_map:
            break
        else:
            cucumber_map = new_cucumber_map
    print(
        f"""Day 25:
        solution: {counter}"""
    )
