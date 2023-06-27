import tkinter as tk

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
        result = eval(expression)
        output_entry.config(state=tk.NORMAL)
        output_entry.delete(0, tk.END)
        output_entry.insert(tk.END, str(result))
        output_entry.config(state=tk.DISABLED)
    except ZeroDivisionError:
        output_entry.config(state=tk.NORMAL)
        output_entry.delete(0, tk.END)
        output_entry.insert(tk.END, "Division by zero")
        output_entry.config(state=tk.DISABLED)
    except (SyntaxError, NameError, TypeError):
        output_entry.config(state=tk.NORMAL)
        output_entry.delete(0, tk.END)
        output_entry.insert(tk.END, "Invalid expression")
        output_entry.config(state=tk.DISABLED)

def clear():
    input_entry.delete(0, tk.END)
    output_entry.config(state=tk.NORMAL)
    output_entry.delete(0, tk.END)
    output_entry.config(state=tk.DISABLED)

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
]

row = 2
col = 3
for button_data in operation_buttons:
    button = tk.Button(window, text=button_data["text"], width=5, command=button_data["command"])
    button.grid(row=row, column=col, padx=5, pady=5)
    row += 1

clear_button = tk.Button(window, text="C", width=5, command=clear)
clear_button.grid(row=row, column=col, padx=5, pady=5)

window.mainloop()