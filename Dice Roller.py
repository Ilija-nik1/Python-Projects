import tkinter as tk
import random
from tkinter import messagebox

# Constants
SIDES_LABEL_TEXT = "Number of sides:"
MIN_SIDES = 1

class DiceRollerGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#282c34")  # Set the background color to dark gray
        self.master = master
        self.master.title("Dice Roller")
        self.pack(padx=10, pady=10)
        self.create_widgets()

        # Store roll history
        self.roll_history = []

    def create_widgets(self):
        # Create labels and entry widgets
        self.sides_label = tk.Label(self, text=SIDES_LABEL_TEXT, bg="#282c34", fg="white")  # Set the background color to dark gray and text color to white
        self.sides_label.grid(row=0, column=0, padx=5, pady=5, sticky="E")
        self.sides_entry = tk.Entry(self, width=10, bg="white", fg="black")  # Set the background color to white and text color to black
        self.sides_entry.grid(row=0, column=1, padx=5, pady=5)

        # Create the Roll button
        self.roll_button = tk.Button(self, text="Roll", command=self.roll_dice, bg="#61afef", fg="white")  # Set the background color to blue and text color to white
        self.roll_button.grid(row=0, column=2, padx=5, pady=5)

        # Create the Clear button
        self.clear_button = tk.Button(self, text="Clear", command=self.clear_fields, bg="#e06c75", fg="white")  # Set the background color to red and text color to white
        self.clear_button.grid(row=0, column=3, padx=5, pady=5)

        # Create the result label
        self.result_label = tk.Label(self, text="", font=("Arial", 14, "bold"), bg="#282c34", fg="white")  # Set the background color to dark gray and text color to white
        self.result_label.grid(row=1, column=0, columnspan=4, padx=5, pady=10)

        # Create the history label
        self.history_label = tk.Label(self, text="Roll History:", bg="#282c34", fg="white")
        self.history_label.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

        # Create the history text area
        self.history_text = tk.Text(self, height=5, width=30, bg="white", fg="black")
        self.history_text.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

    def roll_dice(self):
        # Validate user input
        try:
            num_sides = int(self.sides_entry.get())
            if num_sides < MIN_SIDES:
                raise ValueError("Number of sides must be greater than 0")
        except ValueError:
            self.show_error("Invalid input")
            return

        # Roll the dice and update the result label
        roll_result = random.randint(1, num_sides)
        self.result_label.config(text=f"You rolled a {roll_result}!")

        # Add result to history
        self.roll_history.append(roll_result)
        self.update_history_text()

    def clear_fields(self):
        # Clear the input and result fields
        self.sides_entry.delete(0, tk.END)
        self.result_label.config(text="")

    def update_history_text(self):
        # Update the history text area with the latest roll results
        self.history_text.delete(1.0, tk.END)
        for roll in self.roll_history:
            self.history_text.insert(tk.END, f"Roll: {roll}\n")

    def show_error(self, message):
        # Display an error message in a popup dialog box
        messagebox.showerror("Error", message)


if __name__ == '__main__':
    root = tk.Tk()
    app = DiceRollerGUI(master=root)
    app.mainloop()