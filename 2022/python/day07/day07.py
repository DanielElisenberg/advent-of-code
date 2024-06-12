from collections import defaultdict


SIZE_OF = {}
TOTAL_SPACE = 70000000
FILESYSTEM = defaultdict(list)


def parse_filesystem(terminal_output: list[str]) -> defaultdict:
    current_path = ''
    for line in terminal_output[1:]:
        match line.split():
            case ['$', 'cd', '..']:
                current_path = '/'.join(current_path.split('/')[:-1])
            case ['$', 'cd', directory]:
                current_path = f"{current_path}/{line[5:]}"
            case ['dir', directory]:
                FILESYSTEM[current_path].append(directory)
            case [filesize, filename]:
                FILESYSTEM[current_path].append(f'{filename}:file')
                SIZE_OF[f'{current_path}/{filename}:file'] = int(filesize)


def calculate_size(path: str):
    if path not in SIZE_OF:
        SIZE_OF[path] = sum([
            calculate_size(f'{path}/{content}')
            for content in FILESYSTEM[path]
        ])
    return SIZE_OF[path]


with open('day07/input', encoding='utf-8') as f:
    terminal_output = [
        line.strip() for line in f if not line.startswith('$ ls')
    ]

parse_filesystem(terminal_output)
for directory in FILESYSTEM.keys():
    calculate_size(directory)

directory_sizes = [
    size for path, size in SIZE_OF.items()
    if not path.endswith(':file')
]
directory_sum = sum([s for s in directory_sizes if s <= 100000])
print(f"Part 1: {directory_sum}")

unused_space = TOTAL_SPACE - SIZE_OF['']
needed_space = 30000000 - unused_space
deleted_directory = min([s for s in directory_sizes if s >= needed_space])
print(f"Part 2: {deleted_directory}")
