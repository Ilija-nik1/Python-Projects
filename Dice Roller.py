import tkinter as tk
import random

class DiceRollerGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Dice Roller")
        self.pack(padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        self.sides_label = tk.Label(self, text="Number of sides:")
        self.sides_label.grid(row=0, column=0, padx=5, pady=5)
        self.sides_entry = tk.Entry(self, width=5)
        self.sides_entry.grid(row=0, column=1, padx=5, pady=5)
        self.roll_button = tk.Button(self, text="Roll", command=self.roll_dice)
        self.roll_button.grid(row=0, column=2, padx=5, pady=5)
        self.result_label = tk.Label(self, text="")
        self.result_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

    def roll_dice(self):
        try:
            num_sides = int(self.sides_entry.get())
            if num_sides < 1:
                raise ValueError("Number of sides must be greater than 0")
            roll_result = random.randint(1, num_sides)
            self.result_label.config(text=f"You rolled a {roll_result}!")
        except ValueError as e:
            self.result_label.config(text=str(e))

root = tk.Tk()
app = DiceRollerGUI(master=root)
app.mainloop()