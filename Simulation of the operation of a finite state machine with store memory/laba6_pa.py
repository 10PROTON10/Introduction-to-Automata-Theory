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
    stack = ['z']  # Инициализация стека с дном 'z'
    current_state = 'q0'  # Начальное состояние автомата
    stack_history = []  # Список для хранения состояний стека
    state_history = []  # Список для хранения состояний
    input_symbols_taken = []  # Список для хранения символов, взятых из входной строки

    for symbol in input_string:
        # Сохраняем текущее состояние, состояние стека и символ из входной строки перед применением правила
        stack_history.append(stack.copy())
        state_history.append(current_state)
        input_symbols_taken.append(symbol)

        # Находим правило для текущего состояния и символа на входе
        rule = next((r for r in automaton_rules if r['current_state'] == current_state
                     and r['input_symbol'] == symbol and r['stack_top'] == stack[0]), None)

        if rule:
            current_state = rule['next_state']
            stack.pop(0)
            stack = list(rule['stack_change']) + stack
        else:
            print("Цепочка не является допускающей.")
            return False, current_state, stack_history, state_history, input_symbols_taken

    # Проверяем, достигнуто ли конечное состояние
    if current_state == 'q2' and stack[-1] == 'z':
        return True, current_state, stack_history, state_history, input_symbols_taken
    else:
        return False, current_state, stack_history, state_history, input_symbols_taken



def process_stack_history(stack_history, state_history, input_symbols_taken, automaton_rules):
    alstroka = input_symbols_taken
    # Проходим по состояниям и состояниям стека в обратном порядке
    for i, (stack_state, state) in enumerate(zip(reversed(stack_history), reversed(state_history)), start=1):
        # Копируем стек для применения правил
        stack = stack_state.copy()
        current_state = state
        vsyastroka = alstroka[-i:]  # Берем последние i символов из alstroka
        # Пробуем применить правила для текущего состояния стека
        while stack:
            # Пытаемся применить правило для текущего состояния, символа и верхнего символа стека
            rule = next((r for r in automaton_rules if r['current_state'] == current_state
                         and r['input_symbol'] == 'e' and r['stack_top'] == stack[0]), None)

            if rule:
                # Применяем правило: изменяем состояние и символ на вершине стека
                current_state = rule['next_state']
                stack.pop(0)
                if rule['stack_change'] != 'e':
                    stack = list(rule['stack_change']) + stack
                # Если достигнуто конечное состояние 'q2', завершаем процесс
                if current_state == 'q2' and vsyastroka == []:
                    print("Цепочка является допускающей.")
                    return True
                # Если не достигнуто конечное состояние 'q2', а строка закончилась
                if current_state != 'q2' and vsyastroka == []:
                    break
            else:
                # Если не достигнуто конечное состояние 'q2', а строка закончилась
                if current_state != 'q2' and vsyastroka == []:
                    break
                rule = next((r for r in automaton_rules if r['current_state'] == current_state
                             and r['input_symbol'] == vsyastroka[0] and r['stack_top'] == stack[0]), None)
                if rule:
                    current_state = rule['next_state']
                    stack.pop(0)
                    if rule['stack_change'] != 'e':
                        stack = list(rule['stack_change']) + stack
                    vsyastroka = vsyastroka[1:]
                    # Если достигнуто конечное состояние 'q2', завершаем процесс
                    if current_state == 'q2' and vsyastroka == []:
                        print("Цепочка является допускающей.")
                        return True
                else:
                    # Если правило не найдено, переходим к следующему состоянию стека
                    break

        # Если достигнуто конечное состояние 'q2', завершаем процесс
        if current_state == 'q2' and vsyastroka == []:
            print("Цепочка является допускающей.")
            return True

    # Если не удалось достичь 'q2' и закончились состояния стека, выводим сообщение
    print("Цепочка не является допускающей.")
    return False


if __name__ == "__main__":
    file_path = 'vxod.csv'
    automaton_rules = read_csv(file_path)
    input_string = input("Введите цепочку из 0 и 1: ")
    result, current_state, stack_history, state_history, input_symbols_taken = process_input_string(input_string, automaton_rules)
    print('stack_history: ', stack_history)
    print('state_history: ', state_history)
    print('input_symbols_taken: ', input_symbols_taken)
    if result:
        print("Цепочка является допускающей.")
    else:
        process_stack_history(stack_history, state_history, input_symbols_taken, automaton_rules)
