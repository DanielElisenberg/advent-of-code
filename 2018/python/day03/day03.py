def claim_the_fabric(lines):
    claimed_fabric = {}
    overlap = 0

    for line in lines:
        list = line.split(" ")
        id = list[0].strip("#")
        coords = list[2].strip(":").split(",")
        dim = list[3].strip("\n").split("x")
        print("id: " + id)
        for i in range(int(coords[1]), int(coords[1]) + int(dim[1])):
            for j in range(int(coords[0]), int(coords[0]) + int(dim[0])):
                if (i, j) in claimed_fabric.keys():
                    if claimed_fabric[(i, j)] == "claimed":
                        overlap += 1
                        claimed_fabric[(i, j)] = "overlapped"
                    else:
                        continue
                else:
                    claimed_fabric.update({(i, j): "claimed"})
    return overlap, claimed_fabric


def find_safe_claim(claimed_fabric, lines):
    for line in lines:
        list = line.split(" ")
        id = list[0].strip("#")
        coords = list[2].strip(":").split(",")
        dim = list[3].strip("\n").split("x")
        is_safe = True
        for i in range(int(coords[1]), int(coords[1]) + int(dim[1])):
            for j in range(int(coords[0]), int(coords[0]) + int(dim[0])):
                if claimed_fabric[(i, j)] == "overlapped":
                    is_safe = False
        if is_safe:
            return id
    return overlap, claimed_fabric


input = open("day03/input", "r")
lines = input.readlines()

overlap, claimed_fabric = claim_the_fabric(lines)
print(f"first answer: {overlap}")

safe_claim_id = find_safe_claim(claimed_fabric, lines)
print(f"second answer: {safe_claim_id}")
