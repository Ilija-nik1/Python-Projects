import tkinter as tk

# Functions to perform calculations
def add():
    try:
        x = float(entry.get())
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(x) + " + ")
    except ValueError:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Invalid input")

def subtract():
    try:
        x = float(entry.get())
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(x) + " - ")
    except ValueError:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Invalid input")

def multiply():
    try:
        x = float(entry.get())
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(x) + " * ")
    except ValueError:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Invalid input")

def divide():
    try:
        x = float(entry.get())
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(x) + " / ")
    except ValueError:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Invalid input")

def calculate():
    try:
        expression = entry.get()
        result = eval(expression)
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

def clear():
    entry.delete(0, tk.END)

# Create the GUI window
window = tk.Tk()
window.title("Calculator")

# Create the entry widget
entry = tk.Entry(window)
entry.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

# Create the numpad buttons
numpad_buttons = [
    {"text": "7", "command": lambda: entry.insert(tk.END, "7")},
    {"text": "8", "command": lambda: entry.insert(tk.END, "8")},
    {"text": "9", "command": lambda: entry.insert(tk.END, "9")},
    {"text": "4", "command": lambda: entry.insert(tk.END, "4")},
    {"text": "5", "command": lambda: entry.insert(tk.END, "5")},
    {"text": "6", "command": lambda: entry.insert(tk.END, "6")},
    {"text": "1", "command": lambda: entry.insert(tk.END, "1")},
    {"text": "2", "command": lambda: entry.insert(tk.END, "2")},
    {"text": "3", "command": lambda: entry.insert(tk.END, "3")},
    {"text": "0", "command": lambda: entry.insert(tk.END, "0")},
    {"text": ".", "command": lambda: entry.insert(tk.END, ".")},
]

row = 1
col = 0
for button_data in numpad_buttons:
    button = tk.Button(window, text=button_data["text"], width=5, command=button_data["command"])
    button.grid(row=row, column=col, padx=5, pady=5)
    col += 1
    if col > 2:
        col = 0
        row += 1

# Create the operation buttons
operation_buttons = [
    {"text": "+", "command": add},
    {"text": "-", "command": subtract},
    {"text": "*", "command": multiply},
    {"text": "/", "command": divide},
    {"text": "=", "command": calculate},
]

row = 1
col = 3
for button_data in operation_buttons:
    button = tk.Button(window, text=button_data["text"], width=5, command=button_data["command"])
    button.grid(row=row, column=col, padx=5, pady=5)
    row += 1

# Create the clear button
clear_button = tk.Button(window, text="C", width=5, command=clear)
clear_button.grid(row=row, column=col, padx=5, pady=5)

# Run the GUI window
window.mainloop()