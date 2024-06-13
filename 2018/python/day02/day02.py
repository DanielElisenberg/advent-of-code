def appears_in_string(times, character, string):
    if string.count(character) == times:
        return True
    return False


def generate_checksum(lines):
    thrice = 0
    twice = 0
    for line in lines:
        repeats_thrice = False
        repeats_twice = False
        for character in line:
            if appears_in_string(2, character, line):
                repeats_twice = True
            if appears_in_string(3, character, line):
                repeats_thrice = True
        if repeats_twice:
            twice += 1
        if repeats_thrice:
            thrice += 1
    return twice * thrice


def one_off(line, other_line):
    if line == other_line:
        return False

    one_off = False
    for c1, c2 in zip(line, other_line):
        if c1 != c2:
            if one_off:
                return False
            else:
                one_off = True
    return True


def common_letters(line, other_line):
    common_string = ""
    for i in range(len(line)):
        if line[i] == other_line[i]:
            common_string += line[i]
    return common_string


def find_similar_ID(lines):
    for line in lines:
        for other_line in lines:
            if one_off(line, other_line):
                return common_letters(line, other_line)


input = open("day02/input", "r")
lines = input.readlines()

print(f"first answer: {generate_checksum(lines)}")
print(f"second answer: {find_similar_ID(lines)}")
