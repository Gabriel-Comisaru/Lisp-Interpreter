from .NFA import NFA
from dataclasses import dataclass
import re

EPSILON = ''


class Regex:
    def thompson(self) -> NFA[int]:
        raise NotImplementedError('the thompson method of the Regex class should never be called')

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

def build_tree(regex):
    # Preprocess the regular expression to handle whitespace and add grouping for "|"
    # need to change it because some of them are repeated and there are 70 lines of code just for it
    if (re.search(r'\[', regex)):
        regex = re.sub(r'\\\s', r'! !', regex)
        regex = re.sub(r'(\\)(\+)', r'&', regex)
    else:
        regex = re.sub(r'\\ ', r'!%!', regex)
        regex = re.sub(r'[^\S\n]', '', regex)
        regex = re.sub(r'!%!', r'! !', regex)

    regex = re.sub(r'(\w\*)([a-zA-Z0-9])', r'\1!\2', regex)
    regex = re.sub(r'([a-zA-Z0-9]*)\|', r'(\1)|', regex)
    regex = re.sub(r'(?<=[a-zA-Z0-9])(?=[a-zA-Z0-9])', r'!', regex)
    regex = re.sub(r'\(\)', r'', regex)
    
    
    regex = re.sub(r'\?([a-zA-Z0-9])', r'?!\1', regex)
    regex = re.sub(r'([a-zA-Z0-9])\(', r'\1!(', regex)
    regex = re.sub(r'\)([a-zA-Z0-9])', r')!\1', regex)
    regex = re.sub(r'([a-zA-Z0-9]*)(\*)(\w\*)', r'\1\2(\3)', regex)
    regex = re.sub(r'([a-zA-Z0-9])(\.)(\w\+)', r'\1\2(\3)', regex)
    regex = re.sub(r'\)\(', r')!(', regex)
    
    
    
    regex = re.sub(r'\*([a-zA-Z0-9])', r'*!\1', regex)
    regex = f'({regex})'
    
    regex = re.sub(r'\|([^(][a-zA-Z0-9+*.]*)\)', r'|(\1))', regex)

    
    regex = re.sub(r'\]([a-zA-Z0-9[])([^?^*^)^.])', r']!\1\2', regex)
    regex = re.sub(r'\]([?*])([^)])', r']\1!\2', regex)
    regex = re.sub(r'\\\(', r'!#!', regex)
    regex = re.sub(r'\\\)', r'!^!', regex)
    regex = re.sub(r'\_', r'!_!', regex)
    regex = re.sub(r'([@])', r'!\1!', regex)
    regex = re.sub(r'\(\.\)', r'.', regex)
    regex = re.sub(r'\(\.\.\)', r'..', regex)
    regex = re.sub(r'\-([^|^)])([^]])', r'-!\1\2', regex)
    regex = re.sub(r'\-\.', r'-!.', regex)
    regex = re.sub(r'\.([^|^)])', r'.!\1', regex)
    regex = re.sub(r'([a-zA-Z0-9])(\()', r'\1!\2', regex)

    
    regex = re.sub(r'!\)', r')', regex)
    regex = re.sub(r'\(!', r'(', regex)
    regex = re.sub(r'\+([a-zA-Z0-9])', r'+!\1', regex)

    regex = re.sub(r'([+*?])\.', r'\1!.', regex)
    
    regex = re.sub(r'([a-zA-Z0-9])([a-zA-Z0-9])', r'\1!\2', regex)

    letters_pattern = ''.join(chr(i) for i in range(ord('a'), ord('z') + 1))
    capital_letters_pattern = ''.join(chr(i) for i in range(ord('A'), ord('Z') + 1))
    numbers_pattern = ''.join(chr(i) for i in range(ord('0'), ord('9') + 1))
    regex =  re.sub(r'\[a-z\]', f'({letters_pattern})', regex)
    regex = re.sub(r'([a-z])([^!^)^+^*^?])', r'\1|\2', regex)
    regex = re.sub(r'([a-z])([^!^)^+^*^?^|])', r'\1|\2', regex)

    regex = re.sub(r'\[A-Z\]', f'({capital_letters_pattern})', regex)
    regex = re.sub(r'([A-Z])([^!^)^+^*^?])', r'\1|\2', regex)
    regex = re.sub(r'([A-Z])([^!^)^+^*^?^|])', r'\1|\2', regex)

    regex = re.sub(r'\[0-9\]', f'({numbers_pattern})', regex)
    regex = re.sub(r'([0-9])([^!^)^+^*^?])', r'\1|\2', regex)
    regex = re.sub(r'([0-9])([^!^)^+^*^?^|])', r'\1|\2', regex)

    regex = re.sub(r'\+\(', r'+!(', regex)
    regex = re.sub(r'\)\(', r')!(', regex)

    regex = re.sub(r'\\\/', r'`', regex)
    regex = re.sub(r'\\\*', r'~', regex)

    regex = re.sub(r'`~', r'`!~', regex)
    regex = re.sub(r'([^(^!])~([^)])', r'\1!~!\2', regex)
    regex = re.sub(r'~([^)^!])', r'~!\1', regex)
    regex = re.sub(r'(\|)(\!)', r'|', regex)
    regex = re.sub(r'(\!)(\!)', r'!', regex)

    regex = re.sub(r'(\*)(\()', r'\1!\2', regex)

    regex = re.sub(r'\\\+', r'+', regex)
    regex = re.sub(r'(\()~', r'#*', regex)

    # Define the operators and their priorities
    operators = {'*': 4, '+': 4, '?': 3, '!': 2, '|': 1}

    def parse_expression(start, end):
        if start == end:
            return None

        # Find the operator with the lowest priority
        min_priority = float('inf')
        min_operator_index = -1
        paren_count = 0

        for i in range(start, end):
            if regex[i] == '(':
                paren_count += 1
            elif regex[i] == ')':
                paren_count -= 1

            if paren_count == 0 and regex[i] in operators and operators[regex[i]] < min_priority:
                min_priority = operators[regex[i]]
                min_operator_index = i

        if min_operator_index != -1:
            # Found an operator
            node = TreeNode(regex[min_operator_index])
            node.left = parse_expression(start, min_operator_index)
            node.right = parse_expression(min_operator_index + 1, end)
        elif regex[start] == '(' and regex[end - 1] == ')':
            # Expression is wrapped in parentheses, remove them and parse
            node = parse_expression(start + 1, end - 1)
        else:
            # No operator found, it's a single character or character class
            node = TreeNode(regex[start:end])

        return node

    # Build the tree from the entire regular expression
    root = parse_expression(0, len(regex))
    return root

