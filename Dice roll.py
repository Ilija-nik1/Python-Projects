import tkinter as tk
import random

class DiceRollerGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Dice Roller")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.sides_label = tk.Label(self, text="Number of Sides:")
        self.sides_label.pack()
        self.sides_entry = tk.Entry(self)
        self.sides_entry.pack()
        self.roll_button = tk.Button(self, text="Roll", command=self.roll_dice)
        self.roll_button.pack()
        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

    def roll_dice(self):
        num_sides = int(self.sides_entry.get())
        roll_result = random.randint(1, num_sides)
        self.result_label.config(text=f"You rolled a {roll_result}!")

root = tk.Tk()
app = DiceRollerGUI(master=root)
app.mainloop()