def edit(instructions):
    for i in range(len(instructions)):
        instruction = instructions[i][0]
        if instruction == 'nop':
            instructions[i][0] = 'jmp'
            if run(instructions) > 0:
                return
            instructions[i][0] = 'nop'
        elif instruction == 'jmp':
            instructions[i][0] = 'nop'
            if run(instructions) > 0:
                return
            instructions[i][0] = 'jmp'


def run(instructions):
    current_instruction = 0
    accumulator = 0
    completed_instructions = set()

    while True:
        if current_instruction == len(instructions):
            return accumulator
        if current_instruction in completed_instructions:
            return accumulator*-1

        instruction = instructions[current_instruction][0]
        instruction_number = int(instructions[current_instruction][1])
        completed_instructions.add(current_instruction)

        if instruction == 'acc':
            accumulator += instruction_number
            current_instruction += 1
        elif instruction == 'jmp':
            current_instruction += instruction_number
        else:
            current_instruction += 1


with open('day08/input.data') as input:
    instructions = [line.split(' ') for line in input.read().split('\n')]


print(f'first solution: {run(instructions)*-1}')
edit(instructions)
print(f'second solution: {run(instructions)}')