# Replace the special characters with their corresponding operators
def replace_chars(root):
    if root is not None:
        if root.value == '#':
            root.value = '('
        elif root.value == '^':
            root.value = ')'
        elif root.value == '`':
            root.value = '/'
        replace_chars(root.left)
        replace_chars(root.right)
    return root

def parse_regex(regex: str) -> Regex:
    # Build the tree from the regular expression
    root = build_tree(regex)
    # Replace the special characters with their corresponding operators
    root = replace_chars(root)
    
    # Parse the tree into a Regex object
    def parse_tree(root):
        if root.left is None and root.right is None:
            return Letter(root.value)
        elif root.value == '*':
            return Star(parse_tree(root.left))
        elif root.value == '+': # a+ = aa*
            return Plus(parse_tree(root.left))
        elif root.value == '?': # a? = a|empty
            return Union(parse_tree(root.left), Empty())
        elif root.value == '!':
            return Concat(parse_tree(root.left), parse_tree(root.right))
        elif root.value == '|':
            return Union(parse_tree(root.left), parse_tree(root.right))
        else:
            raise Exception(f'Unknown operator {root.value}')
    def print_tree(node, level=0, prefix="Root: "):
        if node is not None:
            print(" " * (level * 4) + prefix + str(node.value))
            if node.left is not None or node.right is not None:
                print_tree(node.left, level + 1, "L--- ")
                print_tree(node.right, level + 1, "R--- ")
    
    return parse_tree(root)


@dataclass
class Empty(Regex):
    def thompson(self) -> NFA[int]:
        return NFA(set(), {0}, 0, {}, {0})

@dataclass
class Letter(Regex):
    c: str

    def thompson(self) -> NFA[int]:
        if (self.c == '&'):
            self.c = '+'
        elif (self.c == '~'):
            self.c = '*'
        nfa = NFA({self.c}, {0, 1}, 0, {}, {1})
        nfa.d[(0, self.c)] = {1}
            
        return nfa
    

