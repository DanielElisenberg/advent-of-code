import re


def old_validation(low, high, char, password):
    return int(low) <= password.count(char) <= int(high)


def new_validation(low, high, char, password):
    return ((password[int(low)-1] == char) ^
            (password[int(high)-1] == char))


def valid_password_count(lines, validation):
    return len(
        [password for [low, high, char, password] in lines
         if validation(low, high, char, password)]
    )


with open('day02/input.data') as input:
    lines = [re.split('[- :]+', line) for line in input.read().splitlines()]

print(f'first solution: {valid_password_count(lines, old_validation)}')
print(f'second solution: {valid_password_count(lines, new_validation)}')
