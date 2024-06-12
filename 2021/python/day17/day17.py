from itertools import accumulate


MIN_X, MAX_X = 192, 251
MIN_Y, MAX_Y = -89, -59


def x_hits_target(x: int) -> bool:
    return x in range(MIN_X, MAX_X+1)


def y_hits_target(y: int) -> bool:
    return y in range(MAX_Y, MIN_Y-1, -1)


def find_possible_x(include_step: bool = False) -> list:
    possible_x = set()
    for x in range(0, MAX_X+1):
        x_steps = accumulate(list(range(x, 0, -1)))
        possible_x.update(set([
            (x, step+1) for step, x_step in enumerate(x_steps)
            if x_hits_target(x_step)
        ]))
    if include_step:
        return list(possible_x)
    else:
        return list(set([x for x, _ in possible_x]))


def trick_shot():
    possible_x = find_possible_x()
    possible_y = []

    min_y_candidate = round((min(possible_x)-1)/2)
    for y_candidate in range(min_y_candidate, abs(MIN_Y)):
        if y_hits_target(-y_candidate):
            possible_y.append(y_candidate)
        y_candidate += 1
    return (min(possible_x), max(possible_y))


def all_trajectories():
    possible_trajectories = []
    possible_x = find_possible_x(include_step=True)
    for x, step in possible_x:
        for y in range(MIN_Y, abs(MIN_Y-1)):
            y_step = 0
            x_stagnates = step == x
            for i in range(step):
                y_step += y-i
            if x_stagnates:
                while y_step >= MIN_Y:
                    if y_hits_target(y_step):
                        possible_trajectories.append((x, y))
                    i += 1
                    y_step += y-i
            else:
                if y_hits_target(y_step):
                    possible_trajectories.append((x, y))
    return set(possible_trajectories)


if __name__ == "__main__":
    (x, y) = trick_shot()
    trick_shot_height = sum(range(y+1))
    print(
        f"""Day 17:
        first solution: {trick_shot_height}
        second solution: {len(all_trajectories())}"""
    )
