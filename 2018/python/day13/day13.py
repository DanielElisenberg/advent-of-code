from collections import defaultdict


def move_right(wagon):
    wagon["x"] = wagon["x"] + 1
    wagon["path"] += wagon["dir"]
    wagon["dir"] = ">"


def move_left(wagon):
    wagon["x"] = wagon["x"] - 1
    wagon["path"] += wagon["dir"]
    wagon["dir"] = "<"


def move_up(wagon):
    wagon["y"] = wagon["y"] - 1
    wagon["path"] += wagon["dir"]
    wagon["dir"] = "^"


def move_down(wagon):
    wagon["y"] = wagon["y"] + 1
    wagon["path"] += wagon["dir"]
    wagon["dir"] = "v"


def move_intersection(wagon):
    direction = wagon["dir"]

    if wagon["next_turn"] == "left":
        if direction == "^":
            move_left(wagon)
        if direction == "v":
            move_right(wagon)
        if direction == "<":
            move_down(wagon)
        if direction == ">":
            move_up(wagon)
        wagon["next_turn"] = "straight"

    elif wagon["next_turn"] == "straight":
        if direction == "^":
            move_up(wagon)
        if direction == "v":
            move_down(wagon)
        if direction == "<":
            move_left(wagon)
        if direction == ">":
            move_right(wagon)
        wagon["next_turn"] = "right"

    elif wagon["next_turn"] == "right":
        if direction == "^":
            move_right(wagon)
        if direction == "v":
            move_left(wagon)
        if direction == "<":
            move_up(wagon)
        if direction == ">":
            move_down(wagon)
        wagon["next_turn"] = "left"


def move(wagon, tracks):
    direction = wagon["dir"]
    track = tracks[(wagon["x"], wagon["y"])]
    if direction == "^":
        if track == "\\":
            move_left(wagon)
        if track == "/":
            move_right(wagon)
        if track == "|":
            move_up(wagon)
        if track == "+":
            move_intersection(wagon)

    if direction == "v":
        if track == "\\":
            move_right(wagon)
        if track == "/":
            move_left(wagon)
        if track == "|":
            move_down(wagon)
        if track == "+":
            move_intersection(wagon)

    if direction == "<":
        if track == "\\":
            move_up(wagon)
        if track == "/":
            move_down(wagon)
        if track == "-":
            move_left(wagon)
        if track == "+":
            move_intersection(wagon)

    if direction == ">":
        if track == "\\":
            move_down(wagon)
        if track == "/":
            move_up(wagon)
        if track == "-":
            move_right(wagon)
        if track == "+":
            move_intersection(wagon)


def check_for_collisions(wagons):
    for wagon in wagons:
        oneself = True
        location = (wagon["x"], wagon["y"])
        for other_wagon in wagons:
            other_location = (other_wagon["x"], other_wagon["y"])
            if location == other_location:
                if oneself:
                    oneself = False
                else:
                    print(f"collision at {location}")
                    wagons.remove(wagon)
                    wagons.remove(other_wagon)
                    return True
    return False


def decide_underlying_track_type(tracks, x, y):
    top = False
    bot = False
    rgt = False
    lft = False

    if tracks.get((x, y - 1)) in ["|", "/", "\\", "+"]:
        top = True
    if tracks.get((x, y + 1)) in ["|", "/", "\\", "+"]:
        bot = True
    if tracks.get((x + 1, y)) in ["-", "/", "\\", "+"]:
        rgt = True
    if tracks.get((x - 1, y)) in ["-", "/", "\\", "+"]:
        lft = True

    if top and bot and not rgt and not lft:
        return "|"
    elif lft and rgt and not top and not bot:
        return "-"
    elif bot and rgt and not lft and not top:
        return "/"
    elif lft and top and not bot and not rgt:
        return "/"
    elif rgt and top and not bot and not lft:
        return "\\"
    elif lft and bot and not top and not rgt:
        return "\\"
    else:
        return "+"


input = open("day-13/input", "r")
lines = input.readlines()

tracks = defaultdict(lambda: " ")
wagons = []

for y in range(len(lines)):
    for x in range(len(lines[y])):
        tracks[(x, y)] = lines[y][x]

new_tracks = defaultdict(lambda: " ")

for key, val in tracks.items():
    if val in ["<", ">", "v", "^"]:
        underlying = decide_underlying_track_type(tracks, key[0], key[1])
        new_tracks[key] = underlying
        wagons.append(
            {"x": key[0], "y": key[1], "dir": val, "next_turn": "left", "path": ""}
        )
    else:
        new_tracks[key] = val

# tracks = new_tracks
# no_collisions = True
# while(no_collisions):
#    for wagon in sorted(wagons, key=lambda w: (w['y']*1000)+w['x']):
#        move(wagon, tracks)
#        no_collisions = not check_for_collisions(wagons)

tracks = new_tracks
no_collisions = True
while no_collisions:
    for wagon in sorted(wagons, key=lambda w: (w["y"] * 1000) + w["x"]):
        move(wagon, tracks)
        if check_for_collisions(wagons):
            no_collisions = False
for wagon in wagons:
    print(wagon["path"])
