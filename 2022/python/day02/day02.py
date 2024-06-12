rules = {
    'A X': 3 + 1,
    'B Y': 3 + 2,
    'C Z': 3 + 3,
    'A Y': 6 + 2,
    'A Z': 0 + 3,
    'B X': 0 + 1,
    'B Z': 6 + 3,
    'C X': 6 + 1,
    'C Y': 0 + 2
}

new_rules = {
    'A X': 0 + 3,
    'B Y': 3 + 2,
    'C Z': 6 + 1,
    'A Y': 3 + 1,
    'A Z': 6 + 2,
    'B X': 0 + 1,
    'B Z': 6 + 3,
    'C X': 0 + 2,
    'C Y': 3 + 3
}

with open('day02/input', encoding='utf-8') as f:
    strategy_guide = [line.strip() for line in f]
score = sum([rules[row] for row in strategy_guide])
print(f'Part 1: {score}')
score = sum([new_rules[row] for row in strategy_guide])
print(f'Part 2: {score}')
