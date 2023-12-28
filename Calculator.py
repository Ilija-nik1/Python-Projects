import tkinter as tk
import math

# Safe evaluation function
def safe_eval(expression):
    try:
        # Define safe local variables
        allowed_locals = {"math": math}
        return eval(expression, {"__builtins__": {}}, allowed_locals)
    except Exception as e:
        raise e

def handle_button_click(button_text):
    current_input = input_entry.get()
    input_entry.delete(0, tk.END)
    input_entry.insert(tk.END, current_input + button_text)

def handle_operation(operation):
    try:
        x = float(input_entry.get())
        input_entry.delete(0, tk.END)
        input_entry.insert(tk.END, str(x) + " " + operation + " ")
    except ValueError:
        input_entry.delete(0, tk.END)
        input_entry.insert(tk.END, "Invalid input")

def calculate():
    try:
        expression = input_entry.get()
        result = evaluate_expression(expression)
        output_entry.config(state=tk.NORMAL)
        output_entry.delete(0, tk.END)
        output_entry.insert(tk.END, str(result))
        output_entry.config(state=tk.DISABLED)
    except Exception:
        output_entry.config(state=tk.NORMAL)
        output_entry.delete(0, tk.END)
        output_entry.insert(tk.END, "Invalid expression")
        output_entry.config(state=tk.DISABLED)

def evaluate_expression(expression):
    try:
        return eval(expression)
    except Exception:
        return "Invalid expression"

# Updating the evaluate_expression function
def evaluate_expression(expression):
    try:
        return safe_eval(expression)
    except Exception as e:
        return f"Error: {str(e)}"

def clear():
    input_entry.delete(0, tk.END)
    output_entry.config(state=tk.NORMAL)
    output_entry.delete(0, tk.END)
    output_entry.config(state=tk.DISABLED)

def backspace():
    current_input = input_entry.get()
    input_entry.delete(len(current_input) - 1, tk.END)

def calculate_square_root():
    try:
        x = float(input_entry.get())
        result = math.sqrt(x)
        output_entry.config(state=tk.NORMAL)
        output_entry.delete(0, tk.END)
        output_entry.insert(tk.END, str(result))
        output_entry.config(state=tk.DISABLED)
    except ValueError:
        input_entry.delete(0, tk.END)
        input_entry.insert(tk.END, "Invalid input")

def calculate_power():
    try:
        x = float(input_entry.get())
        result = x ** 2  # You can modify this to use a different power
        output_entry.config(state=tk.NORMAL)
        output_entry.delete(0, tk.END)
        output_entry.insert(tk.END, str(result))
        output_entry.config(state=tk.DISABLED)
    except ValueError:
        input_entry.delete(0, tk.END)
        input_entry.insert(tk.END, "Invalid input")

def on_key_press(event):
    if event.char in "1234567890.+-*/":
        handle_button_click(event.char)
    elif event.keysym.lower() == "c":
        clear()
    elif event.keysym.lower() == "return":
        calculate()
    elif event.keysym.lower() == "BackSpace":
        backspace()

window = tk.Tk()
window.title("Calculator")

input_entry = tk.Entry(window)
input_entry.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

output_entry = tk.Entry(window, state=tk.DISABLED)
output_entry.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

numpad_buttons = [
    {"text": "7", "command": lambda: handle_button_click("7")},
    {"text": "8", "command": lambda: handle_button_click("8")},
    {"text": "9", "command": lambda: handle_button_click("9")},
    {"text": "4", "command": lambda: handle_button_click("4")},
    {"text": "5", "command": lambda: handle_button_click("5")},
    {"text": "6", "command": lambda: handle_button_click("6")},
    {"text": "1", "command": lambda: handle_button_click("1")},
    {"text": "2", "command": lambda: handle_button_click("2")},
    {"text": "3", "command": lambda: handle_button_click("3")},
    {"text": "0", "command": lambda: handle_button_click("0")},
    {"text": ".", "command": lambda: handle_button_click(".")},
    {"text": "<-", "command": backspace},
]

row = 2
col = 0
for button_data in numpad_buttons:
    button = tk.Button(window, text=button_data["text"], width=5, command=button_data["command"])
    button.grid(row=row, column=col, padx=5, pady=5)
    col += 1
    if col > 2:
        col = 0
        row += 1

operation_buttons = [
    {"text": "+", "command": lambda: handle_operation("+")},
    {"text": "-", "command": lambda: handle_operation("-")},
    {"text": "*", "command": lambda: handle_operation("*")},
    {"text": "/", "command": lambda: handle_operation("/")},
    {"text": "=", "command": calculate},
    {"text": "√", "command": calculate_square_root},
    {"text": "x^2", "command": calculate_power},
]

# Adding more buttons for advanced operations
advanced_operation_buttons = [
    # Add more buttons like for trigonometric functions, logarithms, etc.
    {"text": "sin", "command": lambda: handle_operation("math.sin(")},
    {"text": "cos", "command": lambda: handle_operation("math.cos(")},
    {"text": "tan", "command": lambda: handle_operation("math.tan(")},
]

row = 2
col = 3
for button_data in operation_buttons:
    button = tk.Button(window, text=button_data["text"], width=5, command=button_data["command"])
    button.grid(row=row, column=col, padx=5, pady=5)
    row += 1

clear_button = tk.Button(window, text="C", width=5, command=clear)
clear_button.grid(row=row, column=col, padx=5, pady=5)

window.bind("<Key>", on_key_press)

window.mainloop()