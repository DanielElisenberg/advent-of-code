from collections import defaultdict, deque


def next_player(current_player, amount_of_players):
    return current_player + 1 if current_player + 1 <= amount_of_players else 1


def insert_marble(circle, marble):
    circle.rotate(-1)
    circle.append(marble)


def is_multiple_of_23(marble):
    return True if marble % 23 == 0 else False


def take_marble(current_player, scores, circle):
    circle.rotate(7)
    scores[current_player] += circle.pop()
    circle.rotate(-1)
    return scores


def solve_for(last_marble, amount_of_players):
    circle = deque([0])
    scores = defaultdict(int)

    current_player = 1
    next_marble = 1

    for next_marble in range(1, last_marble + 1):
        if is_multiple_of_23(next_marble):
            scores[current_player] += next_marble
            scores = take_marble(current_player, scores, circle)
        else:
            insert_marble(circle, next_marble)
        current_player = next_player(current_player, amount_of_players)

    highest_score = 0
    for _, score in scores.items():
        if score > highest_score:
            highest_score = score
    return highest_score


print(f"answer #1: highest score was {solve_for(71144, 424)}")
print(f"answer #2: highest score was {solve_for(7114400, 424)}")
