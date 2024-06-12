from collections import defaultdict


def look_coords_3D():
    look_coords = []
    for look_x in [-1, 0, 1]:
        for look_y in [-1, 0, 1]:
            for look_z in [-1, 0, 1]:
                look_coords.append((look_x, look_y, look_z))
    look_coords.remove((0, 0, 0))
    return look_coords


def look_coords_4D():
    look_coords = []
    for look_x in [-1, 0, 1]:
        for look_y in [-1, 0, 1]:
            for look_z in [-1, 0, 1]:
                for look_w in [-1, 0, 1]:
                    look_coords.append((look_x, look_y, look_z, look_w))
    look_coords.remove((0, 0, 0, 0))
    return look_coords


def search_3D_area(pocket_dimension):
    x_values = [x for (x, y, z) in pocket_dimension.keys()]
    y_values = [y for (x, y, z) in pocket_dimension.keys()]
    z_values = [z for (x, y, z) in pocket_dimension.keys()]
    search_coords = []
    for x in range(min(x_values)-1, max(x_values)+2):
        for y in range(min(y_values)-1, max(y_values)+2):
            for z in range(min(z_values)-1, max(z_values)+2):
                search_coords.append((x, y, z))
    return search_coords


def search_4D_area(pocket_dimension):
    x_values = [x for (x, y, z, w) in pocket_dimension.keys()]
    y_values = [y for (x, y, z, w) in pocket_dimension.keys()]
    z_values = [z for (x, y, z, w) in pocket_dimension.keys()]
    w_values = [w for (x, y, z, w) in pocket_dimension.keys()]
    search_coords = []
    for x in range(min(x_values)-1, max(x_values)+2):
        for y in range(min(y_values)-1, max(y_values)+2):
            for z in range(min(z_values)-1, max(z_values)+2):
                for w in range(min(w_values)-1, max(w_values)+2):
                    search_coords.append((x, y, z, w))
    return search_coords


def run_boot_process_3D(pocket_dimension):
    look_coords = look_coords_3D()
    for i in range(6):
        new_pocket_dimension = defaultdict(int)
        search_coords = search_3D_area(pocket_dimension)
        for coord in search_coords:
            (x, y, z) = coord
            state = pocket_dimension[coord]

            active_count = 0
            for look_coord in look_coords:
                (look_x, look_y, look_z) = look_coord
                active_count += (
                    pocket_dimension[(x+look_x), (y+look_y), (z+look_z)]
                )

            if state == 0 and active_count == 3:
                new_pocket_dimension[coord] = 1
            elif state == 1 and (active_count == 2 or active_count == 3):
                new_pocket_dimension[coord] = 1
            else:
                new_pocket_dimension[coord] = 0

        for k, v in new_pocket_dimension.items():
            pocket_dimension[k] = v
    return sum(pocket_dimension.values())


def run_boot_process_4D(pocket_dimension):
    look_coords = look_coords_4D()
    for i in range(6):
        new_pocket_dimension = defaultdict(int)
        search_coords = search_4D_area(pocket_dimension)
        for coord in search_coords:
            (x, y, z, w) = coord
            state = pocket_dimension[coord]

            active_count = 0
            for look_coord in look_coords:
                (look_x, look_y, look_z, look_w) = look_coord
                active_count += (
                    pocket_dimension[
                        (x+look_x), (y+look_y), (z+look_z), (w+look_w)
                    ]
                )

            if state == 0 and active_count == 3:
                new_pocket_dimension[coord] = 1
            elif state == 1 and (active_count == 2 or active_count == 3):
                new_pocket_dimension[coord] = 1
            else:
                new_pocket_dimension[coord] = 0

        for k, v in new_pocket_dimension.items():
            pocket_dimension[k] = v
    return sum(pocket_dimension.values())
