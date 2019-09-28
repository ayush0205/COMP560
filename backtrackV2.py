import math, operator
# read in input and initialize nodes and blocks
dimensions = input()  # read in dimensions
dimensions = int(dimensions)  # convert to integer
node_list = [[0] * dimensions for _ in range(dimensions)]  # nxn matrix of nodes
block_dict = dict()  # containing all the read in blocks
block_list = dict()  # dictionary with all the block contents given the block name
block_location = dict()  # dictionary with corresponding node locations given the block name
value_list_on_block = dict()  # save the values that were used on previous blocks in case of backtrack


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
        self.parent = None  # parent node (node before)
        self.child = None  # child node (node after)
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


def applyConstraints(node, leaf): # method to apply constraints based on attempted values and unique row/column constraints
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
    if not leaf and node.possible_values:  # leaf input for if has a child node (if does not, need to iterate through all combinations)
        attempted_value = node.possible_values[0]
        node.attempted_values.append(attempted_value)
        node.value = attempted_value

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

for block in block_list:  # for each node in a block, load in the x and y for col/row checking as well as parent/child within a block
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

i = 0  # initialized i (block variable)
j = 0  # intialized j (node variable within a block)
backtrack = False   # boolean on if need to backtrack
value_list = []  # list of values to pass to operateCheck()
blocks = list(block_list.keys())  # block name list
node_count = 0  # counter for total nodes traversed
while i < len(block_list):  # for each block
    block_locations = block_location[blocks[i]]
    current_block = block_list[blocks[i]]  # for the current block
    if backtrack:  # if need to backtrack, iterate to previous block and load in the value_list from previous successful iteration
        i = i - 1
        block_locations = block_location[blocks[i]]
        current_block = block_list[blocks[i]]
        value_list = value_list_on_block[current_block.block_name]
        value_list.pop()  # pop off the last value as we are modifying this
        j = len(block_locations) - 1  # go to the last node on the block so we can backtrack further if needed
        backtrack = False  # set backtrack to false
    while j < len(block_locations):  # for all nodes that correspond to a block
        current_location = block_locations[j]
        decoded_x = (current_location - 1) % dimensions + 1
        decoded_y = math.ceil(current_location / dimensions)
        current_node = node_list[decoded_y - 1][decoded_x - 1]
        if j != len(block_locations)-1:  # for those nodes that have children (not last node in block)
            applyConstraints(current_node, False)
            if len(current_node.possible_values) == 0:  # if no more possibilities
                current_node.possible_values = list(range(1, dimensions + 1))
                current_node.attempted_values.clear()
                current_node.value = 0
                if j == 0:  # at the top-most node of a block, need to go to previous block since possibilities are exhausted
                    backtrack = True
                    break
                else:  # are at mid-level nodes, so simply go back a node within a block after resetting values for current and parent nodes
                    if current_node.parent.value in value_list:
                        value_list.remove(current_node.parent.value)
                    current_node.parent.value = 0
                    j = j - 1
            else:  # if possibilities remain, simply append to value_list and go to next node in block
                value_list.append(current_node.value)
                j = j + 1
        else:  # if last node (node with no children) in block
            failure = True  # initialize failure to true to backtrack if this does not work
            applyConstraints(current_node, True)
            for possibility in current_node.possible_values:  # check if any possibility works
                value_list.append(possibility)
                if operateCheck(current_block.numeric_value, value_list, current_block.operator):  # if it does, go to next block
                    current_node.value = possibility
                    current_node.attempted_values.append(possibility)
                    value_list_on_block[current_block.block_name] = value_list.copy()  # save value_list in case we need to backtrack (used for operateCheck)
                    value_list = []
                    i = i + 1
                    j = 0
                    failure = False
                    break
                else:  # if possibility does not work, remove it from value_list and continue loop
                    value_list.remove(possibility)
            if failure:  # if possibilities do not work, must go back up to mid-level nodes after resetting current and parent nodes
                current_node.possible_values = list(range(1, dimensions + 1))
                current_node.attempted_values.clear()
                current_node.value = 0
                if current_node.parent.value in value_list:
                    value_list.remove(current_node.parent.value)
                current_node.parent.value = 0
                j = j - 1
            else:
                break  # if not failure, done with this block, break away
        node_count = node_count + 1  # increment node_count at end


for i in range(0, dimensions):  # print out solved matrix and the node iterations
    for j in range(0, dimensions):
        print(node_list[i][j].value, end=" ")
    print()
print(node_count)





