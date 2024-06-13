from collections import defaultdict


def sum_pot_keys(state_map):
    summed = 0
    for key, value in state_map.items():
        if value == "#":
            summed += key
    return summed


def print_state(state_map):
    plant_indices = [key for key, val in state_map.items() if val == "#"]
    start = min(plant_indices) - 2
    until = max(plant_indices) + 3

    state = ""
    for i in range(start, until):
        state += state_map[i]
    print(f"{start}-{until}")
    print(state)


def read_rules(lines):
    rules = {}

    for i in range(2, len(lines)):
        rule = lines[i].strip("\n")
        state = rule.split(" => ")[0]
        outcome = rule.split(" => ")[1]
        rules[state] = outcome
    return rules


def solution_one(state_map, rules):
    for gen in range(20):
        plant_indices = [key for key, val in state_map.items() if val == "#"]
        start = min(plant_indices) - 2
        until = max(plant_indices) + 3
        new_state = defaultdict(lambda: ".")

        for i in range(start, until):
            local_state = "".join(state_map[x] for x in range(i - 2, i + 3))
            new_state[i] = rules[local_state]
        state_map = new_state

    return sum_pot_keys(state_map)


def solution_two(state_map, rules):
    last_growth = 0
    last_sum = sum_pot_keys(state_map)
    stagnation_point = 0

    for gen in range(50000000000):
        plant_indices = [key for key, val in state_map.items() if val == "#"]
        start = min(plant_indices) - 2
        until = max(plant_indices) + 3
        new_state = defaultdict(lambda: ".")

        for i in range(start, until):
            local_state = "".join(state_map[x] for x in range(i - 2, i + 3))
            new_state[i] = rules[local_state]
        state_map = new_state

        growth = sum_pot_keys(state_map) - last_sum
        last_sum = sum_pot_keys(state_map)
        if growth == last_growth:
            stagnation_point = gen + 1
            break
        last_growth = growth

    return ((50000000000 - stagnation_point) * last_growth) + last_sum


input = open("day12/input", "r")
lines = input.readlines()

state_list = list(lines[0].split(" ")[2].strip("\n"))
state_map = defaultdict(lambda: ".")
for i in range(len(state_list)):
    state_map[i] = state_list[i]

rules = read_rules(lines)

# print(f"{solution_one(state_map, rules)}")
print(f"{solution_two(state_map, rules)}")
