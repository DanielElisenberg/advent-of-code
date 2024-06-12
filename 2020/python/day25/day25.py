door_public_key = 6930903
card_public_key = 19716708

subject_number = 7
divisor = 20201227
card_loop_size = None
value = 1
loop_size = 1
while card_loop_size is None:
    value = value * subject_number
    value = value % divisor
    if value == card_public_key:
        card_loop_size = loop_size
    loop_size += 1

encryption_key = 1
for _ in range(card_loop_size):
    encryption_key = encryption_key * door_public_key
    encryption_key = encryption_key % divisor

print(f'first solution: {encryption_key}')
