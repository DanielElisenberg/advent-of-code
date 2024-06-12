def scan_ticket_requirements(lines):
    rules = lines[:20]
    requirements = {}
    for rule in rules:
        [rule_name, ranges] = rule.split(': ')
        [first_range, _, second_range] = ranges.split(' ')
        [first_range_min, first_range_max] = first_range.split('-')
        [second_range_min, second_range_max] = second_range.split('-')
        full_range = []
        for i in range(int(first_range_min), int(first_range_max)+1):
            full_range.append(i)
        for i in range(int(second_range_min), int(second_range_max)+1):
            full_range.append(i)
        requirements[rule_name] = full_range
    return requirements


def error_rate(tickets, requirements):
    requirements_set = set(
        [value for sublist in requirements.values() for value in sublist]
    )
    error_list = []
    [error_list.append(value) for sublist in tickets
     for value in sublist if value not in requirements_set]
    return sum(error_list)


def valid_tickets(tickets, requirements_set):
    def valid(ticket, requirements_set):
        return all(
            [True if value in requirements_set else False for value in ticket]
        )
    requirements_set = set(
        [value for sublist in requirements.values() for value in sublist]
    )
    return [
        ticket for ticket in tickets if valid(ticket, requirements_set)
    ]


def one_alternative_per_value(alternatives_list):
    return (sum(
        [len(alternatives) for alternatives in alternatives_list]
    ) == len(alternatives_list))


def find_field_order(tickets, requirements):
    tickets = valid_tickets(tickets, requirements)
    field_order_alternatives = [[] for i in range(20)]
    for i in range(20):
        ticket_values = [ticket[i] for ticket in tickets]
        for field_name in requirements.keys():
            invalid_values = [ticket_value for ticket_value in ticket_values
                              if ticket_value not in requirements[field_name]]
            if not invalid_values:
                field_order_alternatives[i].append(field_name)

    while not one_alternative_per_value(field_order_alternatives):
        for alternatives in field_order_alternatives:
            if len(alternatives) == 1:
                [a.remove(alternatives[0]) for a in field_order_alternatives
                 if len(a) != 1 and alternatives[0] in a]
    return [alternative for [alternative] in field_order_alternatives]


def multiply_departure_fields(field_order, my_ticket):
    multiplied_departure_fields = 1
    for i, field in enumerate(field_order):
        if 'departure' in field:
            multiplied_departure_fields *= my_ticket[i]
    return multiplied_departure_fields


with open('day16/input.data') as input:
    lines = [line for line in input.read().split('\n')]

requirements = scan_ticket_requirements(lines)
my_ticket = [int(value) for value in lines[22].split(',')]
other_tickets = []
for line in lines[25:]:
    other_tickets.append(
        [int(value) for value in line.split(',')]
    )

print(f'first solution: {error_rate(other_tickets, requirements)}')

field_order = find_field_order(other_tickets, requirements)
print(f'first solution: {multiply_departure_fields(field_order, my_ticket)}')