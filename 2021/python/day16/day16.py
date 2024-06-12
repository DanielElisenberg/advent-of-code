from typing import Tuple
import numpy


PACKET_TYPES = {
    "000": "SUM",
    "001": "PRODUCT",
    "010": "MINIMUM",
    "011": "MAXIMUM",
    "100": "LITERAL",
    "101": "GREATER_THAN",
    "110": "LESS_THAN",
    "111": "EQUAL_TO"
}


def sum_versions(binary_transmission: str, index: int) -> Tuple[int, int]:
    packet_version = binary_transmission[index:index+3]
    packet_type = PACKET_TYPES[binary_transmission[index+3:index+6]]
    index += 6
    summed_versions = int(packet_version, 2)

    if packet_type == "LITERAL":
        while binary_transmission[index] != "0":
            index += 5
        return summed_versions, index+5

    length_type_id = binary_transmission[index]
    if length_type_id == "0":
        length_of_subpackets = int(binary_transmission[index+1: index+16], 2)
        index += 16
        end_of_subpackets_index = index + length_of_subpackets
        while index < end_of_subpackets_index:
            subpacket_version_values, index = sum_versions(
                binary_transmission, index=index
            )
            summed_versions += subpacket_version_values
    else:
        amount_of_subpackets = int(binary_transmission[index+1: index+12], 2)
        index += 12
        for _ in range(amount_of_subpackets):
            subpacket_version_values, index = sum_versions(
                binary_transmission, index=index
            )
            summed_versions += subpacket_version_values
    return summed_versions, index


def evaluate_literal(binary_transmission: str, index: int) -> Tuple[int, int]:
    bitstring = ""
    while binary_transmission[index] != "0":
        bitstring += binary_transmission[index+1: index+5]
        index += 5
    bitstring += binary_transmission[index+1: index+5]
    return int(bitstring, 2), index+5


def evaluate_sub_packets(binary_transmission: str,
                         index: int) -> Tuple[list, int]:
    length_type_id = binary_transmission[index]
    subpacket_values = []
    if length_type_id == "0":
        length_of_subpackets = int(binary_transmission[index+1: index+16], 2)
        index += 16
        end_of_subpackets_index = index + length_of_subpackets
        while index < end_of_subpackets_index:
            evaluated_to, index = evaluate_packet(
                binary_transmission, index=index
            )
            subpacket_values.append(evaluated_to)
    else:
        amount_of_subpackets = int(binary_transmission[index+1: index+12], 2)
        index += 12
        for _ in range(amount_of_subpackets):
            evaluated_to, index = evaluate_packet(
                binary_transmission, index=index
            )
            subpacket_values.append(evaluated_to)
    return subpacket_values, index


def evaluate_packet(binary_transmission: str, index: int) -> Tuple[int, int]:
    packet_type = PACKET_TYPES[binary_transmission[index+3:index+6]]
    index += 6
    if packet_type == "LITERAL":
        return evaluate_literal(binary_transmission, index)
    else:
        subpacket_values, index = evaluate_sub_packets(
            binary_transmission, index
        )

    if packet_type == "SUM":
        return sum(subpacket_values), index
    elif packet_type == "PRODUCT":
        return numpy.prod(subpacket_values), index
    elif packet_type == "MINIMUM":
        return min(subpacket_values), index
    elif packet_type == "MAXIMUM":
        return max(subpacket_values), index
    elif packet_type == "GREATER_THAN":
        return int(subpacket_values[0] > subpacket_values[1]), index
    elif packet_type == "LESS_THAN":
        return int(subpacket_values[0] < subpacket_values[1]), index
    elif packet_type == "EQUAL_TO":
        return int(subpacket_values[0] == subpacket_values[1]), index


if __name__ == "__main__":
    with open('day16/input') as input_file:
        transmission = input_file.readline()
        binary_transmission = ""
        for char in transmission:
            binary_transmission += bin(int(char, 16))[2:].zfill(4)

    summed_version_numbers, _ = sum_versions(binary_transmission, 0)
    evaluated_value, _ = evaluate_packet(binary_transmission, 0)
    print(
        f"""Day 16:
        first solution: {summed_version_numbers}
        second solution: {evaluated_value}"""
    )
