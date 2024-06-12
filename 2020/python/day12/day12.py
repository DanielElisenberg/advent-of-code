from collections import deque


move = {
    'E': lambda amount, x, y: (x+amount, y),
    'W': lambda amount, x, y: (x-amount, y),
    'N': lambda amount, x, y: (x, y+amount),
    'S': lambda amount, x, y: (x, y-amount)
}
rotate = {
    90: lambda x, y: (y, -x),
    180: lambda x, y: (-x, -y),
    270: lambda x, y: (-y, x)
}


def turn(current_direction, angle):
    directions = deque(['N', 'E', 'S', 'W'])
    directions.rotate(-directions.index(current_direction)-int(angle/90))
    return directions[0]


def move_ship_with_commands(commands):
    (x, y) = (0, 0)
    direction = 'E'
    for (instruction, parameter) in commands:
        if instruction == 'R':
            direction = turn(direction, parameter)
        else:
            move_direction = direction if instruction == 'F' else instruction
            (x, y) = move[move_direction](parameter, x, y)
    return abs(x) + abs(y)


def move_ship_with_waypoint(commands):
    (x, y) = (0, 0)
    (waypoint_x, waypoint_y) = (10, 1)
    for (instruction, parameter) in commands:
        if instruction == 'R':
            (waypoint_x, waypoint_y) = (
                rotate[parameter](waypoint_x, waypoint_y)
            )
        elif instruction == 'F':
            (x, y) = (x+waypoint_x*parameter, y+waypoint_y*parameter)
        else:
            (waypoint_x, waypoint_y) = (
                move[instruction](parameter, waypoint_x, waypoint_y)
            )
    return abs(x) + abs(y)


with open('day12/input.data') as input:
    commands = [(line[0], int(line[1:])) for line in input.read().split('\n')]
    for (instruction, parameter) in commands:
        if instruction == 'L':
            index = commands.index((instruction, parameter))
            commands[index] = ('R', 360 - parameter)

print(f'first solution: {move_ship_with_commands(commands)}')
print(f'second solution: {move_ship_with_waypoint(commands)}')
