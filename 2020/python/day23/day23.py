def run_moves(circle_map, start_cup, times):
    min_cup = min(circle_map.keys())
    max_cup = max(circle_map.keys())
    current_cup = start_cup
    for i in range(times):
        next_cup = circle_map[current_cup]
        destination_cup = None
        search_cup = current_cup - 1
        while destination_cup is None:
            if (
                    search_cup not in [
                        next_cup,
                        circle_map[next_cup],
                        circle_map[circle_map[next_cup]]
                    ]
                    and search_cup >= min_cup):
                destination_cup = search_cup
            elif search_cup < min_cup:
                search_cup = max_cup
            else:
                search_cup -= 1
        circle_map[current_cup] = circle_map[circle_map[circle_map[next_cup]]]
        old_next = circle_map[destination_cup]
        circle_map[destination_cup] = next_cup
        circle_map[circle_map[circle_map[next_cup]]] = old_next
        current_cup = circle_map[current_cup]


def ten_million_moves(circle):
    circle_map = {}

    for i in range(len(circle)-1):
        circle_map[circle[i]] = circle[i+1]
    max_cup = max(circle) + 1
    circle_map[circle[-1]] = max_cup
    while len(circle_map.keys()) < 999999:
        circle_map[max_cup] = max_cup + 1
        max_cup += 1
    circle_map[max_cup] = circle[0]

    run_moves(circle_map, circle[0], 10000000)
    return circle_map[1] * circle_map[circle_map[1]]


def hundred_moves(circle):
    circle_map = {}
    for i in range(len(circle)-1):
        circle_map[circle[i]] = circle[i+1]
    circle_map[circle[-1]] = circle[0]

    run_moves(circle_map, circle[0], 100)

    next_cup = circle_map[1]
    circle_string = str(next_cup)
    while True:
        next_cup = circle_map[next_cup]
        circle_string += str(next_cup)
        if next_cup == 1:
            break
    return circle_string[:-1]


input = '583976241'
print(f'first solution: {hundred_moves([int(ch) for ch in input])}')
print(f'second solution: {ten_million_moves([int(ch) for ch in input])}')
