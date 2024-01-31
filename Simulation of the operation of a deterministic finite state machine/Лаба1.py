import csv

# Считываем CSV файл и представляем его в виде словаря
path = {}
with open('path.csv', 'r') as file:
    csv_reader = csv.reader(file, delimiter=';')
    for row in csv_reader:
        start_node, value, end_node = row
        if start_node not in path:
            path[start_node] = {}
        path[start_node][end_node] = int(value)
print(path)
# Функция для проверки, можно ли пройти всю последовательность начиная с заданной вершины

def can_reach_sequence(node, sequence):
    if not sequence:
        return True

    if node not in path:
        return False

    for neighbor, value in path[node].items():
        if sequence and value == int(sequence[0]):
            if can_reach_sequence(neighbor, sequence[1:]):
                return True

    return False

# Задаем начальную точку
start = 'A'

# Ввод последовательности 0 и 1
sequence = input("Введите последовательность 0 и 1: ")

# Проверяем, существует ли путь в графе для введенной последовательности
result = can_reach_sequence(start, sequence)
print(result)




