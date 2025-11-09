step_number = 1
# --- Functions ---
def addition_step(number1, number2):
    global step_number
    print(f"{step_number}. Add: {number1} and {number2}\n")
    step_number += 1

def subtraction_step(number1, number2):
    global step_number
    print(f"{step_number}. Subtract: {number1} and {number2}\n")
    step_number += 1

def multiplication_step(number1, number2):
    global step_number
    print(f"{step_number}. Multiply: {number1} and {number2}\n")
    step_number += 1

def division_step(number1, number2):
    global step_number
    print(f"{step_number}. Divide: {number1} and {number2}\n")
    step_number += 1

def power_step(number1, number2):
    global step_number
    print(f"{step_number}. Power: {number1} ^ {number2}")
    print("Definition: Multiply the base number (the one on the left)\n " \
    "by itself x amount of times, where x is the exponent (the one on the right).\n")  
    step_number += 1 

def root_step(number):
    global step_number
    print(f"{step_number}. Square Root: √{number}")
    print("Definition: A square root of a number x is a number y such that y^2 = x\n")
    step_number += 1

# --- Helper Function ---
def process_steps(equation_list, operator, function_to_call):
    while operator in equation_list:
        
        i = equation_list.index(operator)

        if function_to_call == root_step:
            num = equation_list[i+1]
            function_to_call(num)
            new_grouped_step = f"({operator}{num})"
            equation_list[i] = new_grouped_step
            equation_list.pop(i+1)

        else:
            num1 = equation_list[i-1]
            num2 = equation_list[i+1]
            function_to_call(num1, num2)
            new_grouped_step = f"({num1} {operator} {num2})"
            equation_list[i-1] = new_grouped_step
            equation_list.pop(i)
            equation_list.pop(i)

    return equation_list

# --- Main Program ---
print("Possible symbols:\n"\
    "   Addition: + \n" \
    "   Subtraction: -\n" \
    "   Division: /\n" \
    "   Multipication: *\n" \
    "   Power: ^\n" \
    "   Square Root: √\n" \
    "---------------------\n")
print("Write an equation (e.g., 5 + 6 * 3 - 5 * 2): ")
equation_str = input()
equation_parts = equation_str.split()

print("\n--- Here are the steps to solve an equation: ---\n")

equation_parts = process_steps(equation_parts, "√", root_step)

equation_parts = process_steps(equation_parts, "^", power_step)

equation_parts = process_steps(equation_parts, "*", multiplication_step)

equation_parts = process_steps(equation_parts, "/", division_step)

equation_parts = process_steps(equation_parts, "+", addition_step)

equation_parts = process_steps(equation_parts, "-", subtraction_step)


print("--- All steps complete. ---")
print(f"Final nested expression: {equation_parts[0]}\n")