@dataclass
class Star(Regex):
    r: Regex

    def thompson(self) -> NFA[int]:
        nfa = self.r.thompson()
        new_nfa = NFA(nfa.S, nfa.K, nfa.q0, nfa.d, nfa.F)
        start = len(nfa.K)
        final = len(nfa.K) + 1
        new_nfa.K.add(start)
        new_nfa.K.add(final)
        new_nfa.q0 = start
        F = nfa.F.copy()
        new_nfa.F.clear()
        new_nfa.F.add(final)
        new_nfa.d[(start, EPSILON)] = {nfa.q0, final}
        for nfa_state in F:
            new_nfa.d[(nfa_state, EPSILON)] = {nfa.q0, final}
        return new_nfa
    
@dataclass
class Plus(Regex):
    r: Regex

    def thompson(self) -> NFA[int]:
        nfa1 = self.r.thompson()
        nfa2 = self.r.thompson()
        if (nfa1.q0 > nfa2.q0):
            nfa2 = nfa2.remap_states(lambda s: s + len(nfa1.K))
        elif (nfa1.q0 < nfa2.q0):
            nfa1 = nfa1.remap_states(lambda s: s + len(nfa2.K))
        else:
            nfa2 = nfa2.remap_states(lambda s: s + len(nfa1.K))
        nfa = NFA(nfa1.S.union(nfa2.S), nfa1.K.union(nfa2.K), nfa1.q0, nfa1.d, nfa2.F)
        nfa.d.update(nfa2.d)
        between = len(nfa.K)
        final = len(nfa.K) + 1
        nfa.K.add(between)
        nfa.K.add(final)
        nfa.q0 = nfa2.q0
        nfa.d[(between, EPSILON)] = {nfa1.q0, final}
        for nfa2_state in nfa2.F:
            nfa.d[(nfa2_state, EPSILON)] = {between}
        for nfa1_state in nfa1.F:
            nfa.d[(nfa1_state, EPSILON)] = {nfa1.q0, final}
        nfa.F.clear()
        nfa.F.add(final)
        return nfa
        

@dataclass
class Concat(Regex):
    r1: Regex
    r2: Regex

    def thompson(self) -> NFA[int]:
        nfa1 = self.r1.thompson()
        nfa2 = self.r2.thompson()
        # nfa2 = nfa2.remap_states(lambda s: s + len(nfa1.K))
        if (nfa1.q0 > nfa2.q0):
            nfa2 = nfa2.remap_states(lambda s: s + len(nfa1.K))
        elif (nfa1.q0 < nfa2.q0):
            nfa1 = nfa1.remap_states(lambda s: s + len(nfa2.K))
        else:
            nfa2 = nfa2.remap_states(lambda s: s + len(nfa1.K))
        nfa = NFA(nfa1.S.union(nfa2.S), nfa1.K.union(nfa2.K), nfa1.q0, nfa1.d, nfa2.F)
        nfa.d.update(nfa2.d)
        for nfa1_state in nfa1.F:
            nfa.d[(nfa1_state, EPSILON)] = {nfa2.q0}
        return nfa
    
@dataclass
class Union(Regex):
    r1: Regex
    r2: Regex

    def thompson(self) -> NFA[int]:
        nfa1 = self.r1.thompson()
        nfa2 = self.r2.thompson()
        if (nfa1.q0 > nfa2.q0):
            nfa2 = nfa2.remap_states(lambda s: s + len(nfa1.K))
        elif (nfa1.q0 < nfa2.q0):
            nfa1 = nfa1.remap_states(lambda s: s + len(nfa2.K))
        else:
            nfa2 = nfa2.remap_states(lambda s: s + len(nfa1.K))
        nfa = NFA(nfa1.S.union(nfa2.S), nfa1.K.union(nfa2.K), nfa1.q0, nfa1.d, nfa2.F)
        nfa.d.update(nfa2.d)
        start = len(nfa.K)
        final = len(nfa.K) + 1
        nfa.K.add(start)
        nfa.K.add(final)
        nfa.q0 = start
        nfa.d[(start, EPSILON)] = {nfa1.q0, nfa2.q0}
        for nfa1_state in nfa1.F:
            nfa.d[(nfa1_state, EPSILON)] = {final}
        for nfa2_state in nfa2.F:
            nfa.d[(nfa2_state, EPSILON)] = {final}       
        nfa.F.clear()
        nfa.F.add(final)
        return nfa
    


