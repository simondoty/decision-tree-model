# Python Implementation of a two class decision tree

import copy

column_details = [["binary"], ["log_distance"], ["binary"]]
inputfile = 'sample_input.txt'
data=dict()
f = open('sample_input.txt')
for line in iter(f):
	line = line.replace('\n', "")
	line_array = line.split(',')
	line_array = map(int, line_array)
	fid = int(line_array[0])
	attr_list = line_array[1:]
	data[fid] = attr_list
f.close()

data_keys = list(data.keys())
col_nums = list() 
for i in range(0, len(data[data_keys[0]]) - 1):
	col_nums.append(i)

# Node class
class d_node:
	def __init__(self, records, col_nums):
		self.records = records
		self.col_nums = col_nums
		self.gini = None
		self.split_col = None
		self.is_leaf = False
		self.tchild = None
		self.fchild = None
		self.classification = None
		self.split_value = None

# Decision Tree class
class d_tree:
	def __init__(self, records, col_ids):
		self.root = d_node(records, col_ids)

def calculateGini(records):		
	total = float(len(records))
	if total == 0: return 0
	num_class_1 = 0
	for record in records:
		if data[record][-1] == 1: num_class_1 = num_class_1 + 1
	num_class_0 = total - num_class_1
	gini = 1 - (num_class_1 / total)**2 - (num_class_0 / total)**2
	return gini

def returnSplitGini(records, col_split):
	true_set= list()
	false_set= list()
	return_set= tuple()
	records_length = float(len(records))

	if column_details[col_split][0] == "binary":
		for record in records:		
			if data[record][col_split] == 1: true_set.append(record)
			else: false_set.append(record)
		true_set_gini = calculateGini(true_set)
		false_set_gini = calculateGini(false_set)		
		total_gini = ( (len(true_set) / records_length * true_set_gini) + 
		( len(false_set) / records_length * false_set_gini) )
		return_set = (total_gini, true_set, false_set, col_split)

	#elif column_details[col_split][0] == "log_distance":
	else: # column_details[col_split][0] == "log_distance":
		best_gini = 0.6
		best_set= tuple()		
		for log_break in range(1, 10):
			del true_set[:]
			del false_set[:]
			for record in records:
				if data[record][col_split] >= log_break: true_set.append(record)
				else: false_set.append(record)
			true_set_gini = calculateGini(true_set)
			false_set_gini = calculateGini(false_set)
			total_gini = ( (len(true_set) / records_length * true_set_gini) + 
			( len(false_set) / records_length * false_set_gini) )
			if total_gini < best_gini:
				return_set = (total_gini, copy.deepcopy(true_set), copy.deepcopy(false_set), col_split, log_break)				
				best_gini = total_gini
		
	return return_set
	

def makeLeaf(node):
	node.is_leaf = True
	node.classification = classifyLeaf(node.records)

def classifyLeaf(records):
	num_true = 0
	for record in records:
		if data[record][-1] == 1: num_true += 1
	return num_true > len(records) / 2

	
def recursiveSplit(node):
	print "parent node: " + str(node.records)
	if len(node.records) <= 1 or len(node.col_nums) < 1:
		makeLeaf(node)
		return
	node.gini = calculateGini(node.records)	
	if node.gini == 0: 
		makeLeaf(node)
		return
	else:		
		best_gini_col_id = None
		return_values = tuple()
		best = tuple()	
		for col_id in node.col_nums:			
			return_values = returnSplitGini(node.records, col_id)
			if return_values[0] < node.gini:
				best = copy.deepcopy(return_values)
		if len(best) == 0:
			makeLeaf(node)
			return	
		print "printing best: " + str(best)
		node.split_col = best[3]
		if column_details[node.split_col][0] == "log_distance":
			print "yes a log"
			node.split_value = best[4]
		split_col_index = col_nums.index(node.split_col)
		colst =list()
		colst = node.col_nums[:split_col_index] + node.col_nums[split_col_index + 1:]
		colsf = copy.deepcopy(colst)
		node.tchild = d_node(best[1], colst)
		node.fchild = d_node(best[2], colsf)
		recursiveSplit(node.tchild)
		recursiveSplit(node.fchild)	

def classifyRecord(record, node):
	if node.is_leaf:
		print "at leaf this is classification: " + str(node.classification)
		record.append(node.classification)
		return

	elif column_details[node.split_col][0] == "binary":
		if record[node.split_col] == 1: classifyRecord(record, node.tchild)
		else: classifyRecord(record, node.fchild)
	else:
		if record[node.split_col] >= node.split_value: classifyRecord(record, node.tchild)
		else: classifyRecord(record, node.fchild)

def classifyRecords(records, my_tree):
	for record in records:		
		classifyRecord(record, my_tree.root)

# PrintTree methods
def printTree(my_tree):
	printTreeInOrder(my_tree.root, "  ")

def printTreeInOrder(node, spaces):
	if not node.tchild is None:
		printTreeInOrder(node.tchild, spaces + "         ")	
	if node.is_leaf: print spaces + str(node.classification)
	else: print spaces + str(node.split_col)
	if not node.fchild is  None:
		printTreeInOrder(node.fchild, spaces + "         ")

my_tree = d_tree(data_keys, col_nums)
recursiveSplit(my_tree.root)
printTree(my_tree)

test_record = [[0,0,1]]

classifyRecords(test_record, my_tree)
print "printing classification: " + str(test_record[-1])
