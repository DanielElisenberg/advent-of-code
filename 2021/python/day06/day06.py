from collections import defaultdict


def run_simulation(lanternfish: dict, generations: int) -> int:
    for _ in range(generations):
        next_generation = defaultdict(int)
        for internal_timer, amount in lanternfish.items():
            if internal_timer == 0:
                next_generation[6] += amount
                next_generation[8] += amount
            else:
                next_generation[internal_timer-1] += amount
        lanternfish = next_generation
    return sum(amount for amount in lanternfish.values())


if __name__ == "__main__":
    with open('day06/input') as input_file:
        fish_list = [
            int(internal_timer)
            for internal_timer in input_file.read().split(",")
        ]
    lanternfish = defaultdict(int)
    for internal_timer in fish_list:
        lanternfish[internal_timer] += 1

    print(
        f"""Day 6:
        first solution: {run_simulation(lanternfish, generations=80)}
        second solution: {run_simulation(lanternfish, generations=256)}"""
    )
