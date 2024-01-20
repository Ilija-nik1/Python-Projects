import tkinter as tk
import math

# Safe evaluation function
def safe_eval(expression):
    try:
        # Add more validation and allowed functions as necessary
        allowed_locals = {"math": math, "pi": math.pi, "e": math.e}
        return eval(expression, {"__builtins__": {}}, allowed_locals)
    except Exception as e:
        return f"Error: {str(e)}"

class CalculatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Advanced Calculator")

        self.input_entry = tk.Entry(master, font=("Arial", 14))
        self.input_entry.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky="nsew")

        self.output_entry = tk.Entry(master, font=("Arial", 14), state=tk.DISABLED)
        self.output_entry.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky="nsew")

        self.create_buttons()
        master.bind("<Key>", self.on_key_press)

    def create_buttons(self):
        numpad_buttons = ["7", "8", "9", "4", "5", "6", "1", "2", "3", "0", "."]
        row, col = 2, 0
        for btn in numpad_buttons:
            button = tk.Button(self.master, text=btn, font=("Arial", 12),
                               command=lambda b=btn: self.append_to_input(b))
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            col += 1
            if col > 2:
                col = 0
                row += 1

        operation_buttons = ["+", "-", "*", "/", "=", "√", "x^2", "(", ")", "C", "<-", "sin", "cos", "tan", "log", "exp", "π", "e"]
        row, col = 2, 3
        for btn in operation_buttons:
            button = tk.Button(self.master, text=btn, font=("Arial", 12),
                               command=lambda b=btn: self.handle_operation(b))
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            row += 1
            if row > 7:
                row = 2
                col += 1

        # Make all columns and rows expandable
        for i in range(5):
            self.master.grid_columnconfigure(i, weight=1)
        for i in range(8):
            self.master.grid_rowconfigure(i, weight=1)

    def append_to_input(self, char):
        current_pos = self.input_entry.index(tk.INSERT)
        self.input_entry.insert(current_pos, char)

    def handle_operation(self, operation):
        if operation == "C":
            self.clear()
        elif operation == "<-":
            self.backspace()
        elif operation == "=":
            self.calculate()
        elif operation in ["sin", "cos", "tan", "log", "exp"]:
            self.append_to_input(f"math.{operation}(")
        elif operation == "π":
            self.append_to_input("math.pi")
        elif operation == "e":
            self.append_to_input("math.e")
        elif operation in ["+", "-", "*", "/", "(", ")"]:
            self.append_to_input(operation)
        elif operation == "√":
            self.append_to_input("math.sqrt(")
        elif operation == "x^2":
            self.append_to_input("**2")

    def calculate(self):
        expression = self.input_entry.get()
        result = safe_eval(expression)
        self.output_entry.config(state=tk.NORMAL)
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(tk.END, str(result))
        self.output_entry.config(state=tk.DISABLED)

    def clear(self):
        self.input_entry.delete(0, tk.END)
        self.output_entry.config(state=tk.NORMAL)
        self.output_entry.delete(0, tk.END)
        self.output_entry.config(state=tk.DISABLED)

    def backspace(self):
        current_pos = self.input_entry.index(tk.INSERT)
        if current_pos > 0:
            self.input_entry.delete(current_pos - 1)

    def on_key_press(self, event):
        if event.char in "1234567890.+-*/()":
            self.append_to_input(event.char)
        elif event.keysym == "Left":
            self.move_cursor(-1)
        elif event.keysym == "Right":
            self.move_cursor(1)
        elif event.keysym.lower() == "c":
            self.clear()
        elif event.keysym == "Return":
            self.calculate()
        elif event.keysym == "BackSpace":
            self.backspace()

    def move_cursor(self, direction):
        current_pos = self.input_entry.index(tk.INSERT)
        if direction < 0 and current_pos > 0:
            self.input_entry.icursor(current_pos - 1)
        elif direction > 0 and current_pos < len(self.input_entry.get()):
            self.input_entry.icursor(current_pos + 1)

def main():
    root = tk.Tk()
    root.geometry("400x500")
    app = CalculatorApp(root)
    root.resizable(True, True)  # Making the window resizable
    root.mainloop()

if __name__ == "__main__":
    main()