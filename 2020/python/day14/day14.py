from collections import defaultdict


def sum_memory_old_chip(lines):
    mem = defaultdict(int)
    for line in lines:
        if 'mask' in line:
            and_mask = int(''.join(
                ['0' if ch == '0' else '1' for ch in line[7:]]
            ), 2)
            or_mask = int(''.join(
                ['1' if ch == '1' else '0' for ch in line[7:]]
            ), 2)
        else:
            split_line = line.split('] = ')
            location = int(split_line[0][4:])
            value = (int(split_line[1]) & and_mask) | or_mask
            mem[location] = value
    return sum(mem.values())


def sum_memory_new_chip(lines):
    mem = defaultdict(int)
    for line in lines:
        if 'mask' in line:
            x_mask = line[7:]
            bitlength = len([x for x in x_mask if x == 'X'])
            variations = ["{0:0{len}b}".format(i, len=bitlength)
                          for i in range(2**bitlength)]
        else:
            split_line = line.split('] = ')
            location_bitstring = '{0:0{len}b}'.format(
                int(split_line[0][4:]),
                len=len(x_mask)
            )
            value = int(split_line[1])

            for variation in variations:
                location_variation = list(location_bitstring)
                counter = 0
                for i in range(len(x_mask)):
                    if x_mask[i] == 'X':
                        location_variation[i] = variation[counter]
                        counter += 1
                    elif x_mask[i] == '1':
                        location_variation[i] = '1'
                mem[''.join(location_variation)] = value
    return sum(mem.values())


with open('day14/input.data') as input:
    lines = [line for line in input.read().split('\n')]

print(f'first solution: {sum_memory_old_chip(lines)}')
print(f'second solution: {sum_memory_new_chip(lines)}')
