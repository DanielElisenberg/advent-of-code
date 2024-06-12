from collections import defaultdict


def find_number(input, at):
    count = len(input)+1
    last_appeared = defaultdict(int)
    for i in range(len(input)):
        last_appeared[input[i]] = i+1

    last_number = input[-1]
    while count <= at:
        if last_appeared[last_number] == 0:
            last_appeared[last_number] = count-1
            last_number = 0
        else:
            new_number = count - 1 - last_appeared[last_number]
            last_appeared[last_number] = count-1
            last_number = new_number
        count += 1
    return last_number


input = [14, 1, 17, 0, 3, 20]
print(f'first solution: {find_number(input, 2020)}')
print(f'second solution: {find_number(input, 30000000)}')
