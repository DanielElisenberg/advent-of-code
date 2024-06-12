BOARD_SIZE = 5


class Board():
    def __init__(self, content):
        self.board = [line.split() for line in content]
        self.has_won = False

    def mark(self, called_number: int) -> None:
        self.board = [
            ["x" if number == called_number else number for number in row]
            for row in self.board
        ]

    def has_bingo(self) -> bool:
        bingo_in_row = any(
            all(num == "x" for num in row) for row in self.board
        )
        transposed_board = [list(column) for column in zip(*self.board)]
        bingo_in_column = any(
            all(num == "x" for num in column) for column in transposed_board
        )
        if bingo_in_row or bingo_in_column:
            self.has_won = True
        return self.has_won

    def sum(self) -> int:
        return sum(
            sum(int(number) for number in row if number != "x")
            for row in self.board
        )


def play_bingo(numbers_to_draw: list, boards: list) -> list[int]:
    winners = []
    for number in numbers_to_draw:
        for board in boards:
            if board.has_won:
                continue
            board.mark(number)
            if board.has_bingo():
                winners.append(board.sum()*int(number))
    return winners


if __name__ == "__main__":
    with open('day04/input') as input_file:
        input = [
            line.strip() for line in input_file.readlines()
        ]
    numbers_to_draw = input[0].split(",")
    boards = [
        Board(input[i:i+BOARD_SIZE])
        for i in range(2, len(input), BOARD_SIZE+1)
    ]
    winners = play_bingo(numbers_to_draw, boards)

    print(
        f"""Day 4:
        first solution: {winners[0]}
        second solution: {winners[-1]}"""
    )
