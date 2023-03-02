# Import necessary modules  
from tkinter import * 
from tkinter import messagebox 
  
# Create window object 
window = Tk() 
  
# Function to get input from user, call conversion functions  
# and display the result 
def convert(): 
      
    # Get the value from Entry field  
    dec_value = int(dec_entry.get()) 
  
    bin_value = bin(dec_value) 
    oct_value = oct(dec_value) 
    hex_value = hex(dec_value) 
  
    # Display the result in message box 
    messagebox.showinfo("Result", 
                        "Decimal: " + str(dec_value) +  
                         "\nBinary: " + str(bin_value)[2::] + 
                         "\nOctal: " + str(oct_value)[2::] + 
                         "\nHexadecimal: " + str(hex_value)[2::]) 
      
# Designing window for registration 
label1 = Label(window, text="Enter your Decimal") 
label1.grid(row=0, column=0) 
  
dec_entry = Entry(window) 
dec_entry.grid(row=0, column=1) 
  
# Submit Button 
Button(window, text="Convert", command=convert).grid(row=1,columnspan=2) 
  
# End the loop when window is closed 
window.mainloop() 