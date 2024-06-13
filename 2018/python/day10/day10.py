def get_size(min_x, max_x, min_y, max_y):
    return (max_y - min_y) * (max_x - min_x)


def converge_at(points):
    convergance_time = 0
    min_size = 99999999999999

    for time in range(100000):
        min_y = 1000000
        min_x = 1000000
        max_y = 0
        max_x = 0
        for point in points:
            this_x = point[0] + (point[2] * time)
            this_y = point[1] + (point[3] * time)
            if this_y < min_y:
                min_y = this_y
            if this_y > max_y:
                max_y = this_y
            if this_x < min_x:
                min_x = this_x
            if this_x > max_x:
                max_x = this_x
        this_size = get_size(min_x, max_x, min_y, max_y)
        if this_size < min_size:
            min_size = this_size
            convergance_time = time
    return convergance_time


def move_time(points, time):
    points_after = []
    for point in points:
        this_x = point[0] + (point[2] * convergance_time)
        this_y = point[1] + (point[3] * convergance_time)
        points_after.append((this_x, this_y))
    return points_after


input = open("day10/input", "r")
data = input.readlines()
points = []

for line in data:
    stripped_line = line.strip("position=<").strip(">\n")
    formatted_line = stripped_line.replace("> velocity=<", ", ")
    point_data = formatted_line.split(",")
    points.append(
        (
            int(int(point_data[0])),
            int(int(point_data[1])),
            int(int(point_data[2])),
            int(int(point_data[3])),
        )
    )

convergance_time = converge_at(points)
converging_points = move_time(points, convergance_time)

min_y = 1000000
min_x = 1000000
max_y = 0
max_x = 0
for point in converging_points:
    this_x = point[0]
    this_y = point[1]
    if this_y < min_y:
        min_y = this_y
    if this_y > max_y:
        max_y = this_y
    if this_x < min_x:
        min_x = this_x
    if this_x > max_x:
        max_x = this_x

draw_grid = [["."] * 62] * 11
list_for_print = []
for point in converging_points:
    list_for_print.append((point[0] - min_x, point[1] - min_y))
    draw_grid[point[0] - min_x][point[1] - min_y] = "#"

list_for_print.sort()
print(list_for_print)
for row in draw_grid:
    print("".join(row))
