# Simplified Lisp Interpreter
The entry point of the interpreter is the file `src/main.py`, which takes the file to be interpreted as an argument and prints the interpretation result to `stdout`.

To run a file from a package, you can use the command:
```
python3.12 -m src.main {arguments}
```

# Functionality
**Language L**

We will interpret a functional language inspired by `Lisp ("List Processing")`, but much simplified.

A program is a list of atoms, where an atom can be:
- a natural number
- an empty list ()
- a lambda expression
- a function invocation
- another list of atoms

The output is a number or a list consisting only of:
- numbers
- other lists (composed only of numbers or other lists)

### Natural numbers
In L, we will only use natural numbers, without a specific upper limit. A number is any sequence of digits (from 0 to 9).

### Empty List
An empty list is a list without elements, represented by the string ().

### Lambda Expressions
A lambda expression represents the definition of a 'custom' function. The syntax for defining a lambda expression is as follows:
```
lambda {id}: {expr}
```
Example:
```
(lambda x: (x x) (1 2))
```

is evaluated to:
```
((1 2) (1 2))
```

### Function Invocations

A list of the form (f x) can be evaluated as long as f is:
- a lambda expression
- a function from the standard library

For simplicity, we will limit ourselves to 2 standard functions:
- `+`, which when applied to a list, recursively sums the elements of the list and returns an atom (it cannot be applied to lists containing other functions/expressions)
- `++`, which when applied to a list, concatenates all component lists (if there are atoms in the list, they are added to the resulting list)
