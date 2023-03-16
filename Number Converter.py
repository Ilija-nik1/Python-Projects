from tkinter import *
from tkinter import messagebox

# Create window object
root = Tk()
root.title("Decimal to Binary/Octal/Hexadecimal Converter")

# Function to convert decimal to binary, octal, and hexadecimal
def convert():
    try:
        # Get the value from Entry field
        dec_value = int(dec_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid decimal number")
        return

    # Convert to binary, octal, and hexadecimal
    bin_value = bin(dec_value)[2:]
    oct_value = oct(dec_value)[2:]
    hex_value = hex(dec_value)[2:]

    # Display the result in a label
    result_label.config(text="Decimal: {}\nBinary: {}\nOctal: {}\nHexadecimal: {}"
                                 .format(dec_value, bin_value, oct_value, hex_value))

# Designing window for registration
label1 = Label(root, text="Enter your Decimal:")
label1.grid(row=0, column=0)

dec_entry = Entry(root)
dec_entry.grid(row=0, column=1)

# Submit Button
submit_button = Button(root, text="Convert", command=convert)
submit_button.grid(row=1, columnspan=2)

# Label to display the result
result_label = Label(root, text="")
result_label.grid(row=2, columnspan=2)

# End the loop when window is closed
root.mainloop()