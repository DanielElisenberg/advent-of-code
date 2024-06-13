metadata_sum = 0


def solution_one(data, i):
    amount_of_children = int(data[i])
    amount_of_metadata = int(data[i + 1])
    i += 2

    for _ in range(amount_of_children):
        i = solution_one(data, i)
    for _ in range(amount_of_metadata):
        global metadata_sum
        metadata_sum += int(data[i])
        i += 1

    return i


def solution_two(data, i):
    amount_of_children = int(data[i])
    amount_of_metadata = int(data[i + 1])
    i += 2
    this_value = 0
    child_values = []

    if amount_of_children > 0:
        for _ in range(amount_of_children):
            child_value, i = solution_two(data, i)
            child_values.append(child_value)
        for _ in range(amount_of_metadata):
            meta = int(data[i])
            try:
                this_value += child_values[meta - 1]
            except Exception:
                pass
            i += 1
    else:
        for _ in range(amount_of_metadata):
            this_value += int(data[i])
            i += 1
    return this_value, i


input = open("day08/input", "r")
data = input.readlines()[0].split(" ")

solution_one(data, 0)
print(f"answer #1: {metadata_sum}")
num, _ = solution_two(data, 0)
print(f"answer #2: {num}")
