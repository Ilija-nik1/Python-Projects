from tkinter import Tk, Label, Entry, StringVar, OptionMenu, Button, messagebox
import math

class Converter:
    # Define constants
    WINDOW_TITLE = "Number System Converter"
    INPUT_LABEL_TEXT = "Enter your number:"
    INPUT_SYSTEM_LABEL_TEXT = "Input system:"
    OUTPUT_SYSTEM_LABEL_TEXT = "Output system:"
    CONVERT_BUTTON_TEXT = "Convert"
    RESULT_LABEL_TEXT = "{} in {} = {} in {}"

    # Define dictionaries for converting between number systems
    SYSTEMS = {
        "Decimal": 10,
        "Binary": 2,
        "Octal": 8,
        "Hexadecimal": 16
    }
    TO_DECIMAL = {
        "Binary": lambda x: int(x, 2),
        "Octal": lambda x: int(x, 8),
        "Decimal": lambda x: int(x),
        "Hexadecimal": lambda x: int(x, 16)
    }
    FROM_DECIMAL = {
        "Binary": lambda x: bin(x)[2:],
        "Octal": lambda x: oct(x)[2:],
        "Decimal": lambda x: str(x),
        "Hexadecimal": lambda x: hex(x)[2:]
    }

    def __init__(self, master):
        # Initialize the GUI
        self.master = master
        master.title(self.WINDOW_TITLE)

        # Designing window for input and output
        self.input_label = Label(master, text=self.INPUT_LABEL_TEXT)
        self.input_label.grid(row=0, column=0)

        self.input_entry = Entry(master)
        self.input_entry.grid(row=0, column=1)

        self.input_system_label = Label(master, text=self.INPUT_SYSTEM_LABEL_TEXT)
        self.input_system_label.grid(row=1, column=0)

        self.input_system_var = StringVar(master)
        self.input_system_var.set("Decimal")
        self.input_system_menu = OptionMenu(master, self.input_system_var, *self.SYSTEMS.keys())
        self.input_system_menu.grid(row=1, column=1)

        self.output_system_label = Label(master, text=self.OUTPUT_SYSTEM_LABEL_TEXT)
        self.output_system_label.grid(row=2, column=0)

        self.output_system_var = StringVar(master)
        self.output_system_var.set("Binary")
        self.output_system_menu = OptionMenu(master, self.output_system_var, *self.SYSTEMS.keys())
        self.output_system_menu.grid(row=2, column=1)

        # Submit Button
        self.submit_button = Button(master, text=self.CONVERT_BUTTON_TEXT, command=self.convert)
        self.submit_button.grid(row=3, column=0)

        # Copy to Clipboard Button
        self.copy_button = Button(master, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.grid(row=3, column=1)

        # Clear Button
        self.clear_button = Button(master, text="Clear", command=self.clear)
        self.clear_button.grid(row=3, column=2)

        # Label to display the result
        self.result_label = Label(master, text="")
        self.result_label.grid(row=4, columnspan=3)

    def convert(self):
        # Get the input value and number system
        input_value = self.input_entry.get()
        input_system = self.input_system_var.get()
        output_system = self.output_system_var.get()

        # Validate input for the selected input system
        if not self.is_valid_input(input_value, input_system):
            messagebox.showerror("Error", "Invalid input for selected input system.")
            return

        # Convert input value to decimal
        try:
            decimal_value = self.TO_DECIMAL[input_system](input_value)
        except ValueError:
            messagebox.showerror("Error", "Invalid input for selected input system.")
            return

        # Convert decimal value to output system
        output_value = self.FROM_DECIMAL[output_system](decimal_value)

        # Display the result in a label
        self.result_label.config(text=self.RESULT_LABEL_TEXT.format(input_value, input_system, output_value, output_system))

    def is_valid_input(self, input_value, input_system):
        if input_system == "Binary":
            return all(char in "01" for char in input_value)
        elif input_system == "Octal":
            return all(char in "01234567" for char in input_value)
        elif input_system == "Decimal":
            return input_value.isdigit()
        elif input_system == "Hexadecimal":
            return all(char in "0123456789ABCDEF" for char in input_value)
        else:
            return False

    def copy_to_clipboard(self):
        output_value = self.result_label.cget("text")
        self.master.clipboard_clear()
        self.master.clipboard_append(output_value)

    def clear(self):
        self.input_entry.delete(0, "end")
        self.result_label.config(text="")

# Create window object
root = Tk()
converter = Converter(root)

# End the loop when window is closed
root.mainloop()