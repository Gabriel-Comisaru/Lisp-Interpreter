import re
from sys import argv
from src.Lexer import Lexer
# from src.Regex import TreeNode

class TreeNode:
	def __init__(self, value):
		self.value = value
		self.left = None
		self.right = None
	
	def _display_aux(self):
		"""Returns list of strings, width, height, and horizontal coordinate of the root."""
		# No child.
		if self.right is None and self.left is None:
			line = '%s' % self.value
			width = len(line)
			height = 1
			middle = width // 2
			return [line], width, height, middle

		# Only left child.
		if self.right is None:
			lines, n, p, x = self.left._display_aux()
			s = '%s' % self.value
			u = len(s)
			first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
			second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
			shifted_lines = [line + u * ' ' for line in lines]
			return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

		# Only right child.
		if self.left is None:
			lines, n, p, x = self.right._display_aux()
			s = '%s' % self.value
			u = len(s)
			first_line = s + x * '_' + (n - x) * ' '
			second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
			shifted_lines = [u * ' ' + line for line in lines]
			return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

		# Two children.
		left, n, p, x = self.left._display_aux()
		right, m, q, y = self.right._display_aux()
		s = '%s' % self.value
		u = len(s)
		first_line = (x + 1) * ' ' + (n - x - 1) * '' + s + y * '' + (m - y) * ' '
		second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
		if p < q:
			left += [n * ' '] * (q - p)
		elif q < p:
			right += [m * ' '] * (p - q)
		zipped_lines = zip(left, right)
		lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
		return lines, n + m + u, max(p, q) + 2, n + u // 2

	def display(self):
		lines, *_ = self._display_aux()
		for line in lines:
			print(line)

def find_nr_of_numbers(tokens): # find the number of numbers in the tokens
	return sum(1 for token_type, token_value in tokens if token_type == 'NUMBER')

def find_another_function(tokens, node): # find another function in the tokens
	global contains_lambda, not_lambda, start_lambda, end_lambda
	if node is None:
		return None
	
	value = node.value
	if len(value) > 2 and any(op in value for op in ('+', '.', '++', 'l')): 
		if value[0] != 'l':
			value = value[1:-1]
		value = value.replace('( +', '(+').replace('( ++', '(++)').replace('( lambda', '(lambda') # remove spaces before operators
		content = global_lexer.lex(value)
		contains_lambda = 0
		if lambda_index != 0 and any(op in not_lambda for op in [('SUM', '+'), ('CONCAT', '++')]):
			content = not_lambda[:lambda_index] + content + not_lambda[end_lambda:]	# add the rest of the tokens with the result of the lambda
			not_lambda = []
			start_lambda = end_lambda = 0

		node = parse_expression(content, first = 0)
	return node

def replace_lambda(node):
	if node is None:
		return None
	
	if node.value[0] == 'l':
		if (node.right.value[0] == 'l'):
			replace_lambda(node.right)

		replaced_char = node.value[1]
		replaced_value = node.left.value
		node.left = None
		
		# for every char in the node.right value, replace the char with the replaced_value
		body = node.right.value
		new_body = "".join(replaced_value if (char == replaced_char and (i - 2 < 0 or body[i - 2] != 'a')) else char for i, char in enumerate(body))
		node.right = None
		node.value = new_body

def replace_node(node, token_list):
    if node is None:
        if token_list:
            remaining_params.extend(token for token in token_list if token not in remaining_params) # if there are remaining parameters, add them to the list
        return None
    
    if node.value[0] == 'l' and node.left is None:
        if token_list:
            res = "".join(token_value if token_type not in ['OPEN_PAREN', 'CLOSE_PAREN'] else f" {token_value} " for token_type, token_value in token_list[0]) # build the parameter
            node.left = TreeNode(res) # add it to the left node
            token_list.pop(0)
    
    replace_node(node.right, token_list)

def parse_sum(tokens, node):
	nr_of_numbers = find_nr_of_numbers(tokens)
	
	if tokens[0][0] == 'VOID':
		return TreeNode('0')
	
	if nr_of_numbers == 1: # if there is only one number
		# search for the number
		for token_type, token_value in tokens:
			if token_type == 'NUMBER':
				return TreeNode(token_value)
	else:
		if tokens[0][0] != 'NUMBER': # we skip any whitespace, brackets before the number
			return parse_sum(tokens[1:], node)
		
		node = TreeNode('+')
		start_index = end_index = paren_count = found_nr = 0
		# find the start and end index of the first number found
		while end_index < len(tokens):
			paren_count += (tokens[end_index][0] == 'OPEN_PAREN') - (tokens[end_index][0] == 'CLOSE_PAREN')
			found_nr += (tokens[end_index][0] == 'NUMBER')
			end_index += 1
			if paren_count == 0 and found_nr >= 1:
				break

		node.left = parse_sum(tokens[start_index:end_index], node) # parse the first number
		node.right = parse_sum(tokens[end_index:], node) # parse the rest of the numbers
		return node

