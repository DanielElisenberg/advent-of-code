class Node:

    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value

    def get_value(self):
        if self.value.isdigit():
            return (int(self.value))
        elif self.value == '+':
            return self.left.get_value() + self.right.get_value()
        elif self.value == '*':
            return self.left.get_value() * self.right.get_value()


def value_or_nested_expression(line, i, parse_expression):
    if line[i] == '(':
        open_parenthesis = 1
        for j in range(i+1, len(line)):
            if line[j] == '(':
                open_parenthesis += 1
            if line[j] == ')':
                open_parenthesis -= 1
            if open_parenthesis == 0:
                inner_expression = parse_expression(line[i+1:j])
                return (Node(str(inner_expression.get_value())), j+1)
    else:
        return (Node(line[i]), i+1)


def parse_expression_plus_precedence(line):
    (root, i) = value_or_nested_expression(
        line, 0, parse_expression_plus_precedence
    )
    while i < len(line)-1:
        if line[i] == '+' and root.right is not None:
            new_branch = Node(line[i])
            new_branch.left = root.right
            (new_branch.right, i) = value_or_nested_expression(
                line, i+1, parse_expression_plus_precedence
            )
            root.right = new_branch
        else:
            new_root = Node(line[i])
            new_root.left = root
            (new_root.right, i) = value_or_nested_expression(
                line, i+1, parse_expression_plus_precedence
            )
            root = new_root
    return root


def parse_expression_same_precedence(line):
    (root, i) = value_or_nested_expression(
        line, 0, parse_expression_same_precedence
    )
    while i < len(line)-1:
        new_root = Node(line[i])
        new_root.left = root
        (new_root.right, i) = value_or_nested_expression(
            line, i+1, parse_expression_same_precedence
        )
        root = new_root
    return root


with open('day18/input.data') as input:
    lines = [line.replace(' ', '') for line in input.read().split('\n')]

sum_of_homework = sum(
    [parse_expression_same_precedence(line).get_value() for line in lines]
)
print(f'first solution: {sum_of_homework}')

sum_of_homework = sum(
    [parse_expression_plus_precedence(line).get_value() for line in lines]
)
print(f'second solution: {sum_of_homework}')
