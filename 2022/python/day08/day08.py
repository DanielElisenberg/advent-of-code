
from functools import reduce


def get_trees_to_edges(
    row: int, column: int, grid: list[list[str]]
) -> list[list[str]]:
    return (
        list(reversed([tree for tree in grid[row][:column]])),
        [tree for tree in grid[row][column+1:]],
        list(reversed([row[column] for row in grid[:row]])),
        [row[column] for row in grid[row+1:]]
    )


def calculate_scenic_score(
    from_tree: str, trees_to_edges: list[list[str]]
) -> int:
    def blocking_tree_index(from_tree: str, trees: list[str]) -> int:
        return next(
            (index for index, tree in enumerate(trees) if tree >= from_tree),
            len(trees)
        )
    return reduce(lambda x, y: x*y, [
        len(trees[:1 + blocking_tree_index(from_tree, trees)])
        for trees in trees_to_edges
    ])


def is_visible(from_tree, trees_to_edges: list[list[str]]) -> bool:
    return [] in [
        [tree for tree in trees if tree >= from_tree]
        for trees in trees_to_edges
    ]


with open('day08/input', encoding='utf-8') as f:
    grid = [line.strip() for line in f]

trees = reduce(lambda x, y: x+y, [
    [(tree, get_trees_to_edges(y, x, grid)) for x, tree in enumerate(row)]
    for y, row in enumerate(grid)
])
visible_trees = sum(
    [1 for (tree, to_edges) in trees if is_visible(tree, to_edges)]
)
scenic_score = max(
    [calculate_scenic_score(tree, to_edges) for (tree, to_edges) in trees]
)
print(f'Part 1 : {visible_trees}')
print(f'Part 2 : {scenic_score}')
