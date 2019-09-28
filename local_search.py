import math, random
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


class Node:
    def __init__(self, block):  # class to maintain a node's block and value
        self.block = block
        self.value = 0


def operateCheck(correct_val, values, operator):  # method to verify if contents of a block are accurate
    result = None
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


def swap(swap_type, num1, num2, current_nodes):  # method that swaps 2 rows or 2 columns given input
    temp_list = [0] * dimensions
    copy_list = current_nodes.copy()
    if swap_type == "row":
        for t in range(0, dimensions):
            temp_list[t] = copy_list[num1][t]
            copy_list[num1][t] = copy_list[num2][t]
            copy_list[num2][t] = temp_list[t]
    elif swap_type == "column":
        for t in range(0, dimensions):
            temp_list[t] = copy_list[t][num1]
            copy_list[t][num1] = copy_list[t][num2]
            copy_list[t][num2] = temp_list[t]
    return copy_list


def violationCheck(node_check):  # a method that checks the number of violated block constraints, less is better
    violations = []
    for letter in block_location:
        points = block_location[letter]
        value_list = []
        for p in points:
            decoded_x = (p - 1) % dimensions + 1  # to get the column
            decoded_y = math.ceil(p / dimensions)  # to get the row
            value_list.append(node_check[decoded_y - 1][decoded_x - 1].value)
        if not operateCheck(block_list[letter].numeric_value, value_list, block_list[letter].operator):
            violations.append(letter)
    return violations


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

for i in range(0, dimensions):
    for j in range(0, dimensions):
        node_list[i][j].value = (i + j) % dimensions + 1  # initial unique row and column assignment for local search
        #print(node_list[i][j].value, end=" ")  # toggle with below line to see initial assignment
    #print()

curr_violations = violationCheck(node_list)

# randomized swap of 2 columns or 2 rows, if the swap keeps
# the number of violations the same or decreases, keep continuing
iters = 0  # counted/ effective iterations
total_iters = 0
original_node_list = node_list
while len(curr_violations) > 0:
    swap_type = None
    rand_swap = random.randint(0, 1)  # randomly choose between row or column swap
    if rand_swap == 0:
        swap_type = "row"
    elif rand_swap == 1:
        swap_type = "column"
    swap_num_1 = random.randint(0, dimensions - 1)  # choose row/column number to swap
    swap_num_2 = random.randint(0, dimensions - 1)
    while swap_num_1 == swap_num_2:
        swap_num_2 = random.randint(0, dimensions - 1)  # choose diff row/column number to swap with if same
    swapped_list = swap(swap_type, swap_num_1, swap_num_2, node_list)
    swapped_violations = violationCheck(swapped_list)
    if len(swapped_violations) < len(curr_violations):
        #print(swapped_violations)  #  toggle to see the violated blocks
        #print(total_iters)  # toggle to see total iterations
        iters = iters + 1
        node_list = swapped_list
        curr_violations = swapped_violations
    if total_iters > 100000:  # since this is local search, solution not guaranteed, in this case reset to initial state when total iterations exceed 100000
        print("restart")
        total_iters = 0
        iters = 0
        node_list = original_node_list
        curr_violations = violationCheck(node_list)
    total_iters = total_iters + 1

for i in range(0, dimensions):  # print out solved matrix and the swap iterations
    for j in range(0, dimensions):
        print(node_list[i][j].value, end=" ")
    print()
print(iters)
