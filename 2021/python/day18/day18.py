import math
import itertools


class Pair:
    def __init__(self, parent=None, right=None, left=None):
        self.parent = parent
        self.right = right
        self.left = left

    def magnitude(self) -> int:
        magnitude_left = (
            self.left*3 if type(self.left) is int
            else self.left.magnitude()*3
        )
        return magnitude_left + (
            self.right*2 if type(self.right) is int
            else self.right.magnitude()*2
        )

    def reduce(self) -> None:
        while True:
            if self.explode():
                continue
            if self.split():
                continue
            break

    def split(self) -> bool:
        if type(self.left) is int and self.left >= 10:
            self.left = self.__split_child(self.left)
            return True
        elif type(self.left) is Pair and self.left.split():
            return True

        if type(self.right) is int and self.right >= 10:
            self.right = self.__split_child(self.right)
            return True
        elif type(self.right) is Pair and self.right.split():
            return True
        return False

    def explode(self, depth=0) -> bool:
        if depth == 4:
            left_value, right_value = (self.left, self.right)
            parent = self.parent
            self.__add_to_left(left_value)
            self.__add_to_right(right_value)
            if parent.right is self:
                parent.right = 0
            else:
                parent.left = 0
            return True

        if type(self.left) is Pair and self.left.explode(depth=depth+1):
            return True
        elif type(self.right) is Pair:
            return self.right.explode(depth=depth+1)
        else:
            return False

    def __split_child(self, value_to_split: int) -> None:
        return Pair(
            parent=self,
            left=math.floor(value_to_split/2),
            right=math.ceil(value_to_split/2)
        )

    def __add_to_right(self, value: int):
        child = self
        parent = self.parent
        while True:
            if parent is None:
                return
            if parent.right is child:
                child = parent
                parent = child.parent
            elif type(parent.right) is int:
                parent.right += value
                return
            else:
                break
        add_to_tree = parent.right
        while not type(add_to_tree.left) is int:
            add_to_tree = add_to_tree.left
        add_to_tree.left += value

    def __add_to_left(self, value: int):
        child = self
        parent = self.parent
        while True:
            if parent is None:
                return
            if parent.left is child:
                child = parent
                parent = child.parent
            elif type(parent.left) is int:
                parent.left += value
                return
            else:
                break
        add_to_tree = parent.left
        while not type(add_to_tree.right) is int:
            add_to_tree = add_to_tree.right
        add_to_tree.right += value

    def __add__(self, other):
        combined = Pair(
            left=self,
            right=other
        )
        self.parent = other.parent = combined
        combined.reduce()
        return combined

    def __str__(self) -> str:
        return f"[{str(self.left)},{str(self.right)}]"


def parse_snailfish_number(snailfish_notation: str) -> Pair:
    snailfish_number = Pair()
    current = snailfish_number
    insert_at = "left"
    for char in snailfish_notation[1:]:
        if char == "[":
            sub_pair = Pair(parent=current)
            if insert_at == "left":
                current.left = sub_pair
            else:
                current.right = sub_pair
                insert_at = "left"
            current = sub_pair
        elif char.isdigit() and insert_at == "left":
            current.left = int(char)
        elif char.isdigit() and insert_at == "right":
            current.right = int(char)
        elif char == ",":
            insert_at = "right"
        elif char == "]":
            current = current.parent
    return snailfish_number


def magnitude_of_final_sum(lines: list) -> int:
    snailfish_number = parse_snailfish_number(lines[0])
    for line in lines[1:]:
        snailfish_number += parse_snailfish_number(line)
    return snailfish_number.magnitude()


def biggest_magnitude_pair(lines: list) -> int:
    return max([
        magnitude_of_final_sum(line_pair)
        for line_pair in itertools.product(lines, lines)
    ])


if __name__ == "__main__":
    with open('day18/input') as input_file:
        lines = [line.strip() for line in input_file.readlines()]
    print(
        f"""Day 18:
        first solution: {magnitude_of_final_sum(lines)}
        second solution: {biggest_magnitude_pair(lines)}"""
    )
