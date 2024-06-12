from typing import Tuple


def completion_points_for_line(open_chunks: list) -> int:
    point_for = {
        "(": 1,
        "[": 2,
        "{": 3,
        "<": 4
    }
    missing_characters = [
        character for character in list(reversed(open_chunks))
    ]
    completion_points = 0
    for character in missing_characters:
        completion_points = completion_points * 5 + point_for[character]
    return completion_points


def parse_line(line: str) -> Tuple[list, int]:
    open_chunks = []
    match_for = {
        "[": "]",
        "(": ")",
        "{": "}",
        "<": ">"
    }
    for character in line:
        if character in ["(", "[", "{", "<"]:
            open_chunks.append(character)
        else:
            if match_for[open_chunks.pop()] != character:
                syntax_error_score = {
                    ")": 3,
                    "]": 57,
                    "}": 1197,
                    ">": 25137
                }[character]
                return open_chunks, syntax_error_score
    return open_chunks, 0


if __name__ == "__main__":
    with open('day10/input') as input_file:
        parsed_lines = [
            parse_line(line.strip()) for line in input_file.readlines()
        ]

    syntax_error_score = sum(
        [line_error_score for (_, line_error_score) in parsed_lines]
    )
    completion_points = [
        completion_points_for_line(open_chunks)
        for (open_chunks, line_error_score) in parsed_lines
        if not line_error_score
    ]
    completion_points.sort()
    print(
        f"""Day 10:
        first solution: {syntax_error_score}
        second solution: {completion_points[(len(completion_points))//2]}"""
    )
