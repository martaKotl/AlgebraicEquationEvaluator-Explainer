step_number = 1

# --- Tokenizer ---
def tokenize(expr):
    tokens = []
    i = 0

    while i < len(expr):
        ch = expr[i]

        if ch.isspace():
            i += 1
            continue

        if ch.isdigit():
            num = ch
            i += 1
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                num += expr[i]
                i += 1
            tokens.append(num)
            continue

        if ch == "√":
            tokens.append("√")
            i += 1
            continue

        if ch in "+-*/^()":
            tokens.append(ch)
            i += 1
            continue

        raise ValueError(f"Unknown character: {ch}")

    return tokens


# --- Step Functions ---
def addition_step(n1, n2):
    global step_number
    print(f"{step_number}. Add: {n1} and {n2}\n")
    step_number += 1

def subtraction_step(n1, n2):
    global step_number
    print(f"{step_number}. Subtract: {n1} and {n2}\n")
    step_number += 1

def multiplication_step(n1, n2):
    global step_number
    print(f"{step_number}. Multiply: {n1} and {n2}\n")
    step_number += 1

def division_step(n1, n2):
    global step_number
    print(f"{step_number}. Divide: {n1} and {n2}\n")
    step_number += 1

def power_step(n1, n2):
    global step_number
    print(f"{step_number}. Power: {n1} ^ {n2}")
    print("Definition: Multiply the base number (the one on the left)\n"
          "by itself x amount of times, where x is the exponent (the one on the right).\n")
    step_number += 1

def root_step(n):
    global step_number
    print(f"{step_number}. Square Root: √{n}")
    print(f"Definition: A square root of a number x is a number y such that y^2 = x\n")
    step_number += 1


# --- Operator Processing ---
def process_steps(equation, op, fn):
    while op in equation:

        idx = equation.index(op)

        if fn == root_step:
            num = equation[idx + 1]
            fn(num)
            equation[idx] = f"√({num})"
            equation.pop(idx + 1)

        else:
            n1 = equation[idx - 1]
            n2 = equation[idx + 1]
            fn(n1, n2)
            equation[idx - 1] = f"({n1} {op} {n2})"
            equation.pop(idx)     
            equation.pop(idx)     

    return equation


# --- Parenthesis Handling ---
def solve_parentheses(tokens):
    stack = []
    i = 0

    while i < len(tokens):
        if tokens[i] == "(":
            stack.append(i)

        elif tokens[i] == ")":
            start = stack.pop()
            end = i
            inside = tokens[start + 1:end]
            result_list = solve_expression(inside)
            grouped = result_list[0]
            tokens = tokens[:start] + [grouped] + tokens[end + 1:]
            return solve_parentheses(tokens)

        i += 1

    return tokens


# --- Complete Solve Function ---
def solve_expression(tokens):

    tokens = solve_parentheses(tokens)
    tokens = process_steps(tokens, "√", root_step)
    tokens = process_steps(tokens, "^", power_step)
    tokens = process_steps(tokens, "*", multiplication_step)
    tokens = process_steps(tokens, "/", division_step)
    tokens = process_steps(tokens, "+", addition_step)
    tokens = process_steps(tokens, "-", subtraction_step)

    return tokens


# --- Main Program ---

if __name__ == "__main__":
    print("Possible symbols:\n"
        "   Addition: + \n"
        "   Subtraction: -\n"
        "   Division: /\n"
        "   Multipication: *\n"
        "   Power: ^\n"
        "   Square Root: √\n"
        "---------------------\n")

    expr = input("Write an equation: ")

    tokens = tokenize(expr)

    print("\n--- Steps ---\n")
    result = solve_expression(tokens)

    print("--- All steps complete. ---")
    print(f"Final nested expression: {result[0]}\n")
