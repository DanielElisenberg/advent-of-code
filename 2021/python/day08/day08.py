if __name__ == "__main__":
    with open('day08/input') as input_file:
        input = [
            line.strip().split(" | ") for line in input_file.readlines()
        ]
        input_signals, output_signals = [], []
        for line in input:
            input_signals.append(
                ["".join(sorted(signal)) for signal in line[0].split()]
            )
            output_signals.append(
                ["".join(sorted(signal)) for signal in line[1].split()]
            )

    first_solution = 0
    for output_signal in output_signals:
        first_solution += len([
            output for output in output_signal
            if len(output) in [2, 3, 4, 7]
        ])

    second_solution = 0
    for i in range(len(input)):
        input_line = input_signals[i]
        output_line = output_signals[i]
        signal_patterns = {
            "1": next(signal for signal in input_line if len(signal) == 2),
            "7": next(signal for signal in input_line if len(signal) == 3),
            "4": next(signal for signal in input_line if len(signal) == 4),
            "8": next(signal for signal in input_line if len(signal) == 7)
        }
        five_length_signals = [
            signal for signal in input_line if len(signal) == 5
        ]
        six_length_signals = [
            signal for signal in input_line if len(signal) == 6
        ]

        for signal in six_length_signals:
            if all(
                char in signal
                for char in signal_patterns["4"] + signal_patterns["7"]
            ):
                signal_patterns["9"] = signal
            elif all(char in signal for char in signal_patterns["7"]):
                signal_patterns["0"] = signal
            else:
                signal_patterns["6"] = signal

        for signal in five_length_signals:
            missing_from_six = "".join(
                char for char in "abcdefg" if char not in signal_patterns["6"]
            )
            if all(char in signal for char in signal_patterns["1"]):
                signal_patterns["3"] = signal
            elif missing_from_six in signal:
                signal_patterns["2"] = signal
            else:
                signal_patterns["5"] = signal
        value_for_signal = {
            signal: number for number, signal in signal_patterns.items()
        }
        second_solution += int(
            "".join([value_for_signal[output] for output in output_line])
        )

    print(
        f"""Day 8:
        first solution: {first_solution}
        second solution: {second_solution}"""
    )
