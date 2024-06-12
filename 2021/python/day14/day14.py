from collections import defaultdict


def do_pair_insertion(template: str, insertion_rules: dict,
                      steps: int) -> int:
    template_pairs = defaultdict(int)
    for index in range(len(template)-1):
        template_pairs[template[index:index+2]] = 1

    for _ in range(steps):
        new_template_pairs = defaultdict(int)
        for pair, occurences in template_pairs.items():
            to_insert = insertion_rules[pair]
            new_template_pairs[pair[0] + to_insert] += occurences
            new_template_pairs[to_insert + pair[1]] += occurences
        template_pairs = new_template_pairs

    character_count = defaultdict(int)
    character_count[template[-1]] += 1
    for pair, occurences in template_pairs.items():
        character_count[pair[0]] += occurences

    counts = [count for count in character_count.values()]
    return max(counts) - min(counts)


if __name__ == "__main__":
    with open('day14/input') as input_file:
        input = [line.strip() for line in input_file.readlines()]
        template = input[0]
        insertion_rules = {
            adjacent: insert for (adjacent, insert) in
            [rule.split(" -> ") for rule in input[2:]]
        }

    first_solution = do_pair_insertion(template, insertion_rules, steps=10)
    second_solution = do_pair_insertion(template, insertion_rules, steps=40)

    print(
        f"""Day 14:
        first solution: {first_solution}
        second solution: {second_solution}"""
    )
