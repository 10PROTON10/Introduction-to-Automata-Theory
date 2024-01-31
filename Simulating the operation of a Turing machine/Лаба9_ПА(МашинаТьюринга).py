import csv
import re


def read_csv(file_path):
    result_dict = {}
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')
        header = next(csv_reader)
        column_names = header[1:]
        for row in csv_reader:
            state = row[0]
            transitions = [cell if cell != '---' else '---' for cell in row[1:]]
            result_dict[state] = dict(zip(column_names, transitions))
    return result_dict


def find_initial_head_position(tape):
    match = re.search(r'q(\d)(.)', tape)
    if match:
        return match.group(2)
    return None


def get_value_from_matrix(matrix, row_name, column_name):
    if row_name in matrix:
        row = matrix[row_name]
        if column_name in row:
            value = row[column_name]
            if value != '---':
                return value
    return '---'


def run_turing_machine(input_tape, transitions):
    tape = 'q0' + input_tape

    while len(tape) - tape.find('q') > 1:
        match = re.search(r'q(\d)', tape)
        if match:
            result_string = "q" + match.group(1)
        else:
            print("Подстрока не найдена.")

        head_position = find_initial_head_position(tape)
        value_at_intersection = get_value_from_matrix(transitions, result_string, head_position)

        if value_at_intersection == '---':
            return tape

        new_state, write_symbol, move_direction = value_at_intersection.split(',')
        tape = tape.replace(result_string, new_state, 1)
        for i in range(len(tape)):
            if tape[i] == head_position:
                if i > 0 and tape[i - 1] != 'q':
                    tape = tape[:i] + write_symbol + tape[i + 1:]
                    break
                elif i == 0:
                    tape = write_symbol + tape[1:]
                    break

        if move_direction == 'R':
            q_index = tape.find('q')
            if q_index != -1 and q_index < len(tape) - 2:
                tape = tape[:q_index] + tape[q_index + 2] + 'q' + tape[q_index + 1] + tape[q_index + 3:]
                print(tape)
        elif move_direction == 'L':
            q_index = tape.find('q')
            if q_index != -1 and q_index < len(tape) - 2:
                tape = tape[:q_index-1] + 'q' + tape[q_index+1] + tape[q_index-1] + tape[q_index+2:]
                print(tape)

        q_match = re.search(r'q(\d)', tape)
        if q_match and q_match.end() == len(tape):
            tape += 'B'
            print(tape)

    return tape


if __name__ == "__main__":
    file_path = 'moi_0011.csv'
    transitions = read_csv(file_path)

    input_tape = input("Введите цепочку из 0 и 1: ")
    result_tape = run_turing_machine(input_tape, transitions)
    if 'q0' + input_tape != result_tape:
        print("Результат работы машины Тьюринга:", result_tape)
    else:
        print('Не подходящая цепочка')


# def read_csv(file_path):
#     result_dict = {}
#     with open(file_path, newline='', encoding='utf-8') as csvfile:
#         csv_reader = csv.reader(csvfile, delimiter=';')
#         for row in csv_reader:
#             state = row[0]
#             transitions = [cell.split(',') if cell != '---' else ['---'] for cell in row[1:]]
#             result_dict[state] = transitions
#     return result_dict
# print(read_csv('moi_0011.csv'))


# def find_initial_head_position(tape):
#     for i in range(len(tape) - 1):
#         symbol = tape[i:i+2]
#         if symbol in {'q0', 'q1', 'q2', 'q3', 'q4'}:
#             if i + 2 < len(tape):
#                 return tape[i + 2]
#     return None