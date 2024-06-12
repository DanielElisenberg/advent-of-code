def calculate_seat_id(seat_specification):
    row = sum(
        [2**(6-i) for i, spec in enumerate(seat_specification) if spec == 'B']
    )
    column = sum(
        [2**(9-i) for i, spec in enumerate(seat_specification) if spec == 'R']
    )
    return row*8+column


with open('day05/input.data') as input:
    seat_specifications = [list(line) for line in input.read().split()]

seat_ids = [calculate_seat_id(seat_specification) 
            for seat_specification in seat_specifications]

highest_id = max(seat_ids)
lowest_id = min(seat_ids)
missing_id = sum(range(highest_id+1)) - sum(range(lowest_id)) - sum(seat_ids)

print(f'first solution: {highest_id}')
print(f'second solution: {missing_id}')