def parse_concat(tokens, node):
	if tokens[0][0] == 'NUMBER':
		if len(tokens) == 1 or tokens[1][0] == 'CLOSE_PAREN' or tokens[2][0] == 'CLOSE_PAREN': # 3) or 3 ) or 3
			return TreeNode(tokens[0][1])
		node = TreeNode("++")
		node.left = TreeNode(tokens[0][1]) # send the number to the left node
		node.right = parse_concat(tokens[1:], node) # parse the rest of the tokens
	elif tokens[0][0] == 'OPEN_PAREN': # we found a list of numbers
		start_index = end_index = paren_count = 0
		# find the start and end index of the list of numbers
		while end_index < len(tokens):
			paren_count += (tokens[end_index][0] == 'OPEN_PAREN') - (tokens[end_index][0] == 'CLOSE_PAREN')
			end_index += 1
			if paren_count == 0:
				break
			
		# build the group of numbers
		group = "".join(tokens[j][1] for j in range(start_index, end_index))

		# check if the group is the last one
		if tokens[end_index:] == [] or tokens[end_index:][0][0] == 'CLOSE_PAREN' or tokens[end_index:][1][0] == 'CLOSE_PAREN':
			return TreeNode(group)
		
		node = TreeNode("++")
		node.left = TreeNode(group) # send the group to the left node
		node.right = parse_concat(tokens[end_index:], node) # parse the rest of the tokens
	elif tokens[0][0] == 'VOID':
		node = TreeNode("++")
		node.left = TreeNode("()")
		node.right = parse_concat(tokens[1:], node)
	elif tokens[0][0] == 'WHITESPACE':
		return parse_concat(tokens[1:], node) # skip unnecessary whitespaces
	
	return node

params = []
root = None
contains_lambda = lambda_index = start_lambda = end_lambda = 0
not_lambda = []
global_lexer = None
remaining_params = []
def parse_expression(tokens, first = 0):
		finished = 0
		global params, root, contains_lambda, lambda_index, not_lambda, global_lexer, remaining_params, start_lambda, end_lambda
		if not tokens:
			return None

		brackets = found = found_body = param_start = 0
		body = ""

		# verify if tokens contain lambda
		if contains_lambda == 0:
			for i, (token_type, token_value) in enumerate(tokens):
				if token_type == 'LAMBDA':
					contains_lambda = 1
					lambda_index = i
					# find end of lambda
					end = i + 1
					nr_par = 1
					while nr_par > 0 and end < len(tokens):
						nr_par += (tokens[end][0] == 'OPEN_PAREN') - (tokens[end][0] == 'CLOSE_PAREN')
						end += 1
					not_lambda += tokens[end:]
					start_lambda, end_lambda = i, end
					break
				else:
					not_lambda.append(tokens[i])

		for i, (token_type, token_value) in enumerate(tokens):
			# if we found a sum, concat or lambda, parse it
			if token_type == 'SUM' and first == 0 and contains_lambda == 0:
				found = 1
				first = 1
				# find start index and end index for current sum
				start_sum = i
				end_sum = i + 2
				paren_count = 0
				# find the start and end index of the sum
				while end_sum < len(tokens):
					paren_count += (tokens[end_sum][0] == 'OPEN_PAREN') - (tokens[end_sum][0] == 'CLOSE_PAREN')
					end_sum += 1
					if paren_count == 0:
						break
				node = TreeNode('+')
				node = parse_sum(tokens[start_sum + 3:end_sum], node)
				break
			elif token_type == 'CONCAT' and first == 0:
				found = 1
				first = 2
				# find first group
				start_index = i + 2
				end_index = start_index
				paren_count = 0
				# find the start and end index of the concat
				while end_index < len(tokens) :
					paren_count += (tokens[end_index][0] == 'OPEN_PAREN') - (tokens[end_index][0] == 'CLOSE_PAREN')
					end_index += 1
					if paren_count == 0:
						break
				node = TreeNode('++')
				if root == None:
					root = node
				node = parse_concat(tokens[start_index + 1:end_index], node)
				finished = 1
				break
			elif token_type == 'LAMBDA':
				found = 1
				first = 3
				finished = 1
				lambda_char = tokens[i+2][1]
				node = TreeNode("l" + lambda_char)
				start_index = i + 3
				# save the head of the lambda
				if root == None:
					root = node
				node.right = parse_expression(tokens[start_index:], first)
				break
			elif (first == 3):
				found = 1
				# if we found the body of the lambda
				if found_body == 1:
					param_start = i # save the start index of the parameters
					break
				if token_type == 'OPEN_PAREN':
					body += " " + token_value if body else token_value			
					brackets += 1
					continue
				elif token_type in ['CHAR', 'NUMBER', 'SUM', 'CONCAT']:
					if not body:
						body = token_value
					else:
						body += " " + token_value
					if brackets == 0: # if we have even number of brackets, we found the body of the lambda
						node = TreeNode(body)
						body = ""
						found_body = 1
						continue
					continue
				elif token_type == 'CLOSE_PAREN':
					brackets -= 1
					found = 1
					if brackets == 0:
						node = TreeNode(body + " )")
						body = ""
						found_body = 1
					else:
						body += " " + token_value
					continue
				elif token_type == 'WHITESPACE':
					continue
				break
			elif token_type == 'OPEN_PAREN' and (tokens[i + 1][0] == 'SUM' or tokens[i + 1][0] == 'CONCAT'):
				continue
			elif (first == 0): # if there is no operation
				if token_type == 'NUMBER':
					found = 1
					if (len(tokens) == 1):
						node = TreeNode(token_value)
						break
					node = TreeNode(".")
					node.left = TreeNode(token_value)
					node.right = parse_expression(tokens[i+1:], first)
					break
				elif token_type == 'VOID':
					found = 1
					node = TreeNode(".")
					node.left = TreeNode("()")
					node.right = parse_expression(tokens[i+1:], first)
					break
				elif (token_type == 'OPEN_PAREN' and tokens[i + 1][0] not in ['SUM', 'CONCAT', 'LAMBDA', 'OPEN_PAREN']) or token_type == 'CLOSE_PAREN':
					if ('LAMBDA', 'lambda') not in tokens[i+1:]:
						found = 1
						node = TreeNode(".")
						node.left = TreeNode(token_value)
						node.right = parse_expression(tokens[i+1:], first)
						break
		if (found == 0):
			return None
		
		if (found_body == 1):
			# save in params the parameters of the lambda
			params = tokens[param_start:]
		if finished == 1 and node == root: # if we finished the tree and the current node is the root
			# make a list of the parameters
			param_list = []
			i = 0
			# find the parameters
			while i < len(params): # parse the parameters
				if params[i][0] == 'OPEN_PAREN':
					paren_count = 0
					start = i
					end = i							
					while end < len(params):
						paren_count += (params[end][0] == 'OPEN_PAREN') - (params[end][0] == 'CLOSE_PAREN')
						end += 1
						if paren_count == 0:
							break
					param_list.append(params[start:end])
					i = end
				elif params[i][0] == 'CLOSE_PAREN' or params[i][0] == 'WHITESPACE':
					i += 1
					continue
				elif params[i][0] == 'LAMBDA':
					j = i
					param_aux = []
					end = 0
					while j < len(params):
						if params[j][0] == 'CLOSE_PAREN':
							# finished parameter
							end = j
							break
						param_aux.append(params[j])
						j += 1
					if end == 0:
						end = j
					param_list.append(param_aux)
					i = end + 1
					continue
				else:
					param_list.append(params[i:i+1])
					i += 1
			param_list += remaining_params
			# for every node in the tree, if it is a lambda and left node is empty, replace it with the parameter
			replace_node(node, param_list)
			# if the node is a lambda, replace into right node the values of the left node
			replace_lambda(node)
			root = None
			# check if there are other functions
			return find_another_function(tokens, node)
		return node
