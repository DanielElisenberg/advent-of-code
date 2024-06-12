from copy import deepcopy

look_around = [
    (-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)
]


def occupied_seats(seat_map):
    return len(
        ['#' for state in seat_map.values() if state == '#']
    )


def adjacent_occupied_seats(seat_map, location):
    (x, y) = location
    adjecent_seat_states = [
        seat_map.get((x+look_x, y+look_y), 'L')
        for (look_x, look_y) in look_around
    ]
    return len(['#' for state in adjecent_seat_states if state == '#'])


def visible_occupied_seats(seat_map, location):
    (x, y) = location
    count = 0
    for (look_x, look_y) in look_around:
        visible_range = 0
        look_location_state = '.'
        while look_location_state == '.':
            visible_range += 1
            look_location_state = seat_map.get(
                (x+(look_x*visible_range), y+(look_y*visible_range)),
                'L'
            )
        count += 1 if look_location_state == '#' else 0
    return count


def first_rule(seat_map, location):
    occupied_adjecent = adjacent_occupied_seats(seat_map, location)
    if seat_map[location] == 'L' and occupied_adjecent == 0:
        return '#'
    elif seat_map[location] == '#' and occupied_adjecent >= 4:
        return 'L'
    else:
        return seat_map[location]


def second_rule(seat_map, location):
    visible_occupied = visible_occupied_seats(seat_map, location)
    if seat_map[location] == 'L' and visible_occupied == 0:
        return '#'
    elif seat_map[location] == '#' and visible_occupied >= 5:
        return 'L'
    else:
        return seat_map[location]


def stable_seat_map(initial_seat_map, rule):
    seat_map = deepcopy(initial_seat_map)
    while True:
        new_seat_map = deepcopy(seat_map)
        for location in seat_map.keys():
            new_seat_map[location] = rule(seat_map, location)
        if new_seat_map == seat_map:
            return new_seat_map
        else:
            seat_map = deepcopy(new_seat_map)


with open('day11/input.data') as input:
    rows = [line for line in input.read().split('\n')]
    seat_map = {}
    for y in range(len(rows)):
        for x in range(len(rows[y])):
            seat_map[(x, y)] = rows[y][x]

occupied = occupied_seats(
    stable_seat_map(seat_map, first_rule)
)
print(f'first solution: {occupied}')
occupied = occupied_seats(
    stable_seat_map(seat_map, second_rule)
)
print(f'second solution: {occupied}')
