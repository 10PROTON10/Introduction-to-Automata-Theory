import networkx as nx


class Vertex:
    def __init__(self):
        # Атрибуты узла дерева
        self.left, self.right, self.root, self.value = None, None, None, None

    def new_left(self):
        # Создание нового левого потомка
        self.left = Vertex()
        self.left.root = self
        return self.left

    def new_right(self):
        # Создание нового правого потомка
        self.right = Vertex()
        self.right.root = self
        return self.right

    def new_right_root(self):
        # Создание нового правого потомка и нового корня
        self.root = Vertex()
        self.root.left = self
        return self.root

    def __repr__(self):
        # Представление узла в виде строки (используется для отладки)
        return str(self.value)


def regular_symbols(regexp):
    # Функция, добавляющая точки для конкатенации в регулярном выражении
    T = set(filter(lambda item: not item in operators | brackets, regexp))
    filled_regexp = ""

    for i, item in enumerate(regexp):
        filled_regexp += item
        if i + 1 < len(regexp) and regexp[i] in T | set('*)') and regexp[i + 1] in T | set('('):
            filled_regexp += '.'

    return filled_regexp


def build_tree(regexp):
    # Построение синтаксического дерева из регулярного выражения
    root = Vertex()
    current = root.new_left()

    T = set(filter(lambda item: not item in operators | brackets, regexp))
    filled_regexp = regular_symbols(regexp)

    for token in filled_regexp:
        if token == '(':
            current = current.new_left()
            continue
        if token == ')':
            current = current.root or current.new_right_root()
            continue
        if token in T:
            current.value = token
            current = current.root or current.new_right_root()
            continue
        if token in set('.|'):
            if current.value:
                current = current.new_right_root()
            current.value = token
            current = current.new_right()
            continue
        if token == '*':
            if current.value:
                current = current.new_right_root()
            current.value = token

    return current


def vertex_check(node):
    # Проверка типа узла для вычисления функции followpos
    if node is None:
        return True

    if node.value == '|':
        return vertex_check(node.left) or vertex_check(node.right)

    if node.value == '.':
        return vertex_check(node.left) and vertex_check(node.right)

    if node.value == '*':
        return True

    return False


def fill_tree_pos(root):
    # Заполнение множеств firstpos и lastpos для каждого узла дерева
    global i

    if root is None:
        return

    fill_tree_pos(root.left)
    fill_tree_pos(root.right)

    root.firstpos = set()
    root.lastpos = set()

    if root.value in operators:
        if root.value == '|':
            root.firstpos |= root.left.firstpos | root.right.firstpos
            root.lastpos |= root.left.lastpos | root.right.lastpos
        if root.value == '.':
            if vertex_check(root.left):
                root.firstpos |= root.left.firstpos | root.right.firstpos
            else:
                root.firstpos |= root.left.firstpos

            if vertex_check(root.right):
                root.lastpos |= root.left.lastpos | root.right.lastpos
            else:
                root.lastpos |= root.right.lastpos
        if root.value == '*':
            root.firstpos |= root.left.firstpos
            root.lastpos |= root.left.lastpos
    else:
        root.firstpos.add(i)
        root.lastpos.add(i)
        i += 1


def filling_transitions(root, followpos):
    # Заполнение функции followpos для каждого узла дерева
    if root is None:
        return

    filling_transitions(root.left, followpos)
    filling_transitions(root.right, followpos)

    if root.value == '.':
        for i in root.left.lastpos:
            followpos[i - 1] |= root.right.firstpos

    if root.value == '*':
        for i in root.left.lastpos:
            followpos[i - 1] |= root.left.firstpos


def build_NKA(q0, regexp, followpos):
    # Построение НКА по множествам firstpos и followpos
    positions = list(filter(lambda item: not item in operators | brackets, regexp))

    F = list()
    Q = set()
    unhandled = set()

    unhandled.add(tuple(q0))

    while unhandled:
        current = unhandled.pop()
        if not current in Q:
            for i in current:
                next_state = followpos[i - 1]
                F.append((current, positions[i - 1], tuple(next_state)))
                unhandled.add(tuple(next_state))
        Q.add(current)

    return Q, F


# Операторы и скобки в регулярных выражениях
operators = set('.*|')
brackets = set('()')
i = 1

# Регулярное выражение
regexp = '(ab|b)*(b|a)#'

# Построение синтаксического дерева
root = build_tree(regexp)

# Вычисление firstpos и lastpos для узлов дерева
fill_tree_pos(root)

# Инициализация followpos
followpos = [set() for i in range(len(list(filter(lambda item: not item in operators | brackets, regexp))))]

# Заполнение функции followpos
filling_transitions(root, followpos)

# Построение НКА
Q, F = build_NKA(root.firstpos, regexp, followpos)

# Визуализация НКА с использованием библиотеки NetworkX
Graph = nx.DiGraph()
for i in range(len(F)):
    for j in range(len(F[i][0])):
        for k in range(len(F[i][2])):
            Graph.add_edges_from([(F[i][0][j], F[i][2][k])], weight=ord(F[i][1]))
            if F[i][1] != '#':
                print("q{0} переход q{1} по {2}".format(str(F[i][0][j]), str(F[i][2][k]), F[i][1]))







