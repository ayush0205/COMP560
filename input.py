dimensions = input()
dimensions = int(dimensions)
node_list = [[0]*dimensions for _ in range(dimensions)]
print(node_list)
block_dict = dict()
block_list = dict()

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
                self.numeric_value = value[0:l-1]
                self.operator = value[l-1:len(value)]
                numeric = False

class Node:
    def __init__(self, block):
        self.block = block
        self.value = 0

for i in range(0, dimensions):
    current_line = input()
    for k in range(0, dimensions):
        node_list[i][k] = Node(current_line[k])
        if current_line[k] not in block_dict:
            block_dict[current_line[k]] = None
print(node_list)
for j in range(0, len(block_dict)):
    block_line = input()
    block_dict[block_line[0]] = block_line.split(":")[1]
#print(block_dict)

for b in block_dict:
    block_list[b] = Block(b,block_dict[b])
    #print(block_list[b].operator, block_list[b].numeric_value, block_list[b].block_name)

#print(block_list)
