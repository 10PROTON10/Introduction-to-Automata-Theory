import csv


def read_csv(file_path):
    automaton_description = []

    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            current_state, input_symbol, stack_top = row[0].split(',')
            next_state, stack_change = row[1].split(',')

            rule = {
                'current_state': current_state,
                'input_symbol': input_symbol,
                'stack_top': stack_top,
                'next_state': next_state,
                'stack_change': stack_change
            }

            automaton_description.append(rule)

    return automaton_description


def process_input_string(input_string, automaton_rules):
    stack = ['S']  # Инициализация стека с дном 'z'
    current_state = 'q0'  # Начальное состояние автомата
    symbol = input_string[0]  # Берем первый символ из input_string

    tree = [{'state': current_state, 'symbol': symbol, 'stack': stack.copy()}]  # Дерево разбора

    while stack:
        if current_state == 'q1' and stack == ['z']:
            print('Строка подходит')
            print_tree(tree)
            break

        # Сохраняем текущее состояние перед выполнением правила
        prev_state = current_state

        if input_string == ['e']:
            stack = ['z']

        # Находим правило для текущего состояния и символа на входе
        rule = next((r for r in automaton_rules if r['current_state'] == current_state
                     and r['input_symbol'] == symbol and r['stack_top'] == stack[0]), None)

        if rule:
            current_state = rule['next_state']
            stack.pop(0)
            stack = list(rule['stack_change']) + stack

            # Проверяем, осталось ли состояние 'q0' до и после выполнения правила
            if prev_state == 'q0' and current_state == 'q0':
                # Берем следующий символ из input_string
                if input_string:
                    input_string = input_string[1:]
                    if not input_string:
                        input_string = ['e']
                    else:
                        symbol = input_string[0]
                else:
                    break
            # tree.append({'state': current_state, 'symbol': symbol, 'stack': stack.copy()})

        else:
            rule = next((r for r in automaton_rules if r['current_state'] == current_state
                         and r['input_symbol'] == 'e' and r['stack_top'] == stack[0]), None)
            if rule:
                current_state = rule['next_state']
                if current_state == 'q1' and stack == ['z'] and symbol != 'c':
                    print('Строка не подходит')
                    break
                stack.pop(0)

                if rule['stack_change'] == 'S':
                    stack = ['S']
                elif rule['stack_change'] == 'z':
                    stack = list(rule['stack_change']) + stack
                    # Добавляем информацию о шаге в дерево разбора
                    tree.append({'state': current_state, 'symbol': symbol, 'stack': stack.copy()})
                else:
                    stack = list(symbol) + ['S']
                    # Добавляем информацию о шаге в дерево разбора
                    tree.append({'state': current_state, 'symbol': symbol, 'stack': stack.copy()})

                # Проверяем, осталось ли состояние 'q0' до и после выполнения правила
                if prev_state == 'q0' and current_state == 'q0':
                    # Берем следующий символ из input_string
                    if input_string:
                        input_string = input_string[1:]
                        if not input_string:
                            input_string = ['e']
                        else:
                            symbol = input_string[0]
                    else:
                        break
            # tree.append({'state': current_state, 'symbol': symbol, 'stack': stack.copy()})
            else:
                print('Строка не подходит')
                break


def print_tree(tree):
    print("Дерево разбора:")
    for step in tree:
        print(f"State: {step['state']}, Symbol: {step['symbol']}, Stack: {step['stack']}")


if __name__ == "__main__":
    file_path = 'vxod.csv'
    automaton_rules = read_csv(file_path)
    input_string = input("Введите цепочку из a,b,c: ")
    process_input_string(input_string, automaton_rules)

