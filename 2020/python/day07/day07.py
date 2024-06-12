import re


def contains_gold(bag_info, bag):
    if bag == 'shiny gold bags':
        return True
    return any(
        [contains_gold(bag_info, sub_bag["bag_name"])
         for sub_bag in bag_info[bag]]
    )


def bags_to_buy(bag_rules, bag_name):
    contains = bag_rules[bag_name]
    if contains == []:
        return 0
    return sum(
        [(sub_bag["amount"] +
         (sub_bag["amount"] *
          bags_to_buy(bag_rules, sub_bag["bag_name"])))
         for sub_bag in contains]
    )


def bag_rules_from_file():
    def bag_rule_from_line(line):
        [bag_name, contains] = line.split(' contain ')
        contains = re.sub('(<=[1-9])( )|(, )', ':', contains).split(':')
        if contains == ['no other bags']:
            return {bag_name: []}
        return {
            bag_name: [{
                "bag_name": (
                    sub_bag[2:]+'s' if sub_bag[-1] != 's' else sub_bag[2:]
                ),
                "amount": int(sub_bag[:1])
            } for sub_bag in contains]
        }

    with open('day07/input.data') as input:
        lines = [line for line in input.read().split('.\n')]

    bag_rules = {}
    for line in lines:
        bag_rules.update(bag_rule_from_line(line))
    return bag_rules


bag_rules = bag_rules_from_file()
first_solution = sum(
    [1 for bag_name in bag_rules.keys() if contains_gold(bag_rules, bag_name)]
)-1
second_solution = bags_to_buy(bag_rules, "shiny gold bags")

print(f'first solution: {first_solution}')
print(f'second solution: {second_solution}')
