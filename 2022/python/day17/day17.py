import json
from copy import copy
from collections import deque
from itertools import chain


class Rock:
    shape: list[tuple[int, int]]

    def __init__(self, shape: list[list[str]], tower_height: int):
        self.shape = []
        y_transform = tower_height + 4
        x_transform = 3
        self.shape = chain(*[
            [
                (x + x_transform, y + y_transform)
                for x, char in enumerate(row) if char == '#'
            ]
            for y, row in enumerate(reversed(shape))
        ])

    def push(
        self, wind: int, collision_map: dict[tuple[int, int], str]
    ) -> None:
        new_shape = [(x+wind, y) for x, y in self.shape]
        collides = (
            any([coordinate in collision_map for coordinate in new_shape])
            or any([x in [8, 0] for x, _ in new_shape])
        )
        self.shape = new_shape if not collides else self.shape

    def fall(self, collision_map: dict[tuple[int, int], str]) -> bool:
        new_shape = [(x, y-1) for x, y in self.shape]
        collides = (
            any([coordinate in collision_map for coordinate in new_shape])
            or any([y == 0 for x, y in new_shape])
        )
        if not collides:
            self.shape = new_shape
            return True
        return False


def generate_drop_state(
    rock_shape_name: str,
    winds: deque[int],
    tower_height: int,
    collision_map: dict[tuple[int, int], str],
) -> str:
    deque_state_string = ''.join(
        [str(winds[i]) for i in range(0, len(winds))]
    )
    collision_string = ''
    for y in range(tower_height-15, tower_height):
        for x in range(0, 8):
            collision_string += collision_map.get((x, y), '.')
    return f'{rock_shape_name}{collision_string}{deque_state_string}'


def resolve_repetitions(
    drop_state: str,
    drop_states: dict[str, tuple[int, int]],
    rock_number: int,
    tower_height: int,
    amount: int
) -> int:
    last_occurence, last_highest = drop_states[drop_state]
    repeat_length = rock_number - last_occurence
    remaining_rocks = amount - last_occurence
    overflow = remaining_rocks % repeat_length
    repeat_amount = (remaining_rocks - overflow) // repeat_length
    overflow = remaining_rocks % repeat_length
    height_at_overflow = next(
        score for turn, score in drop_states.values()
        if turn == last_occurence + overflow + 1
    )
    repeat_growth = tower_height - last_highest
    tower_height = (
        height_at_overflow + repeat_growth * (repeat_amount)
    )
    return tower_height


def stack_tower(
    winds: deque[int], rock_shapes: deque[dict], amount: int
) -> int:
    collision_map = {}
    drop_states = {}
    tower_height = 0
    rock_number = 1

    while rock_number <= amount:
        rock = Rock(rock_shapes[0]['shape'], tower_height)
        rock_shapes.rotate()
        drop_state = generate_drop_state(
            rock_shapes[0]['name'], winds, tower_height, collision_map
        )
        if drop_state in drop_states:
            return resolve_repetitions(
                drop_state, drop_states, rock_number, tower_height, amount
            )

        falling = True
        while falling:
            rock.push(winds[0], collision_map)
            winds.rotate()
            if not rock.fall(collision_map):
                drop_states[drop_state] = (rock_number, tower_height)
                highest_rock_point = max([y for _, y in rock.shape])
                tower_height = (
                    highest_rock_point if tower_height < highest_rock_point
                    else tower_height
                )
                for coordinate in rock.shape:
                    collision_map[coordinate] = '#'
                rock_number += 1
                break


with open('day17/input', encoding='utf-8') as f:
    winds = deque(reversed(
        [1 if char == '>' else -1 for char in f.readline()]
    ))
    winds.rotate()
with open('day17/rocks.json', encoding='utf-8') as f:
    rock_shapes = deque(json.load(f))

print(f'Part 1: {stack_tower(copy(winds), copy(rock_shapes), 2022)}')
print(f'Part 2: {stack_tower(copy(winds), copy(rock_shapes), 1000000000000)}')
