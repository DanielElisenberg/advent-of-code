def windowed(datastream: list[str], window: int) -> list[str]:
    staggered_streams = [datastream[i:] for i in range(window)]
    return [''.join(window) for window in (zip(*staggered_streams))]


with open('day06/input', encoding='utf-8') as f:
    datastream = f.read().strip()

start_of_packet = next(
    index + 4 for index, packet in enumerate(windowed(datastream, 4))
    if len(set(packet)) == 4
)
print(f"Part 1: {start_of_packet}")

start_of_message = next(
    index + 14 for index, packet in enumerate(windowed(datastream, 14))
    if len(set(packet)) == 14
)
print(f"Part 2: {start_of_message}")
