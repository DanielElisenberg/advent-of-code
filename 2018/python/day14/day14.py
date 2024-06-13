def move_elf(elf_position, recipes):
    return (elf_position + int(recipes[elf_position]) + 1) % len(recipes)


def solution_one(elf_one, elf_two, recipes):
    while True:
        recipes += str(int(recipes[elf_one]) + int(recipes[elf_two]))
        elf_one = move_elf(elf_one, recipes)
        elf_two = move_elf(elf_two, recipes)
        if len(recipes) > 84611:
            return recipes[84601:84611]


def solution_two(elf_one, elf_two, recipes):
    while True:
        print(len(recipes))
        recipes += str(int(recipes[elf_one]) + int(recipes[elf_two]))
        elf_one = (elf_one + int(recipes[elf_one]) + 1) % len(recipes)
        elf_two = (elf_two + int(recipes[elf_two]) + 1) % len(recipes)
        if "084601" in recipes[len(recipes) - 6 :]:
            return len(recipes) - 6
        if "084601" in recipes[len(recipes) - 7 :]:
            return len(recipes) - 7


recipes = "37"
elf_one = 0
elf_two = 1


print(f"answer #1: {solution_one(elf_one, elf_two, recipes)}")
print(f"answer #2: {solution_two(elf_one, elf_two, recipes)}")
