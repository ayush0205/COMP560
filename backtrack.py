import math
# read in input and initialize nodes and blocks
dimensions = input()  # read in dimensions
dimensions = int(dimensions)  # convert to integer
node_list = [[0] * dimensions for _ in range(dimensions)]  # nxn matrix of nodes
block_dict = dict()  # containing all the read in blocks
block_list = dict()  # dictionary with all the block contents given the block name
block_location = dict()  # dictionary with corresponding node locations given the block name


class Block:  # Block class that contains the block data : Letter, Operator, and Numeric Value
    def __init__(self, letter, value):
        self.block_name = letter
        value = str.strip(value)
        numeric = True
        l = 1
        while numeric: # method to parse out the operator and numeric value
            if str.isnumeric(value[0:l]):
                l = l + 1
                continue
            else:
                self.numeric_value = int(value[0:l - 1])
                self.operator = value[l - 1:len(value)]
                numeric = False


class Node:  # Node class that contains relevant information to a node
    def __init__(self, block):
        self.block = block  # block that the node is part of
        self.value = 0  # the value of the block, initialized to 0
        self.possible_values = list(range(1, dimensions+1))  # all possible values, initialized from 1 to n
        self.attempted_values = list()  # attempted values to make sure there is no repetition
        self.x = 0  # x position
        self.y = 0  # y position


def operateCheck(correct_val, values, operator):  # method to verify if contents of a block are accurate
    result = None
    if len(values) == 0:  # if no values provided in list, fail the check
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


def blockViolationCheck():  # method to verify if there are any violations in the blocks
    for b in block_list:  # go through all blocks
        values = []
        valid = True
        for location in block_location[b]:  # all node locations in a block
            decoded_x = (location - 1) % dimensions + 1
            decoded_y = math.ceil(location / dimensions)
            current_node = node_list[decoded_y - 1][decoded_x - 1]
            if current_node.value == 0:  # if node is not initialized, leave loop to verify if a block is accurate
                valid = False
                break
            else:
                values.append(current_node.value)
        if valid:  # if the block is complete, verify if the operation with the values produces the correct value
            if operateCheck(block_list[b].numeric_value, values , block_list[b].operator):
                continue  # if so, continue checking
            else:
                return False  # if not, fail test and cause backtrack
    return True  # if all pass, pass test


def applyConstraints(node):  # method to apply constraints based on attempted values and unique row/column constraints
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
    exclude = list(set(exclude).union(col_list))  # exclude union of attempted values and what is in other rows/columns
    exclude = list(set(exclude).union(row_list))
    node.possible_values = list(set(node.possible_values).difference(exclude))

    return node


for i in range(0, dimensions):  # load in the blocks into block dictionary and map a block to its node locations here
    current_line = input()
    for k in range(0, dimensions):
        node_list[i][k] = Node(current_line[k])
        if current_line[k] not in block_dict:
            block_dict[current_line[k]] = None
            block_location[current_line[k]] = [dimensions * i + (k + 1)]
        else:
            block_location[current_line[k]].append(dimensions * i + (k + 1))

for j in range(0, len(block_dict)):  # for each block, separate at the colons to get the operator and numeric value
    block_line = input()
    block_dict[block_line[0]] = block_line.split(":")[1]

for b in block_dict:  # load in a block object in the block_list with operator and numeric value
    block_list[b] = Block(b, block_dict[b])

for block in block_list:  # for each node in a block, load in the x and y for col/row checking
    for location in block_location[block]:
        decoded_x = (location - 1) % dimensions + 1
        decoded_y = math.ceil(location / dimensions)
        current_node = node_list[decoded_y - 1][decoded_x - 1]
        current_node.x = decoded_x
        current_node.y = decoded_y

i = 1  # initialize i at 1 since it is at location 1 of the matrix (locations go from 1-6 in row 1, 7-12 row 2, etc.)
node_count = 0  # counter for traversed nodes
while i <= dimensions*dimensions:  # for the entirety of the matrix
    node_count = node_count + 1
    decoded_x = (i - 1) % dimensions + 1
    decoded_y = math.ceil(i / dimensions)
    current_node = node_list[decoded_y - 1][decoded_x - 1]  # get the current node at the location i
    applyConstraints(current_node)
    if len(current_node.possible_values) != 0:  # if there are possible values after constraints
        attempted_value = current_node.possible_values[0]
        current_node.attempted_values.append(attempted_value)
        current_node.value = attempted_value
        if not blockViolationCheck():  # apply a block violation check after assignment, if this check fails
            failure = True
            for possibility in current_node.possible_values:  # iterate through all other possible values
                current_node.value = possibility
                if blockViolationCheck():  # if it passes on a specific possibility, continue on to next location
                    current_node.attempted_values.append(possibility)
                    failure = False
                    i = i + 1
                    break
            if failure:  # if not, backtrack and reset current and previous nodes
                current_node.possible_values = list(range(1, dimensions + 1))
                current_node.attempted_values.clear()
                current_node.value = 0
                temp = i - 1
                temp_decoded_x = (temp-1) % dimensions + 1
                temp_decoded_y = math.ceil(temp / dimensions)
                previous_node = node_list[temp_decoded_y - 1][temp_decoded_x - 1]
                previous_node.value = 0
                i = i - 1
        else:  # if block check is not violated, continue on
            i = i + 1
    else:  # if no more possible values, backtrack and reset current and previous nodes
        current_node.possible_values = list(range(1, dimensions + 1))
        current_node.attempted_values.clear()
        current_node.value = 0
        temp = i - 1
        temp_decoded_x = temp % dimensions + 1
        temp_decoded_y = math.ceil(temp / dimensions)
        previous_node = node_list[temp_decoded_y - 1][temp_decoded_x - 1]
        previous_node.value = 0
        i = i - 1


for i in range(0, dimensions):  # print out solved matrix and the node iterations
    for j in range(0, dimensions):
        print(node_list[i][j].value, end=" ")
    print()
print(node_count)
