# 1. Overview

Our program is a desktop application built with Python and Tkinter. It is an educational tool for learning mathematics. It breaks down calculations into clear, step-by-step operations. The program follows the standard order of operations and displays each step so learners can see exactly 
how an expression is simplified.

The system models the basic steps used when a computer processes a math expression:
- Breaking the expression into pieces (tokenization)
- Figuring out grouped parts like parentheses
- Working through each operation in the correct order
- Rewriting the expression step by step until it is fully simplified

## Key features:
- Step-by-step symbolic simplification
- Correct operator precedence handling
- Support for unary, binary, and functional operators
- Syntax validation with meaningful error messages
- GUI with light/dark mode and scrollable steps
- Optional mathematical definitions for each step

# 2. System Architecture

The program operates in several phases:

## 1. Tokenization

The *tokenize(expr)* function performs lexical analysis:
- Reads the input character-by-character
- Ignores whitespace
- Groups digits (and decimal points) into numeric tokens
- Recognizes alphabetic identifiers (functions such as sin, cos, log, int)
- Identifies operators: + - * / ^ ! √
- Recognizes grouping and delimiters: ( ) | ,
- Raises an error on unrecognized characters

Output: A list of tokens, e.g.:

    "3 + 4 * (2 - 1)" 
    → ["3", "+", "4", "*", "(", "2", "-", "1", ")"]

## 2. Syntax Analysis

Before solving, the system validates expressions using analyze_tokens(). It detects following errors:
- Empty expressions
- Empty parentheses ()
- Adjacent operators + *
- Mismatched parentheses
- Unbalanced |
- Invalid operator placement

Errors are displayed in a GUI error card.

## 3. Handling Parentheses

The *solve_parentheses(tokens)* performs a recursive search for the innermost parentheses pair.

For each pair:
- Extract tokens inside
- Solve the inner expression fully (recursive call)
- Replace the parentheses region with the computed sub-expression
- This models recursive descent parsing and mirrors how expression trees are built.

## 4. Operator Precedence

Operators are processed in the following order:
1. **Grouping Operators** - Parentheses ( ) and Absolute Value | |
2. **Functions** - sin(x), cos(x), log(x), int(lower, upper, expr)
3. **Factorial** - Postfix factorial !
4. **Unary Operators** - Unary minus -x and Square Root √x
5. **Exponentiation** (^)
6. **Multiplication and Division** (*, /)
7. **Addition and Subtraction** (+, -)

Each precedence level is evaluated by *process_steps(equation, op, fn)*. This function:
- Searches for the operator in the token list
- Calls a step-logging function (addition_step, etc.)
- Replaces the operator and its operands with a nested expression

Example:

    n1 = "3", op = "+", n2 = "4"
    → "(3 + 4)"

## 5. Step Logging

Each operation in the expression (such as addition, subtraction, multiplication, etc.) has its own function that prints a step with definition like:

    1. Add: 3 + 4
    
    Definition: Combining two or more quantities into a single sum.

    3. Square Root: √16

    Definition: A square root of a number x is a number y such that y² = x.

Instead of calculating the actual numeric answers, the program shows how the expression is built and simplified according to order of operations.

# 3. Updates since last documentation

## New mathematical capabilities

- Unary minus handling (-5, (-x + 2))
- Factorial operator (n!)
- Absolute value bars (|x|)
- sin(x)
- cos(x)
- log(x)
- Definite integrals

## Floating-Point Support

## Improved Parsing & Validation

Formal syntax analyzer to detect:
- Empty expressions
- Adjacent operators
- Invalid start/end tokens
- Mismatched parentheses
- Unbalanced absolute value bars
- Explicit unary vs binary minus resolution
- Recursive handling of nested expressions

## GUI Enhancements

- Multi-tab interface with Solver, Settings and About section
- Toggleable Dark Mode
- Toggleable step definitions
- Scrollable canvas for large expressions
- Styled result and error cards

## Built-In Documentation

- Lexical specification
- Grammar rules (BNF)
- Operator precedence table
- Usage examples
- Implementation overview

# 4. Conclusion

Math Step Solver is a educational tool, not a calculator.
It prioritizes clarity, structure, and correctness in how mathematical expressions are processed and simplified.

This makes it ideal for:
- Learning compiler concepts
- Understanding operator precedence
- Teaching step-based problem solving
