def generate_list_of_steps(lines):
    list_of_steps = []
    for line in lines:
        list_of_steps.append(line.split(" ")[1])
        list_of_steps.append(line.split(" ")[7])
    return list(set(list_of_steps))


def generate_dependencies(dependencies, lines):
    for line in lines:
        dependencies[line.split(" ")[7]].append(line.split(" ")[1])

    for k, v in dependencies.items():
        dependencies[k] = list(set(v))
    return dependencies


def get_available_steps(dependencies):
    available_steps = []

    for k, v in dependencies.items():
        if len(v) == 0:
            available_steps.append(k)
    return available_steps


def process_instructions(dependencies, amount_of_steps):
    instruction_list = ""
    while len(instruction_list) < amount_of_steps:
        available_steps = get_available_steps(dependencies)
        next_step = sorted(available_steps)[0]

        for _, v in dependencies.items():
            if next_step in v:
                v.remove(next_step)
        dependencies.pop(next_step)

        instruction_list += next_step
    return instruction_list


def problem_one(list_of_steps):
    amount_of_steps = len(list_of_steps)

    dependencies = {k: [] for k in list_of_steps}
    dependencies = generate_dependencies(dependencies, lines)
    instructions = process_instructions(dependencies, amount_of_steps)
    print(f"answer #1: {instructions}")


def problem_two(list_of_steps):
    amount_of_steps = len(list_of_steps)
    instruction_list = ""
    dependencies = {k: [] for k in list_of_steps}
    dependencies = generate_dependencies(dependencies, lines)

    while len(instruction_list) < amount_of_steps:
        available_steps = sorted(get_available_steps(dependencies))


input = open("day07/input", "r")
lines = input.readlines()
list_of_steps = generate_list_of_steps(lines)

problem_one(list_of_steps)
problem_two(list_of_steps)
