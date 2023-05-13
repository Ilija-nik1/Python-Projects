import tkinter as tk
import random

# Constants
SIDES_LABEL_TEXT = "Number of sides:"
MIN_SIDES = 1

class DiceRollerGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Dice Roller")
        self.pack(padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        # Create labels and entry widgets
        self.sides_label = tk.Label(self, text=SIDES_LABEL_TEXT)
        self.sides_label.grid(row=0, column=0, padx=5, pady=5)
        self.sides_entry = tk.Entry(self, width=5)
        self.sides_entry.grid(row=0, column=1, padx=5, pady=5)

        # Create the Roll button
        self.roll_button = tk.Button(self, text="Roll", command=self.roll_dice)
        self.roll_button.grid(row=0, column=2, padx=5, pady=5)

        # Create the result label
        self.result_label = tk.Label(self, text="")
        self.result_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

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

    def show_error(self, message):
        # Display an error message in a popup dialog box
        tk.messagebox.showerror("Error", message)


if __name__ == '__main__':
    root = tk.Tk()
    app = DiceRollerGUI(master=root)
    app.mainloop()