import math


def find_earliest_bus(bus_ids_with_offsets, earliest_time):
    bus_ids = [id[0] for id in bus_ids_with_offsets]
    accumulate_ids = [id for id in bus_ids]
    while not all(time > earliest_time for time in accumulate_ids):
        for i in range(len(bus_ids)):
            accumulate_ids[i] += (
                bus_ids[i] if accumulate_ids[i] < earliest_time else 0
            )
    index = accumulate_ids.index(min(accumulate_ids))
    return (min(accumulate_ids) - earliest_time)*bus_ids[index]


def lowest_common_multiple(a, b):
    return abs(a*b) // math.gcd(a, b)


def timetables_align(bus_ids_with_offset, init_trip=0, idx=1, jump=1):
    trip = init_trip
    first_bus_id = bus_ids_with_offset[0][0]
    other_bus_id = bus_ids_with_offset[idx][0]
    offset = bus_ids_with_offset[idx][1]
    time = first_bus_id * trip

    while (time+offset) % other_bus_id != 0:
        trip += jump
        time = first_bus_id*trip
    if idx == len(bus_ids_with_offset)-1:
        return time
    else:
        lcm = lowest_common_multiple(first_bus_id*jump, other_bus_id)
        return timetables_align(
            bus_ids_with_offset,
            init_trip=trip,
            idx=idx+1,
            jump=lcm//first_bus_id
        )


with open('day13/input.data') as input:
    lines = [line for line in input.read().split('\n')]
    earliest_time = int(lines[0])
    bus_ids = [id for id in lines[1].split(',')]
    bus_ids_with_offset = [(int(id), bus_ids.index(id))
                           for id in bus_ids if id != 'x']

earliest_bus = find_earliest_bus(bus_ids_with_offset, earliest_time)
print(f'first solution: {earliest_bus}')
time_of_alignment = timetables_align(bus_ids_with_offset)
print(f'second solution: {time_of_alignment}')
