def fold_paper(coordinates: list, fold_instructions: list) -> list:
    marked_dots = [(int(x), int(y)) for (x, y) in coordinates]

    for fold_instruction in fold_instructions:
        (fold_axis, fold_at) = (fold_instruction[0], int(fold_instruction[1]))
        folded_paper = []

        for dot in marked_dots:
            if fold_axis == 'x' and dot[0] >= fold_at:
                folded_paper.append(
                    (fold_at*2-dot[0], dot[1])
                )
            elif fold_axis == 'y' and dot[1] >= fold_at:
                folded_paper.append(
                    (dot[0], fold_at*2 - dot[1])
                )
            else:
                folded_paper.append(dot)
        marked_dots = folded_paper
    return list(set(marked_dots))


def print_instruction(marked_dots: list) -> str:
    max_x = max([dot[0] for dot in marked_dots])
    max_y = max([dot[1] for dot in marked_dots])
    instruction = ''

    for y in range(max_y+1):
        for x in range(max_x+1):
            instruction += '#' if (x, y) in marked_dots else '.'
        instruction += '\n'
    return instruction


if __name__ == "__main__":
    with open('day13/input') as input_file:
        dots_input, fold_input = input_file.read().split("\n\n")
        coordinates = [
            coordinate.strip().split(',')
            for coordinate in dots_input.split('\n')
        ]
        fold_instructions = [
            fold_instruction[11:].split('=')
            for fold_instruction in fold_input.split('\n')
        ]
    folded_once = fold_paper(coordinates, fold_instructions[:1])
    fully_folded = fold_paper(coordinates, fold_instructions)
    print(
        f"""Day 13:
        first solution: {len(folded_once)}
        second solution: \n{print_instruction(fully_folded)}"""
    )
