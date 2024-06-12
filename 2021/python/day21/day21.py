from collections import defaultdict


PLAYER_1_STARTING_POSITION = 7
PLAYER_2_STARTING_POSITION = 10


def play_with_deterministic_die() -> int:
    player_1_score = [PLAYER_1_STARTING_POSITION]
    player_2_score = [PLAYER_2_STARTING_POSITION]
    total_die_rolls = 0
    turn = 1

    while sum(player_1_score[1:]) < 1000 and sum(player_2_score[1:]) < 1000:
        roll = 0
        for _ in range(3):
            total_die_rolls += 1
            roll += (
                total_die_rolls % 100 if total_die_rolls % 100 != 0 else 100
            )
        if turn == 1:
            next_score = (
                (player_1_score[-1] + roll) % 10
                if (player_1_score[-1] + roll) % 10 != 0
                else 10
            )
            player_1_score.append(next_score)
        else:
            next_score = (
                (player_2_score[-1] + roll) % 10
                if (player_2_score[-1] + roll) % 10 != 0
                else 10
            )
            player_2_score.append(next_score)
        turn = 1 if turn == 2 else 2

    losing_player_score = (
        sum(player_1_score[1:]) if sum(player_1_score[1:]) < 1000
        else sum(player_2_score[1:])
    )
    return losing_player_score * total_die_rolls


def roll_next(score: list, winning_rolls: defaultdict(int),
              losing_rolls: defaultdict(int), frequency_for_roll: dict,
              frequency: int) -> None:
    if sum(score[1:]) >= 21:
        winning_rolls[len(score[1:])] += frequency
        return
    else:
        losing_rolls[len(score[1:])] += frequency

    for roll, next_frequency in frequency_for_roll.items():
        next_score = (
            (score[-1]+roll) % 10 if (score[-1]+roll) % 10 != 0
            else 10
        )
        roll_next(
            score + [next_score],
            winning_rolls, losing_rolls,
            frequency_for_roll, frequency*next_frequency
        )


def play_with_quantum_die() -> int:
    frequency_for_roll = defaultdict(int)
    for first_roll in range(1, 4):
        for second_roll in range(1, 4):
            for third_roll in range(1, 4):
                frequency_for_roll[first_roll+second_roll+third_roll] += 1
    player_1_score = [PLAYER_1_STARTING_POSITION]
    player_2_score = [PLAYER_2_STARTING_POSITION]

    winning_rolls_1, losing_rolls_1 = defaultdict(int), defaultdict(int)
    roll_next(
        player_1_score,
        winning_rolls_1, losing_rolls_1,
        frequency_for_roll, 1
    )
    winning_rolls_2, losing_rolls_2 = defaultdict(int), defaultdict(int)
    roll_next(
        player_2_score,
        winning_rolls_2, losing_rolls_2,
        frequency_for_roll, 1
    )

    player_1_won_times = sum([
        amount * losing_rolls_2[rolls-1]
        for rolls, amount in winning_rolls_1.items()
    ])
    player_2_won_times = sum([
        amount * losing_rolls_1[rolls]
        for rolls, amount in winning_rolls_2.items()
    ])
    return max(player_1_won_times, player_2_won_times)


if __name__ == "__main__":
    print(
        f"""Day 21:
        first solution: {play_with_deterministic_die()}
        second solution: {play_with_quantum_die()}"""
    )
