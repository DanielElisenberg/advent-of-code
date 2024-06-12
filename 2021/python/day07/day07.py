if __name__ == "__main__":
    with open('day07/input') as input_file:
        crab_positions = [
            int(number) for number in input_file.read().split(",")
        ]

    fuel_usage_constant = []
    fuel_usage_summed = []

    for align_at in range(min(crab_positions), max(crab_positions) + 1):
        constant_fuel = 0
        summed_fuel = 0
        for crab_position in crab_positions:
            diff = abs(align_at - crab_position)
            constant_fuel += diff
            summed_fuel += diff * (diff + 1) // 2
        fuel_usage_constant.append(constant_fuel)
        fuel_usage_summed.append(summed_fuel)

    print(
        f"""Day 7:
        first solution: {min(fuel_usage_constant)}
        second solution: {min(fuel_usage_summed)}"""
    )
