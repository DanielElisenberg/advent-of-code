class Tile:
    def __init__(self, tilestring):
        tilestring = tilestring.split('\n')
        self.id = int(tilestring[0][5:-1])
        self.tiledata = []
        for i in range(1, 11):
            self.tiledata.append(list(tilestring[i]))

    def rotate(self):
        self.tiledata = [list(row) for row in zip(*reversed(self.tiledata))]

    def flip(self):
        self.tiledata = [list(reversed(row)) for row in self.tiledata]

    def get_edge(self, direction):
        if direction == 'north':
            return self.tiledata[0]
        elif direction == 'south':
            return self.tiledata[9]
        elif direction == 'east':
            return [row[9] for row in self.tiledata]
        elif direction == 'west':
            return [row[0] for row in self.tiledata]
        else:
            raise ValueError(f'Invalid direction: {direction}')


def add_search_locations(locations, coord):
    (x, y) = coord
    for search in [-1, 1]:
        if (x+search, y) not in locations:
            locations.append((x+search, y))
        if (x, y+search) not in locations:
            locations.append((x, y+search))


def match(tile, matchers):
    if matchers['north_tile'] is not None:
        tile_edge = tile.get_edge('north')
        match_edge = matchers['north_tile'].get_edge('south')
        if tile_edge != match_edge:
            return False
    if matchers['south_tile'] is not None:
        tile_edge = tile.get_edge('south')
        match_edge = matchers['south_tile'].get_edge('north')
        if tile_edge != match_edge:
            return False
    if matchers['west_tile'] is not None:
        tile_edge = tile.get_edge('west')
        match_edge = matchers['west_tile'].get_edge('east')
        if tile_edge != match_edge:
            return False
    if matchers['east_tile'] is not None:
        tile_edge = tile.get_edge('east')
        match_edge = matchers['east_tile'].get_edge('west')
        if tile_edge != match_edge:
            return False
    return True


def place_tile(coord, placed_tiles, unplaced_tiles):
    (x, y) = coord
    matchers = {
        'north_tile': placed_tiles.get((x, y+1), None),
        'south_tile': placed_tiles.get((x, y-1), None),
        'west_tile': placed_tiles.get((x-1, y), None),
        'east_tile': placed_tiles.get((x+1, y), None)
    }
    for tile in unplaced_tiles:
        for i in range(2):
            tile.flip()
            for i in range(4):
                tile.rotate()
                if match(tile, matchers):
                    placed_tiles[(coord)] = tile
                    unplaced_tiles.remove(tile)
                    return True
    return False


def find_corners(placed_tiles):
    (min_x, max_x, min_y, max_y) = (1, -1, 1, -1)
    for coord in placed_tiles.keys():
        (x, y) = coord
        max_x = x if x > max_x else max_x
        max_y = y if y > max_y else max_y
        min_x = x if x < min_x else min_x
        min_y = y if y < min_y else min_y
    return (min_x, max_x, min_y, max_y)


def multiply_corners(placed_tiles):
    (min_x, max_x, min_y, max_y) = find_corners(placed_tiles)
    return (
        placed_tiles[(min_x, min_y)].id *
        placed_tiles[(min_x, max_y)].id *
        placed_tiles[(max_x, max_y)].id *
        placed_tiles[(max_x, min_y)].id
    )


def combine_image(placed_tiles):
    (min_x, max_x, min_y, max_y) = find_corners(placed_tiles)
    full_image = []
    for y in reversed(range(min_y, max_y+1)):
        rows = [[] for _ in range(8)]
        for x in range(min_x, max_x+1):
            for i in range(1,9):
                rows[i-1] += placed_tiles[(x, y)].tiledata[i][1:9]
        full_image += rows
    return full_image


def find_sea_monsters(full_image):
    sea_monsters_found = 0
    for flips in range(2):
        full_image = [list(reversed(row)) for row in full_image]
        for rotate in range(4):
            full_image = [list(row) for row in zip(*reversed(full_image))]
            for y in range(len(full_image)-2):
                for x in range(len(full_image[y])-19):
                    sea_monster = [
                        full_image[y][x+18],
                        full_image[y+1][x],
                        full_image[y+1][x+5],
                        full_image[y+1][x+6],
                        full_image[y+1][x+11],
                        full_image[y+1][x+12],
                        full_image[y+1][x+17],
                        full_image[y+1][x+18],
                        full_image[y+1][x+19],
                        full_image[y+2][x+1],
                        full_image[y+2][x+4],
                        full_image[y+2][x+7],
                        full_image[y+2][x+10],
                        full_image[y+2][x+13],
                        full_image[y+2][x+16]
                    ]
                    if all([True if c == '#' else False for c in sea_monster]):
                        sea_monsters_found += 1
            if sea_monsters_found > 0:
                return sea_monsters_found


def count_water(full_image):
    return len([water for row in full_image for water in row if water == '#'])


def place_all_tiles(unplaced_tiles):
    placed_tiles = {}
    placed_tiles[(0, 0)] = unplaced_tiles[0]
    unplaced_tiles.remove(unplaced_tiles[0])
    search_locations = []
    add_search_locations(search_locations, (0, 0))

    while unplaced_tiles:
        search_at = search_locations.pop()
        if place_tile(search_at, placed_tiles, unplaced_tiles):
            add_search_locations(search_locations, search_at)
    return placed_tiles


with open('day20/input.data') as input:
    tiles = [tile for tile in input.read().split('\n\n')]
    unplaced_tiles = [Tile(tiledata) for tiledata in tiles]

placed_tiles = place_all_tiles(unplaced_tiles)
print(f'first solution: {multiply_corners(placed_tiles)}')

full_image = combine_image(placed_tiles)
found_sea_monsters = find_sea_monsters(full_image)
water = count_water(full_image)
print(f'second solution: {water-(found_sea_monsters*15)}')