####################################################################### 
# Simon Doty (dotysn)
# Predicitng Urbanization in the Austin Area Using Spatial Data Mining
# CS378 Data Mining; Professor Pradeep Ravikumar

# Python Implementation of a two class decision tree. 
# The tree is created through recursive indicution by choosing split
# node attributes and values using a greedy algorithm based on reducing
# gini. 
#
# The induction for a specific branch stops when the number of records
# in a branch subset is less than a certain threshold, or when the gini
# is zero, or when no gini gain can be made.
#
# Classification is a simple descension down the tree until a leaf node
# is reached at which point the record will be classified.


import copy, random

TOTAL_RECORDS = 33390
#######################################################################
# Classes used in inducting the tree are a Node class and a simple Tree

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

column_details = [["log_distance"], ["log_distance"], ["log_distance"],
["log_distance"], ["log_distance"], ["log_distance"], ["log_distance"], 
["log_distance"], ["log_distance"], ["log_distance"], ["log_distance"]]


def buildTree(input_file=None, use_all=False, total_set=None, random_train=None, preprune=10):

	#if input_file is None or total_size is None or train_size is None:
	if input_file is None or total_set is None or random_train is None:
		print "Incorrect arguments to build function. Exiting program."
		exit(0)

	# use three dictionaries to store ID numbers with a list of attributes
	train_data=dict()
	test_data=dict()
	total=dict()

	# read in the da row by row and separate into training or test da
	inputfile = input_file
	f = open(inputfile)
	for line in iter(f):
		line = line.replace('\n', "")
		line_array = line.split(',')
		line_array = map(int, line_array)
		fid = int(line_array[0])
		if fid not in total_set and total_set != []:
			continue
		elif fid in random_train:
			test_data[fid] = line_array[1:12] # for testing - no class label
		else:
			train_data[fid] = line_array[1:]  # save training data with class 
		total[fid] = line_array[1:]        # save all to check accuracy later
	f.close()

	if use_all == True:
		return (None, test_data, total)
	# make a list of training records and a list of column numbers
	train_data_keys = list(train_data.keys())
	col_nums = list() 
	for i in range(0, len(train_data[train_data_keys[0]]) - 1):
		col_nums.append(i)


	# calculateGini accepts a set of records and returns the gini score
	# by using the equation: 1 - (x/total)^2 - (y/total)^2
	def calculateGini(records):		
		total = float(len(records))
		if total == 0: return 0
		num_class_1 = 0
		for record in records:
			if train_data[record][-1] == 1: num_class_1 = num_class_1 + 1
		num_class_0 = total - num_class_1
		gini = 1 - (num_class_1 / total)**2 - (num_class_0 / total)**2
		return gini

	# returns a tuple of gini, a true subset, a false subset, a split column
	# and a split value is applicable. Used to 
	def returnSplitGini(records, col_split):
		true_set= list()
		false_set= list()
		return_set= tuple()
		records_length = float(len(records))

		if column_details[col_split][0] == "binary":
			for record in records:		
				if train_data[record][col_split] == 1: true_set.append(record)
				else: false_set.append(record)
			true_set_gini = calculateGini(true_set)
			false_set_gini = calculateGini(false_set)		
			total_gini = ( (len(true_set) / records_length * true_set_gini) + 
			( len(false_set) / records_length * false_set_gini) )
			return_set = (total_gini, true_set, false_set, col_split)
		else: 
			best_gini = 0.6
			best_set= tuple()		
			for log_break in range(0, 10):
				del true_set[:]
				del false_set[:]
				for record in records:
					if train_data[record][col_split] >= log_break: true_set.append(record)
					else: false_set.append(record)
				true_set_gini = calculateGini(true_set)
				false_set_gini = calculateGini(false_set)
				total_gini = ( (len(true_set) / records_length * true_set_gini) + 
				( len(false_set) / records_length * false_set_gini) )
				if total_gini < best_gini:
					return_set = (total_gini, copy.deepcopy(true_set), 
						copy.deepcopy(false_set), col_split, log_break)				
					best_gini = total_gini
			
		return return_set

	# Passed a node, the classification is calculated as the is_leaf flag set
	def makeLeaf(node):
		node.is_leaf = True
		node.classification = classifyLeaf(node.records)

	# Given a set of records, finds the majority and returns T/F
	def classifyLeaf(records):
		num_true = 0
		for record in records:
			if train_data[record][-1] == 1: num_true += 1
		return num_true > len(records) / 2

	# Most induction work done here. given node, choses  how to split
	# and constructs child nodes, or makes node a leaf
	def recursiveSplit(node):
		if len(node.records) <= preprune or len(node.col_nums) < 1:
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
			node.split_col = best[3]
			if column_details[node.split_col][0] == "log_distance":
				node.split_value = best[4]
			split_col_index = col_nums.index(node.split_col)
			colst =list()
			colst = node.col_nums[:split_col_index] + node.col_nums[split_col_index + 1:]
			colsf = copy.deepcopy(colst)
			node.tchild = d_node(best[1], colst)
			node.fchild = d_node(best[2], colsf)
			recursiveSplit(node.tchild)
			recursiveSplit(node.fchild)	

	my_tree = d_tree(train_data_keys, col_nums) # create the tree
	recursiveSplit(my_tree.root) # kickoff induction with root
	return (my_tree, test_data, total)


