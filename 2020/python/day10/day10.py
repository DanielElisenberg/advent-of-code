def jolt_differences(adapter_outputs):
    jolt_diff_of = {1: 0, 3: 0}
    for i in range(len(adapter_outputs)-1):
        diff = adapter_outputs[i+1] - adapter_outputs[i]
        jolt_diff_of[diff] += 1
    return jolt_diff_of[1] * jolt_diff_of[3]


def possible_arrangments(adapter_outputs):
    amount_map = {adapter: 0 for adapter in adapter_outputs.keys()}
    amount_map[0] = 1
    amount_map[max(next_for.keys())+1] = 0

    while sum(amount_map.values()) > amount_map[99]:
        for adapter in amount_map.keys():
            if adapter != 99 and amount_map[adapter] > 0:
                for next_adapter in adapter_outputs[adapter]:
                    amount_map[next_adapter] += amount_map[adapter]
                amount_map[adapter] -= amount_map[adapter]
    return amount_map[max(next_for.keys())+1]


def next_for_adapters(adapter_outputs):
    next_for = {}
    for i in range(0, len(adapter_outputs)-1):
        possible_next = []
        for j in range(i+1, len(adapter_outputs)):
            if adapter_outputs[j] - adapter_outputs[i] > 3:
                break
            if adapter_outputs[j] - adapter_outputs[i] <= 3:
                possible_next.append(j)
        next_for[i] = possible_next
    return next_for


with open('day10/input.data') as input:
    adapter_outputs = [int(line) for line in input.read().split('\n')]

adapter_outputs.sort()
adapter_outputs = [0] + adapter_outputs
adapter_outputs.append(adapter_outputs[-1]+3)

print(f'first solution: {jolt_differences(adapter_outputs)}')
next_for = next_for_adapters(adapter_outputs)
print(f'second solution: {possible_arrangments(next_for)}')
