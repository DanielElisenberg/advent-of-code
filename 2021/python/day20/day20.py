from copy import deepcopy


def extend_image_with_frame(image, infinity_pixel):
    all_x = [x for x, _ in image]
    all_y = [y for _, y in image]
    for y in range(min(all_y)-1, max(all_y)+2):
        for x in range(min(all_x)-1, max(all_x)+2):
            image[(x, y)] = image.get((x, y), infinity_pixel)


def lit_pixels_in(image):
    return len(
        [pixel for pixel in image.values() if pixel == "#"]
    )


def algorithm_index(image, x, y, infinity_pixel):
    bitstring = ""
    for search_y in range(y-1, y+2):
        for search_x in range(x-1, x+2):
            char = image.get((search_x, search_y), infinity_pixel)
            bitstring += "1" if char == "#" else "0"
    return int(bitstring, 2)


def enhance_image(image, enhancement_algorithm, times):
    infinity_pixel = '.'
    for _ in range(times):
        extend_image_with_frame(image, infinity_pixel)
        enhanced_image = {
            (x, y): enhancement_algorithm[
                algorithm_index(image, x, y, infinity_pixel)
            ]
            for (x, y) in image
        }
        image = enhanced_image
        infinity_pixel = "." if infinity_pixel == "#" else "#"
    return image


if __name__ == "__main__":
    with open('day20/input') as input_file:
        lines = [
            line.strip() for line in
            input_file.readlines()
        ]
        enhancement_algorithm = {
            value: char for value, char in enumerate(lines[0])
        }
        input_image = {}
        for y, line in enumerate(lines[2:]):
            for x, char in enumerate(line):
                input_image[(x, y)] = char

    enhanced_twice = enhance_image(
        deepcopy(input_image), enhancement_algorithm, 2
    )
    enhanced_50_times = enhance_image(
        deepcopy(input_image), enhancement_algorithm, 50
    )

    print(
        f"""Day 20:
        first solution: {lit_pixels_in(enhanced_twice)}
        second solution: {lit_pixels_in(enhanced_50_times)}"""
    )