def main():
	global global_lexer
	if len(argv) != 2:
		return
	
	filename = argv[1]
	# open file and read it
	with open(filename, 'r') as file:
		content = file.read()
		content = ' '.join(content.split())
		# if there is a space before an operator, remove it
		content = content.replace(' +', '+')
		content = content.replace(' ++', '++')

	spec = [
		('VOID', r'\(\)'),
		('OPEN_PAREN', r'\('),
		('CLOSE_PAREN', r'\)'),
		('NUMBER', r'[0-9]+'),
		('WHITESPACE', r'\ '),
		('CONCAT', r'&!&'),
		('SUM', r'&'),
		('LAMBDA', "lambda"),
		('POINTS', ":"),
		('CHAR', r'[a-z]+ | [A-Z]+'),
	]
	lexer = Lexer(spec)
	global_lexer = lexer
	content = content.replace('( +', '(+').replace('( ++', '(++').replace('( lambda', '(lambda')
	tokens = lexer.lex(content)
	tokens = list(filter(lambda a: a[0] != 'POINTS', tokens)) # remove the ':' token as it is not needed
	tokens = tokens[1:-1] # remove the first set of brackets
	expression_tree = parse_expression(tokens)
	
	# interpret the tree
	def interpret_tree(node, operand = None):
		if node is None:
			return 0 if operand == '+' else ""
		
		if node.value == '+':
			return int(interpret_tree(node.left, '+')) + int(interpret_tree(node.right, '+'))
		elif node.value in ['.', '++']:
			return f"{interpret_tree(node.left, node.value)} {interpret_tree(node.right, node.value)}"
		else:
			if operand == '+':
				return int(node.value)
			elif operand == '.':
				return str(node.value)
			elif operand == '++':
				if node.value[0] == '(':
					return " " + node.value[1:-1] + " "
				else:
					return node.value
	
	result = interpret_tree(expression_tree)
	# check if the result is a string
	if isinstance(result, str):
		# put paranthesis around the result
		result = f"( {result} )"
		# remove multiple spaces
		result = re.sub(r'\ +', ' ', result)
		# if the opening paranthesis are not equal to the closing ones, remove the unnecessary ones
		if (result.count('(') != result.count(')')):
			result = result[:-2]
	if result is None: # if we don't have the result, it is in the head of the tree
		result = expression_tree.value 
		result = re.sub(r'\ +', ' ', result) # remove multiple spaces
	print(result)


if __name__ == '__main__':
    main()