# induction done
###############################################################################
# The code below is used to classify a set of records once the tree is induced.

# Classifies a specific record given a record of attributes and the tree root
def classifyRecord(record, node):
	if node.is_leaf:
		record.append(node.classification)
	elif column_details[node.split_col][0] == "binary":
		if record[node.split_col] == 1: classifyRecord(record, node.tchild)
		else: classifyRecord(record, node.fchild)
	else:
		if record[node.split_col] >= node.split_value:
			classifyRecord(record, node.tchild)
		else: classifyRecord(record, node.fchild)

# Classification kickoff that classifies a set of records
def classifyRecords(test_records, my_tree):
	for record in test_records:		
		classifyRecord(test_data[record], my_tree.root)

# classification done
###############################################################################
# PrintTree methods to output a crude visual representation of the induced tree

def printTree(my_tree):
	printTreeInOrder(my_tree.root, "  ")

def printTreeInOrder(node, spaces):
	if not node.tchild is None:
		printTreeInOrder(node.tchild, spaces + "      ")	
	if node.is_leaf: print spaces + str(node.classification)
	else: print spaces + str(node.split_col) + str(node.split_value)
	if not node.fchild is  None:
		printTreeInOrder(node.fchild, spaces + "      ")

# printing done
############################################################################
# The code below is run to build the decision tree with the training train_data. 
# The tree constructor takes a list of records (training records, and list 
# of col numbers of attributes.                            

###############################################################################
# Create a training set of roughly 2/3 total data
# Split training set into 10 cross validation sets to estimate accuracy and prune


preprune = 40

all_data = [x for x in range(1, 33392)]
training_set_size = 2 * 33391 / 3
training_data = random.sample((all_data), training_set_size)
testing_data = [x for x in range(1, 33392) if x not in training_data ]
random.shuffle(training_data) 
chunk_size = training_set_size / 10
total_correct = 0
total_classified = 0

# run cross validation sets
print ("\nBuilding tree, classifying test records, and" + 
	"calculating accuracy for cross validation sets 1 - 10...")
for i in range(0, 10):
	print ("\nCross validation set " + str(i+1) + 
		" (records [" + str(i * chunk_size) + ":" + str(i * chunk_size + chunk_size) + "] of training set):")
	cross_test_data = training_data[i * chunk_size : i * chunk_size + chunk_size]
	results = buildTree('dataset/entire_dataset.csv', False, training_data, cross_test_data, preprune)
	tree = results[0]
	test_data = results[1]
	total = results[2]
	#printTree(tree)
	classifyRecords(test_data, tree)
	correct = 0
	total_test_data = 0
	for record in test_data:
		total_test_data += 1
		if ( (total[record][-1] == 1 and test_data[record][-1] == True) or 
			(total[record][-1] == 0 and test_data[record][-1] == False) ): 
			correct += 1

	accuracy = correct * 1.0 / total_test_data

	print ( str(correct) + " records classified correctly out of a total of " + 
		str(total_test_data) + ".\nAccuracy of cross validation set " + str(i + 1) + " = " + str(accuracy) )
	total_classified += total_test_data
	total_correct += correct
print "----------------------------------------------------------------------------------"
# print estimated accuracy of the whole training set with test data
accuracy = total_correct * 1.0 / total_classified
print ( "\nAcross all ten (10) cross validation sets:\n" + str(total_correct) +
	" classified correctly out of a total of " + 
	str(total_classified) + ".\nEstimated accuracy of classifier = " + str(accuracy) + "\n")

###############################################################################
# Calculate final results using the whole dataset, training and testing.
# Print results when done. 

final_results = buildTree('dataset/entire_dataset.csv', False, all_data, testing_data, preprune)
tree = final_results[0]
test_data = final_results[1]
total = final_results[2]
classifyRecords(test_data, tree)

false_positives=list()
false_negatives=list()
true_positives=list()
true_negatives=list()

correct = 0
total_test_data = 0
for record in test_data:
	total_test_data += 1
	if (total[record][-1] == 1 and test_data[record][-1] == True):
		true_positives.append(record)
		correct += 1
	elif (total[record][-1] == 0 and test_data[record][-1] == False): 
		true_negatives.append(record)
		correct += 1
	elif (total[record][-1] == 0 and test_data[record][-1] == True):
		false_positives.append(record)
	else:
		false_negatives.append(record)
total_true = true_positives + true_negatives
total_false = false_positives + false_negatives

accuracy = correct * 1.0 / total_test_data
print "----------------------------------------------------------------------------------"

print ( "\nFinal results using entire training set to train and entire testing set to test: " +
	"\n" + str(correct) + " correct out of a total of " + 
	str(total_test_data) + ".\nFinal accuracy of model = " + str(accuracy) )

print ( "\nSize of true positives, true_negatives, false_positives, and false_negatives: " +
	str(len(true_positives)) + ", " + str(len(true_negatives)) + ", " + str(len(false_positives)) + ", " + str(len(false_negatives)) )
