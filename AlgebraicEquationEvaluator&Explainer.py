import tkinter as tk
from tkinter import scrolledtext
import tkinter.ttk as ttk

output_callback = print  
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
        
        if ch.isalpha():   
            word = ""
            while i < len(expr) and expr[i].isalpha():
                word += expr[i]
                i += 1
            tokens.append(word)
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

        if ch in "+-*/^()!|,":
            tokens.append(ch)
            i += 1
            continue

        raise ValueError(f"Unknown character: {ch}")
    return tokens

# --- Syntax Analyzer ---

def analyze_tokens(tokens):
    """Inspects tokens for mathematical syntax errors before solving."""
    if not tokens:
        raise ValueError("The expression is empty.")

    stack = []
    pipe_count = 0
    binary_ops = {"+", "*", "/", "^", ","} 
    all_ops = {"+", "-", "*", "/", "^", "!", "√", ","}

    for i, token in enumerate(tokens):
        if token == "(" and i + 1 < len(tokens) and tokens[i+1] == ")":
            raise ValueError("Empty parentheses '()' detected.")

        if i == 0 and token in binary_ops:
            raise ValueError(f"Expression cannot start with '{token}'.")
        if i == len(tokens) - 1 and token in all_ops and token != "!":
            raise ValueError(f"Expression cannot end with '{token}'.")

        if token in binary_ops and i + 1 < len(tokens):
            if tokens[i+1] in binary_ops:
                raise ValueError(f"Adjacent operators detected: '{token} {tokens[i+1]}'.")

        if token == "(":
            stack.append("(")
        elif token == ")":
            if not stack:
                raise ValueError("Mismatched parentheses: closed ')' without opening.")
            stack.pop()
        
        if token == "|":
            pipe_count += 1

    if stack:
        raise ValueError("Mismatched parentheses: unclosed '('.")
    if pipe_count % 2 != 0:
        raise ValueError("Mismatched absolute value bars '|'.")
    
    return True

# --- Step Functions ---
def addition_step(n1, n2):
    global step_number
    output_callback(f"{step_number}. Add: {n1} + {n2}\n\nDefinition: Combining two or more quantities into a single sum.")
    step_number += 1

def subtraction_step(n1, n2):
    global step_number
    output_callback(f"{step_number}. Subtract: {n1} - {n2}\n\nDefinition: Taking one quantity away from another to find the difference.")
    step_number += 1

def multiplication_step(n1, n2):
    global step_number
    output_callback(f"{step_number}. Multiply: {n1} * {n2}\n\nDefinition: Repeated addition of a number a certain number of times.")
    step_number += 1

def division_step(n1, n2):
    global step_number
    output_callback(f"{step_number}. Divide: {n1} / {n2}\n\nDefinition: Splitting a large group into equal smaller groups.")
    step_number += 1

def power_step(n1, n2):
    global step_number
    output_callback(f"{step_number}. Power: {n1} ^ {n2}\n\nDefinition: Multiply the base number by itself x times.")
    step_number += 1

def root_step(n):
    global step_number
    output_callback(f"{step_number}. Square Root: √{n}\n\nDefinition: A square root of a number x is a number y such that y^2 = x.")
    step_number += 1

def absolute_step(n):
    global step_number
    output_callback(f"{step_number}. Absolute Value: |{n}|\n\nDefinition: Absolute value is the distance from zero.")
    step_number += 1

def factorial_step(n):
    global step_number
    output_callback(f"{step_number}. Factorial: {n}!\n\nDefinition: Multiply all positive integers from 1 up to the number.")
    step_number += 1

def negation_step(n):
    global step_number
    output_callback(f"{step_number}. Negation: -{n}\n\nDefinition: Finding the opposite of a number on the number line.")
    step_number += 1

def sine_step(n):
    global step_number
    output_callback(f"{step_number}. Sine: sin({n})\n\nDefinition: In a right triangle, the ratio of the length of the side opposite the angle to the hypotenuse.")
    step_number += 1

def cosine_step(n):
    global step_number
    output_callback(f"{step_number}. Cosine: cos({n})\n\nDefinition: In a right triangle, the ratio of the length of the adjacent side to the hypotenuse.")
    step_number += 1

def log_step(n):
    global step_number
    output_callback(f"{step_number}. Logarithm: log({n})\n\nDefinition: The power to which a base must be raised to produce that number.")
    step_number += 1

