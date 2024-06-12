from collections import defaultdict


def safe_ingredients_occurence(contains, all_ingredients):
    ingredients_with_allergens = []
    for ingredient in contains.values():
        [ingredient] = ingredient
        ingredients_with_allergens.append(ingredient)

    ingredients_without_allergen = [
        ingredient for ingredient in set(all_ingredients)
        if ingredient not in ingredients_with_allergens
    ]
    count = 0
    for ingredient in ingredients_without_allergen:
        count += len(
            [occurence for occurence in all_ingredients if occurence == ingredient]
        )
    return count


def dangerous_ingredients_list(contains):
    sorted_allergens = list(contains.keys())
    sorted_allergens.sort()
    dangerous_ingredients_list = ''
    for allergen in sorted_allergens:
        [ingredient] = contains[allergen]
        dangerous_ingredients_list += f'{ingredient},'
    return dangerous_ingredients_list[:-1]


def parse_ingredients_and_allergens(lines):
    contains = defaultdict(list)
    all_ingredients = []

    for line in lines:
        (ingredients, allergens) = line.split(' (contains ')
        ingredients = ingredients.split(' ')
        allergens = allergens[:-1].split(', ')

        [all_ingredients.append(ingredient) for ingredient in ingredients]
        for allergen in allergens:
            if not contains[allergen]:
                [contains[allergen].append(ingredient)
                for ingredient in ingredients]
            else:
                contains[allergen] = [ingredient for ingredient in ingredients
                                    if ingredient in contains[allergen]]
                if len(contains[allergen]) == 1:
                    for a, i in contains.items():
                        if a != allergen:
                            while contains[allergen][0] in i:
                                i.remove(contains[allergen][0])
    return contains, all_ingredients


with open('day21/input.data') as input:
    lines = [line for line in input.read().split('\n')]

contains, all_ingredients = parse_ingredients_and_allergens(lines)
count = safe_ingredients_occurence(contains, all_ingredients)
print(f'first solution: {count}')
print(f'second solution: {dangerous_ingredients_list(contains)}')
