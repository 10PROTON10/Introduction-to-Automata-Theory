import csv


path = {}
with open('path.csv', 'r') as file:
    csv_reader = csv.reader(file, delimiter=';')
    for row in csv_reader:
        start_node = row[0]
        end_node = row[-1]
        values = list(map(int, row[1:-1]))

        if start_node not in path:
            path[start_node] = {}

        if end_node not in path[start_node]:
            path[start_node][end_node] = []

        path[start_node][end_node].extend(values)

print(path)


def find_paths(node, sequence, current_path=None):
    if not sequence:
        return [[]]

    if node not in path:
        return []

    if current_path is None:
        current_path = []

    paths = []

    for neighbor, values in path[node].items():
        for val in values:
            if int(val) == int(sequence[0]):
                subpaths = find_paths(neighbor, sequence[1:], current_path + [(node, neighbor, val)])
                for subpath in subpaths:
                    paths.append([neighbor] + subpath)

    return paths


def can_reach_sequence(node, sequence):
    paths = find_paths(node, sequence)
    return len(paths) > 0


start = 'A'


sequence = input("Введите последовательность 0 и 1: ")


result = can_reach_sequence(start, sequence)
print(result)
