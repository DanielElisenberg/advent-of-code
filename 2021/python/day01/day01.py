def increasing_measurements(depth_list: list) -> int:
    return sum([
        previous_depth < current_depth for previous_depth, current_depth
        in zip(depth_list, depth_list[1:])
    ])


if __name__ == '__main__':
    with open('day01/input') as input_file:
        depth_list = [int(line.strip('\n')) for line in input_file.readlines()]

    first_solution = increasing_measurements(depth_list)

    three_measurement_sliding_window = list(
        map(sum, zip(depth_list, depth_list[1:], depth_list[2:]))
    )
    second_solution = increasing_measurements(three_measurement_sliding_window)

    print(
        f"""day 1:
        first solution: {first_solution}
        second solution: {second_solution}"""
    )
