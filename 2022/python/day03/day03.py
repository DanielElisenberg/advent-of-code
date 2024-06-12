import string


CHARACTERS = string.ascii_lowercase + string.ascii_uppercase
numeric_value_of = {
    character: index + 1 for index, character in enumerate(CHARACTERS)
}


with open('day03/input', encoding='utf-8') as f:
    rucksacks = [line.strip() for line in f]
    rucksack_compartments = [
        (
            set(line[:int(len(line)/2)]),
            set(line[int(len(line)/2):])
        )
        for line in rucksacks
    ]
    misplaced_items = sum([
        numeric_value_of[c1.intersection(c2).pop()]
        for c1, c2 in rucksack_compartments
    ])
    print(f'Part 1: {misplaced_items}')

    badges = sum([
        numeric_value_of[
            (
                set(rucksack)
                .intersection(rucksacks[index+1], rucksacks[index+2])
                .pop()
            )
        ]
        for index, rucksack in enumerate(rucksacks)
        if index % 3 == 0
    ])
    print(f'Part 2: {badges}')
