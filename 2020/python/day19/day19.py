import itertools


def resolve(rule_map, key):
    if key == 'a' or key == 'b':
        return [key]
    rules = rule_map[int(key)]
    all_inner = []
    for rule in rules:
        inner = []
        for inner_rule in rule:
            inner.append(resolve(rule_map, inner_rule))
        inner = [''.join(s) for s in itertools.product(*inner)]
        all_inner += inner
    return all_inner


def parse_rules(rules):
    rule_map = {}
    for rule in rules:
        [rule_number, rule] = rule.split(': ')
        if '"' in rule:
            rule = [rule[1]]
        else:
            done_rule = []
            or_rules = rule.split(' | ')
            for or_rule in or_rules:
                done_rule.append(or_rule.split(' '))
            rule = done_rule
        rule_map[int(rule_number)] = rule
    return rule_map


def validate_recursive(rule_map, messages):
    def find_rule_in_message(rules, message, found):
        for rule in rules:
            if message[:len(rule)] == rule:
                return find_rule_in_message(
                    rules, message[len(rule):], found+1
                )
        return message, found

    def is_valid(first_rule_count, second_rule_count, message):
        return (
            (second_rule_count > 1 or first_rule_count > 2) and
            second_rule_count > 0 and first_rule_count > second_rule_count
            and message == ''
        )

    first_rules = resolve(rule_map, 42)
    second_rules = resolve(rule_map, 31)
    total_valid = 0
    for message in messages:
        message, first_rule_count = find_rule_in_message(
            first_rules, message, 0
        )
        message, second_rule_count = find_rule_in_message(
            second_rules, message, 0
        )
        if is_valid(first_rule_count, second_rule_count, message):
            total_valid += 1
    return total_valid


def valid_messages(messages, rule_map):
    valid_messages = [message for message in messages if message in rules]
    return len(valid_messages)


with open('day19/input.data') as input:
    [rules, messages] = input.read().split('\n\n')

rule_map = parse_rules(rules.split('\n'))
rules = resolve(rule_map, 0)
valid_count = valid_messages(messages.split('\n'), rules)
print(f'first solution: {valid_count}')

valid_recursive_count = validate_recursive(rule_map, messages.split('\n'))
print(f'second solution: {valid_count + valid_recursive_count}')
