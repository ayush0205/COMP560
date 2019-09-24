import math, sys
# read in input and initialize nodes and blocks
dimensions = input()
dimensions = int(dimensions)
node_list = [[0] * dimensions for _ in range(dimensions)]
block_dict = dict()
block_list = dict()
block_location = dict()
row_dict = dict()
col_dict = dict()
last_node_on_block = dict()
value_list_on_block = dict()
block_stack = list()
backtrack_stack = list()
first_node_on_block = dict()
#sys.setrecursionlimit(100000)
global traversal_count
traversal_count = 0


class Block:
    def __init__(self, letter, value):
        self.block_name = letter
        value = str.strip(value)
        numeric = True
        l = 1
        while numeric:
            if str.isnumeric(value[0:l]):
                l = l + 1
                continue
            else:
                self.numeric_value = int(value[0:l - 1])
                self.operator = value[l - 1:len(value)]
                numeric = False


class Node:
    def __init__(self, block):
        self.block = block
        self.value = 0
        self.possible_values = list(range(1, dimensions+1))
        self.attempted_values = list()
        self.parent = None
        self.child = None
        self.x = 0
        self.y = 0


def operateCheck(correct_val, values, operator):
    result = None
    if len(values) == 0:
        return False
    if operator == "+":
        for v in range(0, len(values)):
            if v == 0:
                result = values[v]
            else:
                result = result + values[v]
    elif operator == "-":
        result = abs(values[0] - values[1])
    elif operator == "*":
        for v in range(0, len(values)):
            if v == 0:
                result = values[v]
            else:
                result = result * values[v]
    elif operator == "/":
        result = max(values[0] / values[1], values[1] / values[0])
    else:  # no operator case
        result = values[0]
    return result == correct_val


def applyConstraints(node, leaf):
    exclude = node.attempted_values
    x = node.x
    y = node.y
    row_list = list()
    col_list = list()
    for i in range(0, dimensions):
        if node_list[i][x-1].value != 0:
            col_list.append(node_list[i][x-1].value)
        if node_list[y-1][i].value != 0:
            row_list.append(node_list[y-1][i].value)
    exclude = list(set(exclude).union(col_list))
    exclude = list(set(exclude).union(row_list))
    node.possible_values = list(set(node.possible_values).difference(exclude))
    if not leaf and node.possible_values:
        attempted_value = node.possible_values[0]
        node.attempted_values.append(attempted_value)
        node.value = attempted_value

    return node


def traverse(block_object, node, values):
    if node.child is not None and node.possible_values:
        # apply constraints and choose first non-constrained value
        node = applyConstraints(node, False)
        # pass function on to child of current_node
        if len(node.possible_values) == 0 and node.parent is not None:
            # backtrack to parent
            node.possible_values = list(range(1, dimensions + 1))
            node.attempted_values.clear()
            if node.parent.value in values:
                values.remove(node.parent.value)
            node.parent.value = 0
            node.value = 0
            traverse(block_object, node.parent, values)
        elif len(node.possible_values) == 0 and node.parent is None:
            # backtrack to previous block
            node.possible_values = list(range(1, dimensions + 1))
            node.attempted_values.clear()
            node.value = 0
            values.clear()
            new_block_object = block_stack.pop()
            values = value_list_on_block[new_block_object]
            values.pop()
            backtrack_stack.append(block_object.block_name)
            first_node_on_block[block_object.block_name] = node
            traverse(block_list[new_block_object], last_node_on_block[new_block_object], values)
        else:
            values.append(node.value)
            traverse(block_object, node.child, values)
    elif node.child is None and node.possible_values:
        # apply constraints and iterate through non-constrained values
        node = applyConstraints(node, True)
        if len(node.possible_values) == 0 and node.parent is not None:
            # backtrack to parent
            node.possible_values = list(range(1, dimensions + 1))
            node.attempted_values.clear()
            if node.parent.value in values:
                values.remove(node.parent.value)
            node.parent.value = 0
            node.value = 0
            traverse(block_object, node.parent, values)
        elif len(node.possible_values) == 0 and node.parent is None:
            # backtrack to previous block
            node.possible_values = list(range(1, dimensions + 1))
            node.attempted_values.clear()
            node.value = 0
            values.clear()
            new_block_object = block_stack.pop()
            values = value_list_on_block[new_block_object]
            values.pop()
            backtrack_stack.append(block_object.block_name)
            first_node_on_block[block_object.block_name] = node
            traverse(block_list[new_block_object], last_node_on_block[new_block_object], values)
        else:
            not_a_fail = False
            for possibility in node.possible_values:
                values.append(possibility)
                if operateCheck(block_object.numeric_value, values, block_object.operator):
                    node.value = possibility
                    node.attempted_values.append(possibility)
                    last_node_on_block[block_object.block_name] = node
                    value_list_on_block[block_object.block_name] = values.copy()
                    block_stack.append(block_object.block_name)
                    if len(backtrack_stack) == 0:
                        return
                    else:
                        view = node_list
                        forward_block = backtrack_stack.pop()
                        values.clear()
                        traverse(block_list[forward_block], first_node_on_block[forward_block], values)
                        not_a_fail = True
                        break
                else:
                    values.remove(possibility)
            # if none work, backtrack by calling function on parent
            if node.parent.value in values and not not_a_fail:
                values.remove(node.parent.value)
            if not not_a_fail:
                node.parent.value = 0
                node.value = 0
                node.attempted_values.clear()
                node.possible_values = list(range(1, dimensions+1))
                traverse(block_object, node.parent, values)


for i in range(0, dimensions):
    current_line = input()
    for k in range(0, dimensions):
        node_list[i][k] = Node(current_line[k])
        if current_line[k] not in block_dict:
            block_dict[current_line[k]] = None
            block_location[current_line[k]] = [dimensions * i + (k + 1)]
        else:
            block_location[current_line[k]].append(dimensions * i + (k + 1))

for j in range(0, len(block_dict)):
    block_line = input()
    block_dict[block_line[0]] = block_line.split(":")[1]

for b in block_dict:
    block_list[b] = Block(b, block_dict[b])

for block in block_list:
    parent = None
    child = None
    for location in block_location[block]:
        decoded_x = (location - 1) % dimensions + 1
        decoded_y = math.ceil(location / dimensions)
        current_node = node_list[decoded_y - 1][decoded_x - 1]
        current_node.x = decoded_x
        current_node.y = decoded_y
        if parent is not None:
            parent.child = current_node
        current_node.parent = parent
        parent = current_node


for block in block_list:
    value_list = []
    first_location = block_location[block][0]
    decoded_x = (first_location - 1) % dimensions + 1
    decoded_y = math.ceil(first_location / dimensions)
    current_node = node_list[decoded_y - 1][decoded_x - 1]
    #not_a_fail = False
    traverse(block_list[block], current_node, value_list)
    traversal_count = traversal_count + 1


for i in range(0, dimensions):
    for j in range(0, dimensions):
        print(node_list[i][j].value, end=" ")
    print()






