import math, random

dimensions = input()
dimensions = int(dimensions)
node_list = [[0]*dimensions for _ in range(dimensions)]
#print(node_list)
block_dict = dict()
block_list = dict()
block_location = dict()

class Block:
    def __init__(self, letter, value):
        self.block_name = letter
        value = str.strip(value)
        numeric = True
        l = 1
        while numeric:
            if str.isnumeric(value[0:l]):
                l = l+1
                continue
            else:
                self.numeric_value = int(value[0:l-1])
                self.operator = value[l-1:len(value)]
                numeric = False

class Node:
    def __init__(self, block):
        self.block = block
        self.value = 0

def operateCheck(correct_val, values, operator):
    result = None
    if operator == "+":
        for v in range(0,len(values)):
            if v == 0:
                result = values[v]
            else:
                result = result + values[v]
    elif operator == "-":
        result = abs(values[0]-values[1])
    elif operator == "*":
        for v in range(0, len(values)):
            if v == 0:
                result = values[v]
            else:
                result = result * values[v]
    elif operator == "/":
        result = max(values[0]/values[1],values[1]/values[0])
    return result == correct_val

def swap(swap_type, num1, num2, current_nodes):
    temp_list = [0,0,0,0,0,0]
    copy_list = current_nodes.copy()
    #print(temp_list[0])
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

def violationCheck(node_check):
    violations = []
    for letter in block_location:
        points = block_location[letter]
        value_list = []
        for p in points:
            decoded_x = (p-1) % 6 + 1
            decoded_y = math.ceil(p/6)
            value_list.append(node_check[decoded_y-1][decoded_x-1].value)
        if not operateCheck(block_list[letter].numeric_value, value_list, block_list[letter].operator):
            violations.append(letter)
    print(violations)
    return violations

for i in range(0, dimensions):
    current_line = input()
    for k in range(0, dimensions):
        node_list[i][k] = Node(current_line[k])
        if current_line[k] not in block_dict:
            block_dict[current_line[k]] = None
            block_location[current_line[k]] = [6 * i + (k+1)]
        else:
            block_location[current_line[k]].append(6 * i + (k+1))
print(node_list)
print(block_location)
for j in range(0, len(block_dict)):
    block_line = input()
    block_dict[block_line[0]] = block_line.split(":")[1]
#print(block_dict)

for b in block_dict:
    block_list[b] = Block(b,block_dict[b])
    #print(block_list[b].operator, block_list[b].numeric_value, block_list[b].block_name)

#print(block_list)

for i in range(0,dimensions):
    for j in range(0,dimensions):
        node_list[i][j].value = (i + j) % 6 + 1 #initial unique row and column assignment for local search
        print(node_list[i][j].value, end=" ")
    print()

curr_violations = violationCheck(node_list)

# randomized swap of 2 columns or 2 rows, if the swap keeps
# the number of violations the same or decreases, keep continuing
iters = 0
while len(curr_violations) > 0:
    swap_type = None
    rand_swap = random.randint(0,1)
    if rand_swap == 0:
        swap_type = "row"
    elif rand_swap == 1:
        swap_type = "column"
    swap_num_1 = random.randint(0,5)
    swap_num_2 = random.randint(0,5)
    while swap_num_1 == swap_num_2:
        swap_num_2 = random.randint(0,5)
    swapped_list = swap(swap_type, swap_num_1, swap_num_2, node_list)
    swapped_violations = violationCheck(swapped_list)
    if len(swapped_violations) < len(curr_violations):
        iters = iters + 1
        node_list = swapped_list
        curr_violations = swapped_violations

print(iters)
for i in range(0,dimensions):
    for j in range(0,dimensions):
        print(node_list[i][j].value, end=" ")
    print()
