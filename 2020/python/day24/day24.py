from collections import defaultdict


walk = {
    'nw': (-0.5, 1),
    'ne': (0.5, 1),
    'e': (1, 0),
    'w': (-1, 0),
    'sw': (-0.5, -1),
    'se': (0.5, -1)
}


def flip_accordingly(tile_map):
    black_adjecent = defaultdict(int)
    for (x, y) in tile_map.keys():
        black_adjecent[(x, y)] += 0
        if tile_map[(x, y)] == 'black':
            for (walk_x, walk_y) in walk.values():
                black_adjecent[(x+walk_x, y+walk_y)] += 1

    for coords, count in black_adjecent.items():
        if count == 2:
            if coords in tile_map.keys():
                if tile_map[coords] == 'white':
                    tile_map[coords] = 'black'
            else:
                tile_map[coords] = 'black'
        elif count == 0 or count > 2:
            if coords in tile_map.keys():
                if tile_map[coords] == 'black':
                    tile_map[coords] = 'white'


with open('day24/input.data') as input:
    lines = input.read().split('\n')

tile_map = {}
for line in lines:
    (x, y)= (0, 0)
    i = 0
    while i < len(line):
        if line[i] in ['n', 's']:
            command = line[i:i+2]
            i += 2
        else:
            command = line[i]
            i += 1
        (walk_x, walk_y) = walk[command]
        x += walk_x
        y += walk_y
    if (x, y) in tile_map.keys():
        tile_map[(x,y)] = 'white' if tile_map[(x, y)] == 'black' else 'black'
    else:
        tile_map[(x, y)] = 'black'
black_tiles_count = len([1 for val in tile_map.values() if val == 'black'])
print(f'first solution: {black_tiles_count}')

for i in range(100):
    flip_accordingly(tile_map)
black_tiles_count = len([1 for val in tile_map.values() if val == 'black'])
print(f'second solution: {black_tiles_count}')