def integral_step(lower, upper, function):
    global step_number
    output_callback(f"{step_number}. Definite Integral: ∫ from {lower} to {upper} of ({function})\n\nDefinition: Represents the signed area under the curve between two points.")
    step_number += 1

# --- Operator Processing ---
def process_steps(equation, op, fn):
    while op in equation:
        idx = equation.index(op)
        if op in ["√", "sin", "cos", "log"]:
            num = equation[idx + 1]
            fn(num)
            equation[idx] = f"{op}({num})"
            equation.pop(idx + 1)
        else:
            n1 = equation[idx - 1]
            n2 = equation[idx + 1]
            fn(n1, n2)
            equation[idx - 1] = f"({n1} {op} {n2})"
            equation.pop(idx)
            equation.pop(idx)


    return equation

# --- Unary Minus Processing ---
def process_unary_minus(tokens):
    i = 0
    while i < len(tokens):
        if tokens[i] == "-":
            if i == 0 or tokens[i - 1] in "+-*/^(|":
                tokens[i] = "u-"
        i += 1
    return tokens

def process_negation(tokens):
    while "u-" in tokens:
        idx = tokens.index("u-")
        num = tokens[idx + 1]
        negation_step(num)
        tokens[idx] = f"(-{num})"
        tokens.pop(idx + 1)
    return tokens

# --- Absolute Value ---
def process_absolute(tokens):
    stack = []
    i = 0
    while i < len(tokens):
        if tokens[i] == "|":
            if stack:
                start = stack.pop()
                inside = tokens[start + 1:i]
                result_list = solve_expression(inside)
                grouped = result_list[0]
                absolute_step(grouped)
                tokens = tokens[:start] + [f"|{grouped}|"] + tokens[i + 1:]
                return process_absolute(tokens)
            else:
                stack.append(i)
        i += 1
    return tokens

# --- Factorial ---
def process_factorial(equation):
    while "!" in equation:
        idx = equation.index("!")
        num = equation[idx - 1]
        factorial_step(num)
        equation[idx - 1] = f"({num}!)"
        equation.pop(idx)

    return equation

# --- Integral Logic ---
def process_integral(tokens):
    while "int" in tokens:
        idx = tokens.index("int")
        start_paren = idx + 1
        
        depth = 0
        end_paren = -1
        for i in range(start_paren, len(tokens)):
            if tokens[i] == "(": depth += 1
            elif tokens[i] == ")":
                depth -= 1
                if depth == 0:
                    end_paren = i
                    break
        
        if end_paren != -1:
            content = tokens[start_paren + 1 : end_paren]
            
            parts_tokens = []
            current_part = []
            c_depth = 0
            for t in content:
                if t == "(": c_depth += 1
                elif t == ")": c_depth -= 1
                
                if t == "," and c_depth == 0:
                    parts_tokens.append(current_part)
                    current_part = []
                else:
                    current_part.append(t)
            parts_tokens.append(current_part)

            if len(parts_tokens) == 3:
                lower = solve_expression(parts_tokens[0])[0]
                upper = solve_expression(parts_tokens[1])[0]
                func = solve_expression(parts_tokens[2])[0]
                
                integral_step(lower, upper, func)
                tokens[idx : end_paren + 1] = [f"∫({lower} to {upper})[{func}]"]
            else:
                tokens.pop(idx)
        else:
            break
    return tokens

# --- Parenthesis Handling ---
def solve_parentheses(tokens):
    stack = []
    i = 0
    while i < len(tokens):
        if tokens[i] == "(":
            stack.append(i)
        elif tokens[i] == ")":
            start = stack.pop()
            inside = tokens[start + 1:i]
            result_list = solve_expression(inside)
            grouped = result_list[0]
            tokens = tokens[:start] + [grouped] + tokens[i + 1:]
            return solve_parentheses(tokens)
        i += 1
    return tokens

# --- Solve Function ---
def solve_expression(tokens):
    tokens = process_unary_minus(tokens)
    tokens = process_integral(tokens)
    tokens = solve_parentheses(tokens)
    tokens = process_absolute(tokens)
    tokens = process_factorial(tokens)
    tokens = process_negation(tokens)

    tokens = process_steps(tokens, "sin", sine_step)
    tokens = process_steps(tokens, "cos", cosine_step)
    tokens = process_steps(tokens, "log", log_step)
    tokens = process_steps(tokens, "√", root_step)
    tokens = process_steps(tokens, "^", power_step)
    tokens = process_steps(tokens, "*", multiplication_step)
    tokens = process_steps(tokens, "/", division_step)
    tokens = process_steps(tokens, "+", addition_step)
    tokens = process_steps(tokens, "-", subtraction_step)

    return tokens

