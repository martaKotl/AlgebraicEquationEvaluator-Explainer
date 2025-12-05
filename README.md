# 1. Overview

This program is an educational tool for learning mathematics. It breaks down calculations into clear, step-by-step operations. The program follows the standard order of operations and displays each step so learners can see exactly 
how an expression is simplified.

The system models the basic steps used when a computer processes a math expression:
- Breaking the expression into pieces (tokenization)
- Figuring out grouped parts like parentheses
- Working through each operation in the correct order
- Rewriting the expression step by step until it is fully simplified

# 2. System Architecture

The program operates in several phases:

## 1. Tokenization

The *tokenize(expr)* function performs lexical analysis:
- Reads the input character-by-character
- Groups digits into multi-digit numbers
- Identifies operators: + - * / ^ √
- Recognizes parentheses: ( )

Output: A list of tokens, e.g.:

    "3 + 4 * (2 - 1)" 
    → ["3", "+", "4", "*", "(", "2", "-", "1", ")"]

## 2. Handling Parentheses

The *solve_parentheses(tokens)* performs a recursive search for the innermost parentheses pair.

For each pair:
- Extract tokens inside
- Solve the inner expression fully (recursive call)
- Replace the parentheses region with the computed sub-expression
- This models recursive descent parsing and mirrors how expression trees are built.

## 3. Operator Precedence

Operators are processed in the following order:
1. Square Root (√)
2. Exponentiation (^)
3. Multiplication and Division (*, /)
4. Addition and Subtraction (+, -)

Each precedence level is evaluated by *process_steps(equation, op, fn)*. This function:
- Searches for the operator in the token list
- Calls a step-logging function (addition_step, etc.)
- Replaces the operator and its operands with a nested expression

Example:

    n1 = "3", op = "+", n2 = "4"
    → "(3 + 4)"

## 4. Step Logging

Each operation in the expression (such as addition, subtraction, multiplication, etc.) has its own function that prints a step like:

    1. Add: n1 and n2
    2. Multiply: n1 and n2

or for more complex operations, it prints a step with explanation, like:
    
    1. Square Root: √n
    Definition: A square root of a number x is a number y such that y^2 = x\n

Instead of calculating the actual numeric answers, the program shows how the expression is built and simplified according to order of operations.

# 3. Program Behavior

When the program starts, it first displays a list of all the supported mathematical operations. Then, it asks the user to enter an expression.

    Possible symbols:
       Addition: + 
       Subtraction: -
       Division: /
       Multipication: *
       Power: ^
       Square Root: √
    ---------------------
    
    Write an equation:

When the user enters an expression, they are presented with steps and final nested expression:

    Write an equation: 3 * 4 - (2 ^ 5 - 7)
    
    --- Steps ---
    
    1. Power: 2 ^ 5
    Definition: Multiply the base number (the one on the left)
    by itself x amount of times, where x is the exponent (the one on the right).
    
    2. Subtract: (2 ^ 5) and 7
    
    3. Multiply: 3 and 4
    
    4. Subtract: (3 * 4) and ((2 ^ 5) - 7)
    
    --- All steps complete. ---
    Final nested expression: ((3 * 4) - ((2 ^ 5) - 7))

# 4. Possible Extensions

**- Support More Unary Functions**

Such as:
- sin(x)
- cos(x)
- log(x)
- factorial (n!)

**- Add Floating-Point Support**

**- Add Evaluation Phase**

Actually compute numeric results after building the AST.

**- Add Error Handling**

Detect:
- Mismatched parentheses
- Invalid operator combinations
- Unexpected input sequences

# 7. Conclusion
