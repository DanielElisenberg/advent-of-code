from itertools import accumulate


def find_duplicate(frequencies):
    reached_frequencies = set()
    for i in range(len(frequencies)):
        if frequencies[i] in reached_frequencies:
            return frequencies[i]
        else:
            reached_frequencies.add(frequencies[i])
    return None


input = open("day01/input", "r")
frequencies = [int(line) for line in input.readlines()]

frequency_log = list(accumulate([0] + frequencies))
print(f"first answer: {frequency_log[-1]}")

while find_duplicate(frequency_log) is None:
    new_frequencies = list(accumulate(frequency_log[-1:] + frequencies))
    frequency_log = frequency_log[:-1] + new_frequencies

print(f"second answer: {find_duplicate(frequency_log)}")
