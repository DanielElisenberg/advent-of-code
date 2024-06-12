def play_recursive_combat(first_deck, second_deck):
    player_one_deck = [card for card in first_deck]
    player_two_deck = [card for card in second_deck]
    history = []

    while player_one_deck and player_two_deck:
        if f'{player_one_deck}{player_two_deck}' in history:
            return player_one_deck, []
        history.append(f'{player_one_deck}{player_two_deck}')

        player_one_plays = player_one_deck.pop(0)
        player_two_plays = player_two_deck.pop(0)
        if player_one_plays <= len(player_one_deck) and player_two_plays <= len(player_two_deck):
            player_one_won, _ = play_recursive_combat(
                player_one_deck[:player_one_plays], player_two_deck[:player_two_plays]
            )
        else:
            player_one_won = player_one_plays > player_two_plays

        if player_one_won:
            player_one_deck += [player_one_plays, player_two_plays]
        else:
            player_two_deck += [player_two_plays, player_one_plays]
    return player_one_deck, player_two_deck


def play_combat(first_deck, second_deck):
    player_one_deck = [card for card in first_deck]
    player_two_deck = [card for card in second_deck]

    while player_one_deck and player_two_deck:
        player_one_plays = player_one_deck.pop(0)
        player_two_plays = player_two_deck.pop(0)
        if player_one_plays > player_two_plays:
            player_one_deck += [player_one_plays, player_two_plays]
        else:
            player_two_deck += [player_two_plays, player_one_plays]
    return player_one_deck, player_two_deck


with open('day22/input.data') as input:
    [player_one_deck, player_two_deck] = input.read().split('\n\n')
    player_one_deck = [int(card) for card in player_one_deck.split('\n')[1:]]
    player_two_deck = [int(card) for card in player_two_deck.split('\n')[1:]]

deck_one, deck_two = play_combat(player_one_deck, player_two_deck)
deck = deck_one + deck_two
score = sum([deck[-i]*i for i in range(1, len(deck)+1)])
print(f'first solution: {score}')

deck_one, deck_two = play_recursive_combat(player_one_deck, player_two_deck)
deck = deck_one + deck_two
score = sum([deck[-i]*i for i in range(1, len(deck)+1)])
print(f'second solution: {score}')
