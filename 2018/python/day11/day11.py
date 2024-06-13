import numpy as np

grid_serial_number = 9306


def get_hundreds_digit(num):
    excess = int(num / 1000) * 1000
    return int((num - excess) / 100)


def get_power_level(x, y):
    rack_ID = x + 10
    power_level = rack_ID * y
    power_level += grid_serial_number
    power_level = power_level * rack_ID
    power_level = get_hundreds_digit(power_level)
    return power_level - 5


def map_powerlevels(powermap):
    for x in range(300):
        for y in range(300):
            powermap[y][x] = get_power_level(x + 1, y + 1)


def get_square_powerlevel(x, y, summed_area_table, square_size):
    total_power = summed_area_table[y + square_size - 1][x + square_size - 1]
    mask = 0
    if x > 1:
        mask += summed_area_table[y + square_size - 1][x - 1]
    if y > 1:
        mask += summed_area_table[y - 1][x + square_size - 1]
    if y > 1 and x > 1:
        mask -= summed_area_table[y - 1][x - 1]
    return total_power - mask


def largest_total_power(summed_area_table, square_size):
    max_power_level = -99999999
    max_coords = {}

    for x in range(300 - square_size):
        for y in range(300 - square_size):
            this_power_level = get_square_powerlevel(
                x, y, summed_area_table, square_size
            )
            if this_power_level > max_power_level:
                max_power_level = this_power_level
                max_coords = {"x": x + 1, "y": y + 1}
    return {"x": max_coords["x"], "y": max_coords["y"], "power_level": max_power_level}


def largest_total_power_any_size(summed_area_table):
    max_power_level = 0
    square_properties = {}
    for square_size in range(300):
        this_largest = largest_total_power(summed_area_table, square_size)
        if this_largest["power_level"] > max_power_level:
            max_power_level = this_largest["power_level"]
            square_properties = {
                "x": this_largest["x"],
                "y": this_largest["y"],
                "square_size": square_size,
            }
    return square_properties


powermap = np.zeros((300, 300))
map_powerlevels(powermap)
summed_area_table = powermap.cumsum(axis=0).cumsum(axis=1)

solution_one = largest_total_power(summed_area_table, 3)
print(f"solution one: {solution_one['x']},{solution_one['y']}")
solution_two = largest_total_power_any_size(summed_area_table)
print(
    f"solution two: {solution_two['x']},{solution_two['y']},{solution_two['square_size']}"
)
