import re
import json
import jsonschema


def validate_passport(schema, passport):
    try:
        jsonschema.validate(passport, schema)
        return True
    except jsonschema.ValidationError:
        return False


def count_valid_passports(schema, passports):
    with open(f'day04/{schema}.json') as schema_file:
        json_schema = json.loads(schema_file.read())

    passport_dicts = [dict(zip(passport[::2], passport[1::2]))
                      for passport in passports]
    return len(
        [passport for passport in passport_dicts
         if validate_passport(json_schema, passport)]
    )


with open('day04/input.data') as input:
    passports = (
        [re.split('[ :\\n]', line) for line in input.read().split('\n\n')]
    )

naive_validation_count = count_valid_passports(
    'naive_passport_schema', passports
)
strict_validation_count = count_valid_passports(
    'strict_passport_schema', passports
)
print(f'first solution: {naive_validation_count}')
print(f'second solution: {strict_validation_count}')
