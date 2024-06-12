part_1_scores = [3, 0, 6]
part_2_scores = [3, 1, 2, 4, 5, 6, 8, 9, 7]
to_int = {'A': 1, 'B': 2, 'C': 3, 'X': 1, 'Y': 2, 'Z': 3}

with open('day02/input', encoding='utf-8') as f:
    strategy_guide = [
        (to_int[line[0]], to_int[line[2]]) for line in f
    ]

total_score = sum(
    [part_1_scores[col1-col2] + col2 for col1, col2 in strategy_guide]
)
print(f'Part 1: {total_score}')

total_score = sum([
    part_2_scores[3*(col2-1)+col1-1]
    for col1, col2 in strategy_guide
])
print(f'Part 2: {total_score}')
