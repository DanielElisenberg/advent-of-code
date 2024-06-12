from copy import deepcopy
import itertools


def rotate_on_x_plane(coordinates: list):
    return [(x, z, -y) for (x, y, z) in coordinates]


def rotate_on_y_plane(coordinates: list):
    return [(-z, y, x) for (x, y, z) in coordinates]


def rotate_on_z_plane(coordinates: list, times: int):
    if times == 1:
        return [(y, -x, z) for (x, y, z) in coordinates]
    elif times == 3:
        return [(-y, x, z) for (x, y, z) in coordinates]


def rotate_around_beacon_all_axes(coordinates: list):
    all_rotations = []
    x_plane_rotated = deepcopy(coordinates)
    for _ in range(4):
        x_plane_rotated = rotate_on_x_plane(x_plane_rotated)
        all_rotations.append(x_plane_rotated)
        y_plane_rotated = deepcopy(x_plane_rotated)
        for _ in range(3):
            y_plane_rotated = rotate_on_y_plane(y_plane_rotated)
            all_rotations.append(y_plane_rotated)
        all_rotations.append(rotate_on_z_plane(x_plane_rotated, times=1))
        all_rotations.append(rotate_on_z_plane(x_plane_rotated, times=3))
    return all_rotations


def largest_manhattan_distance(scanner_locations: list) -> int:
    scanner_pairs = itertools.product(scanner_locations, scanner_locations)
    return max([
        (
            abs(scanner[0]-compare_to[0]) +
            abs(scanner[1]-compare_to[1]) +
            abs(scanner[2]-compare_to[2])
        )
        for scanner, compare_to in scanner_pairs
    ])


if __name__ == "__main__":
    with open('day19/input') as input_file:
        scanner_input = [
            scanner.split('\n') for scanner in
            input_file.read().split('\n\n')
        ]
        scanners = {}
        for scanner_number in range(len(scanner_input)):
            beacon_list = scanner_input[scanner_number][1:]
            scanners[scanner_number] = [
                (
                    int(beacon.split(',')[0]),
                    int(beacon.split(',')[1]),
                    int(beacon.split(',')[2])
                )
                for beacon in beacon_list
            ]

        reference_scanner = scanners[0]
        scanner_matched = {
            scanner_number: False
            for scanner_number in range(1, len(scanners))
        }
        scanner_locations = [(0, 0, 0)]

        while not all(aligned for aligned in scanner_matched.values()):
            for scanner_number in range(1, len(scanners)):
                if scanner_matched[scanner_number]:
                    continue

                rotated_beacons_all = rotate_around_beacon_all_axes(
                    scanners[scanner_number]
                )
                for rotated_beacons in rotated_beacons_all:
                    for rotated_beacon in rotated_beacons:
                        for ref_beacon in reference_scanner:
                            assumed_scanner_location = (
                                ref_beacon[0]-rotated_beacon[0],
                                ref_beacon[1]-rotated_beacon[1],
                                ref_beacon[2]-rotated_beacon[2]
                            )
                            beacons_according_to_assumed_scanner = [
                                (
                                    beacon[0] + assumed_scanner_location[0],
                                    beacon[1] + assumed_scanner_location[1],
                                    beacon[2] + assumed_scanner_location[2]
                                )
                                for beacon in rotated_beacons
                            ]
                            matching_beacons = [
                                beacon for beacon
                                in beacons_according_to_assumed_scanner
                                if beacon in reference_scanner
                            ]
                            if len(matching_beacons) >= 12:
                                scanner_matched[scanner_number] = True
                                scanner_locations.append(
                                    assumed_scanner_location
                                )
                                reference_scanner += [
                                    beacon for beacon
                                    in beacons_according_to_assumed_scanner
                                    if beacon not in matching_beacons
                                ]
                                break
                        if scanner_matched[scanner_number]:
                            break
                    if scanner_matched[scanner_number]:
                        break

    print(
        f"""Day 19:
        first solution: {len(reference_scanner)}
        second solution: {largest_manhattan_distance(scanner_locations)}"""
    )
