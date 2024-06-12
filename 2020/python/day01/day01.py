import itertools

with open('day01/input.data') as input:
    expense_report = [int(line) for line in input.read().splitlines()]

combinations = list(itertools.combinations(expense_report, 2))
[product] = [x*y for (x, y) in combinations if x+y == 2020]
print(f"first solution: {product}")

combinations = list(itertools.combinations(expense_report, 3))
[product] = [x*y*z for (x, y, z) in combinations if x+y+z == 2020]
print(f"second solution: {product}")
