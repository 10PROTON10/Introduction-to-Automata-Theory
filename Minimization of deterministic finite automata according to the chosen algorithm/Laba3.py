import csv


def read_csv(filename):
    data = {}

    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')

        for row in csv_reader:
            key, index, value = row
            index = int(index)

            if key not in data:
                data[key] = [[], []]

            data[key][index].append(value)

    return data


def generate_pairs(DFA):
    new = []
    matrix = list(DFA)

    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            new.append(matrix[i] + matrix[j])

    return new


def process_states(DFA, new, condition):
    for _ in range(2):
        for i in new:
            if not condition[i]:
                continue

            paw = list(i)
            first = DFA[paw[0]][0] + DFA[paw[1]][0]
            second = DFA[paw[0]][1] + DFA[paw[1]][1]

            for part in [first, second]:
                retr = ''.join(part)
                if part.count(part[0]) == 1:
                    try:
                        if not condition[retr]:
                            condition[i] = False
                            break
                    except:
                        part[0], part[1] = part[1], part[0]
                        retr = ''.join(part)
                        if condition.get(retr) is False:
                            condition[i] = False
                            break
                elif condition.get(retr) is False:
                    condition[i] = False
                    break

    return condition


# выполняет обновление DFA путем объединения двух состояний и перерасчета переходов между ними
def update(DFA, i):
    state1, state2 = i[0], i[1]
    transitions1 = DFA[state1]
    transitions2 = DFA[state2]

    new_state = state1 + state2
    new_transitions = [[], []]

    for symbol in [0, 1]:
        targets1 = transitions1[symbol]
        targets2 = transitions2[symbol]
        new_targets = list(set(targets1 + targets2))

        new_transitions[symbol] = new_targets
    del DFA[state1]
    del DFA[state2]
    DFA[new_state] = new_transitions


# выполняет удаление недостижимых состояний в детерминированном конечном автомате
def up(DFA):
    state_set = set(DFA.keys())

    for state in DFA:
        for symbol in [0, 1]:
            target = DFA[state][symbol][0]
            if target not in state_set:
                for existing_state in state_set:
                    if target in existing_state:
                        DFA[state][symbol] = [existing_state]


def write(DFA):
    with open('DFA1.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        for state in DFA:
            for symbol in [0, 1]:
                target_states = ",".join(DFA[state][symbol])
                writer.writerow([state, symbol, target_states])


if __name__ == "__main__":
    filename = 'DFA.csv'
    DFA = read_csv(filename)
    pairs = generate_pairs(DFA)
    admitting_states = [state for state in DFA.keys() if "*" in state]
    condition = {i: False if admitting_states[0] in i else True for i in pairs}
    xz = process_states(DFA, pairs, condition)
    print(DFA)
    print(pairs)
    print(condition)
    print(xz)
    for i in condition:
        if condition[i] is False:
            continue
        else:
            update(DFA, i)

    up(DFA)
    print(DFA)
    write(DFA)







