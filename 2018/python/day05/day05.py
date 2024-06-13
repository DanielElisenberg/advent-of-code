def swap_case(c):
    if c.islower():
        return c.upper()
    if c.isupper():
        return c.lower()


def trigger_reactions(polymer):
    polymer_length = len(polymer)
    i = 0
    while i < polymer_length - 1:
        if polymer[i] == swap_case(polymer[i + 1]):
            polymer = polymer[:i] + polymer[i + 2 :]
            i -= 1
            polymer_length -= 2
        else:
            i += 1
    return len(polymer)


def shortest_stripped_polymer(polymer):
    unit_list = list(set(polymer.lower()))
    polymer_lengths = []

    for unit in unit_list:
        stripped_polymer = polymer.replace(unit, "").replace(unit.upper(), "")
        polymer_lengths.append(trigger_reactions(stripped_polymer))
    return min(polymer_lengths)


input = open("day05/input", "r")
polymer = input.readlines()[0].strip("\n")

print(f"answer #1: {trigger_reactions(polymer)}")
print(f"answer #1: {shortest_stripped_polymer(polymer)}")
