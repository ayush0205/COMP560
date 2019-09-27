import math, operator
# read in input and initialize nodes and blocks
dimensions = input()
dimensions = int(dimensions)
node_list = [[0] * dimensions for _ in range(dimensions)]
block_dict = dict()
block_list = dict()
block_location = dict()
last_node_on_block = dict()
value_list_on_block = dict()
block_stack = list()
backtrack_stack = list()
first_node_on_block = dict()


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

block_scores = dict()
sorted_blocks = dict()
for block in block_location:
    length_score = len(block_location[block])*-1
    operator_symbol = block_list[block].operator
    operator_score = 0
    if operator_symbol == "*" or "/":
        operator_score = -1
    score = length_score + operator_score
    block_scores[block] = score

block_scores = sorted(block_scores.items(), key=operator.itemgetter(1))

for i in range(0,len(block_scores)):
    sorted_blocks[block_scores[i][0]] = block_scores[i][1]

i = 0
j = 0
backtrack = False
value_list = []
blocks = list(block_list.keys())
node_count = 0
while i < len(block_list):
    block_locations = block_location[blocks[i]]
    current_block = block_list[blocks[i]]
    if backtrack:
        i = i - 1
        block_locations = block_location[blocks[i]]
        current_block = block_list[blocks[i]]
        value_list = value_list_on_block[current_block.block_name]
        value_list.pop()
        j = len(block_locations) - 1
        backtrack = False
    while j < len(block_locations):
        current_location = block_locations[j]
        decoded_x = (current_location - 1) % dimensions + 1
        decoded_y = math.ceil(current_location / dimensions)
        current_node = node_list[decoded_y - 1][decoded_x - 1]
        if j != len(block_locations)-1:
            applyConstraints(current_node, False)
            if len(current_node.possible_values) == 0:
                current_node.possible_values = list(range(1, dimensions + 1))
                current_node.attempted_values.clear()
                current_node.value = 0
                if j == 0:
                    backtrack = True
                    break
                else:
                    if current_node.parent.value in value_list:
                        value_list.remove(current_node.parent.value)
                    current_node.parent.value = 0
                    j = j - 1
            else:
                value_list.append(current_node.value)
                j = j + 1
        else:
            failure = True
            applyConstraints(current_node, True)
            for possibility in current_node.possible_values:
                value_list.append(possibility)
                if operateCheck(current_block.numeric_value, value_list, current_block.operator):
                    current_node.value = possibility
                    current_node.attempted_values.append(possibility)
                    value_list_on_block[current_block.block_name] = value_list.copy()
                    value_list = []
                    i = i + 1
                    j = 0
                    failure = False
                    break
                else:
                    value_list.remove(possibility)
            if failure:
                current_node.possible_values = list(range(1, dimensions + 1))
                current_node.attempted_values.clear()
                current_node.value = 0
                if current_node.parent.value in value_list:
                    value_list.remove(current_node.parent.value)
                current_node.parent.value = 0
                j = j - 1
            else:
                break
        node_count = node_count + 1


for i in range(0, dimensions):
    for j in range(0, dimensions):
        print(node_list[i][j].value, end=" ")
    print()
print(node_count)





