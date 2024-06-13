from datetime import datetime
from collections import OrderedDict, defaultdict, Counter
import re


def generate_ordered_schedule(lines):
    """Generates an ordered dictionary from input data.

    Parameters:
    lines: lines fron input file

    Returns:
    OrderedDict(datetime, string): events sorted by timestamp

    """
    schedule = {}
    for line in lines:
        line_time = datetime.strptime(line[:18], "[%Y-%m-%d %H:%M]")
        schedule[line_time] = line[19:].strip("\n")
    return OrderedDict(sorted(schedule.items()))


def process_schedule(ordered_schedule):
    """Processes schedule for information on when guards sleep.

    Parameters:
    ordered_schedule (dictionary(datetime, string)): events sorted by timestamp

    Returns:
    dictionary(string, list): list of minutes asleep per guard

    """
    guard_info = defaultdict(list)
    current_guard = ""
    fell_asleep_at = 0

    for k, v in ordered_schedule.items():
        if "Guard" in v:
            guard_id = re.search(r"(?<=#).*?(?=\s)", v)
            current_guard = guard_id.group(0)
        if "falls asleep" in v:
            fell_asleep_at = k.minute
        if "wakes up" in v:
            for i in range(fell_asleep_at, k.minute):
                guard_info[current_guard].append((k.month * 1000 + k.day, i))
    return guard_info


def strategy_one(guard_info):
    """Finds the most frequently sleeping guard,
    and what minute that guard is most frequently asleep.
    """
    sleepy_guard_id, _ = max(guard_info.items(), key=lambda x: len(set(x[1])))
    sleepy_minute, _ = Counter(
        [i for (_, i) in guard_info[sleepy_guard_id]]
    ).most_common(1)[0]
    return int(sleepy_guard_id) * sleepy_minute


def strategy_two(guard_info):
    """Finds the guard most frequently asleep at one given minute"""
    sleepy_guard = (0, 0, 0)
    for guard_id in guard_info:
        this_guard = (int(guard_id),) + Counter(
            [i for (_, i) in guard_info[guard_id]]
        ).most_common(1)[0]
        if sleepy_guard[2] < this_guard[2]:
            sleepy_guard = this_guard
    return sleepy_guard[0] * sleepy_guard[1]


input = open("day04/input", "r")
lines = input.readlines()

ordered_schedule = generate_ordered_schedule(lines)
guard_info = process_schedule(ordered_schedule)

print(f"answer #1: {strategy_one(guard_info)}")
print(f"answer #2: {strategy_two(guard_info)}")