# --- GUI  ---

BG_MAIN = "#F8F9FA"       
BG_CARD = "#FFFFFF"       
ACCENT = "#4F46E5"        
ACCENT_HOVER = "#4338CA"  
TEXT_MAIN = "#1F2937"     
TEXT_DIM = "#6B7280"      
BORDER = "#E5E7EB"        

def make_canvas_scrollable(canvas, frame):
    """Adds mousewheel support only if the content exceeds the window height."""
    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    def _on_mousewheel(event):
        if canvas.yview() != (0.0, 1.0):
            if event.delta:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            else:
                if event.num == 4: canvas.yview_scroll(-1, "units")
                elif event.num == 5: canvas.yview_scroll(1, "units")

    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<Button-4>", _on_mousewheel), add="+")
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<Button-5>", _on_mousewheel), add="+")
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<Button-4>"), add="+")
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<Button-5>"), add="+")
def run_gui():
    global output_callback, step_number

    root = tk.Tk()
    root.title("Math Step Solver")
    root.geometry("1000x800")
    root.minsize(500, 600)

    show_definitions = tk.BooleanVar(value=True)
    dark_mode = tk.BooleanVar(value=False)

    themes = {
        "light": {
            "bg": "#F8F9FA", "card": "#FFFFFF", "text": "#1F2937", 
            "dim": "#6B7280", "border": "#E5E7EB", "accent": "#4F46E5",
            "result_bg": "#EEF2FF","error": "#DC2626"
        },
        "dark": {
            "bg": "#0F172A", "card": "#1E293B", "text": "#F1F5F9", 
            "dim": "#94A3B8", "border": "#334155", "accent": "#818CF8",
            "result_bg": "#2D3748","error": "#F87171"
        }
    }

    current_colors = themes["light"]
    style = ttk.Style()
    style.theme_use('clam')

    def update_notebook_styles(colors):
        style.configure("TNotebook", background=colors["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", padding=[20, 10], font=("Segoe UI", 10, "bold"), 
                        background=colors["card"], foreground=colors["dim"])
        style.map("TNotebook.Tab",
                  background=[("selected", colors["accent"]), ("!selected", colors["card"])],
                  foreground=[("selected", "white"), ("!selected", colors["dim"])])

    update_notebook_styles(current_colors)
    root.configure(bg=current_colors["bg"])

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    # =========================
    # TAB 1: SOLVER
    # =========================
    solver_tab = tk.Frame(notebook, bg=current_colors["bg"])
    notebook.add(solver_tab, text="  SOLVER  ")

    input_frame = tk.Frame(solver_tab, bg=current_colors["bg"])
    input_frame.pack(fill=tk.X, pady=(20, 10), padx=20)

    lbl_input = tk.Label(input_frame, text="ENTER EQUATION", font=("Segoe UI", 20, "bold"), 
                         fg=current_colors["accent"], bg=current_colors["bg"])
    lbl_input.pack(anchor="w", padx=20)
    
    entry = tk.Entry(input_frame, font=("Consolas", 14), bd=0, highlightthickness=1, 
                    highlightbackground=current_colors["border"], highlightcolor=current_colors["accent"], 
                    bg=current_colors["card"], fg=current_colors["text"])
    entry.pack(fill=tk.X, pady=10, ipady=10, padx=20)
    entry.insert(0, "((3 + 2!) * √16) - (|(-4 + 1)| + sin(30) + int(0, 3, (x + 1)^2))")

    steps_canvas = tk.Canvas(solver_tab, bg=current_colors["bg"], highlightthickness=0)
    steps_scrollbar = ttk.Scrollbar(solver_tab, orient="vertical", command=steps_canvas.yview)
    steps_frame = tk.Frame(steps_canvas, bg=current_colors["bg"])

    steps_window = steps_canvas.create_window((0, 0), window=steps_frame, anchor="nw")
    steps_canvas.bind('<Configure>', lambda e: steps_canvas.itemconfig(steps_window, width=e.width))
    steps_canvas.configure(yscrollcommand=steps_scrollbar.set)
    steps_scrollbar.pack(side="right", fill="y")
    steps_canvas.pack(side="left", fill="both", expand=True, padx=20)

    make_canvas_scrollable(steps_canvas, steps_frame)
    card_data = []

    def solve():
        global step_number
        step_number = 1
        card_data.clear() 
        for widget in steps_frame.winfo_children(): widget.destroy()
        
        expr = entry.get()
        if not expr.strip(): return
        
        colors = themes["dark" if dark_mode.get() else "light"]

        try:
            tokens = tokenize(expr)
            analyze_tokens(tokens)
            result = solve_expression(tokens)
            
            res_header = tk.Label(steps_frame, text="FINAL RESULT", font=("Segoe UI", 20, "bold"), 
                                bg=colors["bg"], fg=colors["accent"], name="result_header")
            res_header.pack(anchor="w", padx=20, pady=(30, 5))
            
            f_card = tk.Frame(steps_frame, bg=colors["result_bg"], padx=20, pady=20, 
                            highlightthickness=1, highlightbackground=colors["accent"], name="result_card")
            f_card.pack(fill=tk.X, pady=(0, 60)) 
            
            res_label = tk.Label(f_card, text=result[0], font=("Consolas", 18, "bold"), 
                                bg=colors["result_bg"], fg=colors["text"], justify="left", anchor="w")
            res_label.pack(anchor="w", fill=tk.X)
            
        except Exception as e:
            for widget in steps_frame.winfo_children(): widget.destroy()
            
            err_card = tk.Frame(steps_frame, bg=colors["card"], padx=20, pady=20, 
                               highlightthickness=2, highlightbackground=colors["error"], name="error_card")
            err_card.pack(fill=tk.X, pady=40, padx=20)
            
            tk.Label(err_card, text="SYNTAX ERROR", font=("Segoe UI", 14, "bold"), 
                    fg=colors["error"], bg=colors["card"]).pack(anchor="w")
            
            tk.Label(err_card, text=str(e), font=("Consolas", 12), 
                    fg=colors["text"], bg=colors["card"], wraplength=600, justify="left").pack(anchor="w", pady=(10, 0))
        steps_frame.update_idletasks()
        steps_canvas.configure(scrollregion=steps_canvas.bbox("all"))
        steps_canvas.yview_moveto(0.0)

    btn_solve = tk.Button(input_frame, text="Solve Equation", bg=current_colors["accent"], fg="white", 
                          font=("Segoe UI", 10, "bold"), bd=0, cursor="hand2", 
                          padx=25, pady=10, command=solve)
    btn_solve.pack(pady=10, padx=20, anchor="w")

    # =========================
    # TAB 2: SETTINGS
    # =========================
    settings_tab = tk.Frame(notebook, bg=current_colors["bg"])
    notebook.add(settings_tab, text="  SETTINGS  ")

    settings_header = tk.Label(settings_tab, text="APP SETTINGS", font=("Segoe UI", 20, "bold"), 
                               fg=current_colors["accent"], bg=current_colors["bg"])
    settings_header.pack(anchor="w", padx=60, pady=(20, 5))

    settings_container = tk.Frame(settings_tab, bg=current_colors["card"], padx=30, pady=25, 
                                  highlightthickness=1, highlightbackground=current_colors["border"])
    settings_container.pack(fill=tk.X, padx=40, pady=5)

    def create_toggle(parent, text, variable, command=None):
        container = tk.Frame(parent, bg=parent["bg"])
        container.pack(anchor="w", pady=12, fill="x")
        lbl = tk.Label(container, text=text, font=("Segoe UI", 14), fg=current_colors["text"], bg=container["bg"])
        lbl.pack(side="left")
        canvas = tk.Canvas(container, width=50, height=26, bg=container["bg"], highlightthickness=0)
        canvas.pack(side="right")

        def _rounded_rect(x1, y1, x2, y2, r, **kwargs):
            canvas.create_arc(x1, y1, x1+r*2, y1+r*2, start=90, extent=90, **kwargs)
            canvas.create_arc(x2-r*2, y1, x2, y1+r*2, start=0, extent=90, **kwargs)
            canvas.create_arc(x2-r*2, y2-r*2, x2, y2, start=270, extent=90, **kwargs)
            canvas.create_arc(x1, y2-r*2, x1+r*2, y2, start=180, extent=90, **kwargs)
            canvas.create_rectangle(x1+r, y1, x2-r, y2, **kwargs)
            canvas.create_rectangle(x1, y1+r, x2, y2-r, **kwargs)

        def draw():
            canvas.delete("all")
            colors = themes["dark" if dark_mode.get() else "light"]
            bg_color = colors["accent"] if variable.get() else colors["border"]
            circle_x = 26 if variable.get() else 4
            _rounded_rect(2, 2, 48, 24, 11, fill=bg_color, outline="")
            canvas.create_oval(circle_x, 4, circle_x+18, 22, fill="white", outline="")

        def toggle(event=None):
            variable.set(not variable.get())
            draw()
            if command: command()

        container.bind("<Button-1>", toggle)
        canvas.bind("<Button-1>", toggle)
        lbl.bind("<Button-1>", toggle)
        variable._draw_func = draw
        draw()

    # =========================
    # TAB 3: INFO 
    # =========================
    info_tab = tk.Frame(notebook, bg=current_colors["bg"])
    notebook.add(info_tab, text="  ABOUT  ")
    info_canvas = tk.Canvas(info_tab, bg=current_colors["bg"], highlightthickness=0)
    info_scrollbar = ttk.Scrollbar(info_tab, orient="vertical", command=info_canvas.yview)
    info_frame = tk.Frame(info_canvas, bg=current_colors["bg"])
    info_window = info_canvas.create_window((0, 0), window=info_frame, anchor="nw")
    info_canvas.bind('<Configure>', lambda e: info_canvas.itemconfig(info_window, width=e.width))
    info_canvas.configure(yscrollcommand=info_scrollbar.set)
    info_scrollbar.pack(side="right", fill="y")
    info_canvas.pack(fill="both", expand=True)
    make_canvas_scrollable(info_canvas, info_frame)

    info_sections = [
        ("Lexical Specification (Scanner)", 
         "The scanner converts raw input strings into a stream of categorized tokens using the following character-class rules:\n"
         "• <NUM>   : Digit string with optional decimal: [0-9]+(\\.[0-9]+)?\n"
         "• <FUNC>  : Alphabetical identifier: [a-zA-Z]+ (Targets: sin, cos, log, int)\n"
         "• <OP>    : Mathematical operators: { +, -, *, /, ^, !, √ }\n"
         "• <DELIM> : Grouping/Parameter delimiters: { (, ), |, , }\n\n"
         "Phase logic: Whitespace is consumed and discarded; unrecognized characters trigger a Lexical Error."),

        ("Formal Grammar: BNF Definition", 
         "This language is defined by a Context-Free Grammar (CFG) that enforces mathematical precedence:\n\n"
         "<expression> ::= <term> { (+|-) <term> }\n"
         "<term>       ::= <factor> { (*|/) <factor> }\n"
         "<factor>     ::= <unary> [ ^ <factor> ]\n"
         "<unary>      ::= [ - | √ ] <primary> | <primary> !\n"
         "<primary>    ::= <number> \n"
         "               | '(' <expression> ')' \n"
         "               | '|' <expression> '|'\n"
         "               | <FUNC> '(' <arg_list> ')'\n"
         "<arg_list>   ::= <expression> { ',' <expression> }"),

        ("Operator Precedence & Associativity", 
         "The evaluator resolves operators in descending priority levels:\n"
         "Level 7: ( ) | |           -> Grouping (Highest)\n"
         "Level 6: sin cos log int   -> Functional Evaluation\n"
         "Level 5: !                 -> Postfix Unary\n"
         "Level 4: - √               -> Prefix Unary\n"
         "Level 3: ^                 -> Exponentiation (Right-associative)\n"
         "Level 2: * /               -> Multiplicative (Left-associative)\n"
         "Level 1: + -               -> Additive (Left-associative)"),

        ("Implementation Architecture", 
         "The system utilizes a multi-stage evaluation pipeline:\n"
         "1. Scanning: Linear character scan to produce a list of categorized objects.\n"
         "2. Syntactic Analysis: Uses a recursive reduction method where nested scopes (parentheses) are extracted and evaluated independently.\n"
         "3. Semantic Analysis: Definite integrals are resolved by parsing the 3-tuple parameter list into a distinct evaluation block.\n"
         "4. Traceback: Every transformation is recorded and pushed to the UI callback for step-by-step visibility.")
    ]

    def populate_info():
        for widget in info_frame.winfo_children(): widget.destroy()
        colors = themes["dark" if dark_mode.get() else "light"]
        for title, content in info_sections:
            tk.Label(info_frame, text=title.upper(), font=("Segoe UI", 20, "bold"), 
                     bg=colors["bg"], fg=colors["accent"]).pack(padx=40, pady=(25, 5), anchor="w")
            
            card = tk.Frame(info_frame, bg=colors["card"], padx=25, pady=20, 
                            highlightthickness=1, highlightbackground=colors["border"])
            card.pack(fill=tk.X, padx=40, pady=5)
            
            c_lbl = tk.Label(card, text=content, font=("Consolas", 14), bg=colors["card"], 
                             fg=colors["text"], justify="left", anchor="w")
            c_lbl.pack(fill=tk.X)
            card.bind("<Configure>", lambda e, l=c_lbl: l.configure(wraplength=e.width-50))
        info_frame.update_idletasks() 
        info_canvas.configure(scrollregion=info_canvas.bbox("all"))
        info_canvas.yview_moveto(0) 

    populate_info()

    def refresh_ui():
        mode = "dark" if dark_mode.get() else "light"
        colors = themes[mode]
        root.configure(bg=colors["bg"])
        update_notebook_styles(colors)
        for tab in [solver_tab, settings_tab, info_tab, input_frame, steps_frame, info_frame]:
            tab.configure(bg=colors["bg"])
        steps_canvas.configure(bg=colors["bg"])
        info_canvas.configure(bg=colors["bg"])
        lbl_input.configure(bg=colors["bg"], fg=colors["accent"])
        entry.configure(bg=colors["card"], fg=colors["text"], highlightbackground=colors["border"])
        btn_solve.configure(bg=colors["accent"])
        settings_container.configure(bg=colors["card"], highlightbackground=colors["border"])
        settings_header.configure(bg=colors["bg"], fg=colors["accent"])

        for child in settings_container.winfo_children():
            if isinstance(child, tk.Frame): 
                child.configure(bg=colors["card"])
                for sub in child.winfo_children():
                    if isinstance(sub, tk.Label): sub.configure(bg=colors["card"], fg=colors["text"])
                    if isinstance(sub, tk.Canvas): sub.configure(bg=colors["card"])


        for card in steps_frame.winfo_children():
            if "error_card" in str(card):
                card.destroy()
                continue

            if "result_header" in str(card):
                card.configure(bg=colors["bg"], fg=colors["accent"])
                continue
                
            is_result = "result_card" in str(card)
            bg_t = colors["result_bg"] if is_result else colors["card"]
            border_c = colors["accent"] if is_result else colors["border"]
            
            card.configure(bg=bg_t, highlightbackground=border_c)
            
            for sub in card.winfo_children():
                if isinstance(sub, tk.Label):
                    full = getattr(sub, "full_text", sub.cget("text"))
                    
                    if "Definition:" in full and not show_definitions.get():
                        new_text = full.split("Definition:")[0].strip()
                    else:
                        new_text = full
                    
                    sub.configure(text=new_text, bg=bg_t, fg=colors["text"])

        populate_info()
        show_definitions._draw_func()
        dark_mode._draw_func()

    create_toggle(settings_container, "Show Definitions", show_definitions, command=refresh_ui)
    create_toggle(settings_container, "Dark Mode", dark_mode, command=refresh_ui)

    def gui_output(text):
        card_data.append(text) 
        disp = text.split("Definition:")[0].strip() if "Definition:" in text and not show_definitions.get() else text
        colors = themes["dark" if dark_mode.get() else "light"]
        
        card = tk.Frame(steps_frame, bg=colors["card"], padx=20, pady=15, 
                        highlightthickness=1, highlightbackground=colors["border"])
        card.pack(fill=tk.X, pady=8)
        
        lbl = tk.Label(card, text=disp, font=("Consolas", 12), bg=colors["card"], 
                    fg=colors["text"], justify="left", anchor="w")
        
        lbl.full_text = text 
        
        lbl.pack(anchor="w", fill=tk.X)
        card.bind("<Configure>", lambda e, l=lbl: l.configure(wraplength=e.width-50))
        steps_frame.update_idletasks()
        steps_canvas.configure(scrollregion=steps_canvas.bbox("all"))

    global output_callback
    output_callback = gui_output
    root.mainloop()

if __name__ == "__main__":
    run_gui()
