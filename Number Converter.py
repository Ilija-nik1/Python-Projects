from tkinter import *
from tkinter import messagebox

class Converter:
    # Define constants
    WINDOW_TITLE = "Decimal to Binary/Octal/Hexadecimal Converter"
    LABEL_TEXT = "Enter your Decimal:"
    CONVERT_BUTTON_TEXT = "Convert"
    RESULT_LABEL_TEXT = "Decimal: {}\nBinary: {}\nOctal: {}\nHexadecimal: {}"
    
    def __init__(self, master):
        self.master = master
        master.title(self.WINDOW_TITLE)
        
        # Designing window for registration
        self.label1 = Label(master, text=self.LABEL_TEXT)
        self.label1.grid(row=0, column=0)

        self.dec_entry = Entry(master)
        self.dec_entry.grid(row=0, column=1)

        # Submit Button
        self.submit_button = Button(master, text=self.CONVERT_BUTTON_TEXT, command=self.convert)
        self.submit_button.grid(row=1, columnspan=2)

        # Label to display the result
        self.result_label = Label(master, text="")
        self.result_label.grid(row=2, columnspan=2)

    def convert(self):
        # Get the value from Entry field
        try:
            dec_value = int(self.dec_entry.get())
            if dec_value < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a positive integer.")
            return

        # Convert to binary, octal, and hexadecimal
        bin_value = bin(dec_value)[2:]
        oct_value = oct(dec_value)[2:]
        hex_value = hex(dec_value)[2:]

        # Display the result in a label
        self.result_label.config(text=self.RESULT_LABEL_TEXT.format(dec_value, bin_value, oct_value, hex_value))

# Create window object
root = Tk()
converter = Converter(root)

# End the loop when window is closed
root.mainloop()