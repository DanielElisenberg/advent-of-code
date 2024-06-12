from typing import Callable


BIT_STRING_LENGTH = 12


def most_common_bit(bit_strings: list, position: int) -> str:
    ones = len(
        [1 for bit_string in bit_strings if bit_string[position] == "1"]
    )
    zeros = len(
        [1 for bit_string in bit_strings if bit_string[position] == "0"]
    )
    if ones == zeros:
        return "1"
    else:
        return "1" if ones > zeros else "0"


def least_common_bit(bit_strings: list, position: int):
    most_common = most_common_bit(bit_strings, position)
    return "0" if most_common == "1" else "1"


def locate_rating_value(diagnostic_report: list, filter: Callable) -> str:
    position = 0
    remaining_bit_strings = diagnostic_report
    while len(remaining_bit_strings) > 1:
        filter_bit = filter(remaining_bit_strings, position)
        filtered_list = [
            bit_string for bit_string in remaining_bit_strings
            if bit_string[position] == filter_bit
        ]
        remaining_bit_strings = filtered_list
        position += 1
    return int(remaining_bit_strings[0], 2)


if __name__ == "__main__":
    with open('day03/input') as input_file:
        diagnostic_report = [
            line.strip('\n') for line in input_file.readlines()
        ]

    most_common_bits = ''.join([
        most_common_bit(diagnostic_report, position)
        for position in range(BIT_STRING_LENGTH)
    ])

    gamma_rate = int(most_common_bits, 2)
    epsilon_rate = int(
        ''.join(["0" if bit == "1" else "1" for bit in most_common_bits]), 2
    )
    oxygen_generator_rating = locate_rating_value(
        diagnostic_report, most_common_bit
    )
    co2_scrubber_rating = locate_rating_value(
        diagnostic_report, least_common_bit
    )

    print(
        f"""Day 3:
        first solution: {gamma_rate*epsilon_rate}
        second solution: {oxygen_generator_rating * co2_scrubber_rating}"""
    )
