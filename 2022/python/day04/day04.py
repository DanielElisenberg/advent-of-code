with open('day04/input', encoding='utf-8') as f:
    pairs = [
        (
            set(range(
                int(first_elf.split('-')[0]),
                int(first_elf.split('-')[1])+1
            )),
            set(range(
                int(second_elf.split('-')[0]),
                int(second_elf.split('-')[1])+1
            ))
        )
        for first_elf, second_elf in [
            line.strip().split(',') for line in f
        ]
    ]

complete_overlap_count = len([
    '' for first_elf, second_elf in pairs
    if (
        first_elf.issubset(second_elf)
        or second_elf.issubset(first_elf)
    )
])
print(f'Part 1: {complete_overlap_count}')

overlap_count = len([
    '' for first_elf, second_elf in pairs
    if len(first_elf.intersection(second_elf)) > 0
])
print(f'Part 2: {overlap_count}')
