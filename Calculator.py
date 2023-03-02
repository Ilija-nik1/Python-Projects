import tkinter as tk

# Functions to perform calculations
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y

def power(x, y):
    return x ** y

def square_root(x):
    if x < 0:
        raise ValueError("Cannot take square root of negative number")
    return x ** 0.5

def absolute_value(x):
    return abs(x)

def modulo(x, y):
    return x % y

# Create the GUI window
window = tk.Tk()
window.title("Calculator")

# Create the user interface widgets
label1 = tk.Label(window, text="Enter first number:")
label1.grid(row=0, column=0, padx=5, pady=5)
entry1 = tk.Entry(window)
entry1.grid(row=0, column=1, padx=5, pady=5)
label2 = tk.Label(window, text="Enter second number:")
label2.grid(row=1, column=0, padx=5, pady=5)
entry2 = tk.Entry(window)
entry2.grid(row=1, column=1, padx=5, pady=5)

# Create the operation buttons
operation_buttons = [
    {"text": "Add", "function": add},
    {"text": "Subtract", "function": subtract},
    {"text": "Multiply", "function": multiply},
    {"text": "Divide", "function": divide},
    {"text": "Power", "function": power},
    {"text": "Square Root", "function": square_root},
    {"text": "Absolute Value", "function": absolute_value},
    {"text": "Modulo", "function": modulo},
]

def calculate(func):
    try:
        x = float(entry1.get())
        y = float(entry2.get())
        result = func(x, y)
        result_label.config(text=f"Result: {result}")
    except ValueError as e:
        result_label.config(text=str(e))

for i, button in enumerate(operation_buttons):
    button = tk.Button(window, text=button["text"], width=15, command=lambda func=button["function"]: calculate(func))
    button.grid(row=i+2, column=0 if i%2==0 else 1, padx=5, pady=5)

# Create the result label
result_label = tk.Label(window, text="")
result_label.grid(row=len(operation_buttons)+2, column=0, columnspan=2, padx=5, pady=5)

# Create the clear button
clear_button = tk.Button(window, text="Clear", command=lambda: [entry1.delete(0, tk.END), entry2.delete(0, tk.END), result_label.config(text="")])
clear_button.grid(row=len(operation_buttons)+3, column=0, columnspan=2, padx=5, pady=5)

# Run the GUI window
window.mainloop()