import tkinter as tk
from tkinter import messagebox
import random

BACKGROUND_COLOR = "#282c34"
LABEL_COLOR = "white"
ENTRY_BACKGROUND = "white"
ENTRY_TEXT_COLOR = "black"
BUTTON_BACKGROUND = "#61afef"
BUTTON_TEXT_COLOR = "white"
ERROR_COLOR = "#e06c75"
MIN_SIDES = 1
DICE_FACES = [1, 2, 3, 4, 5, 6]
ANIMATION_ITERATIONS = 10
ANIMATION_DELAY = 100

class DiceRollerGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg=BACKGROUND_COLOR)
        self.master = master
        self.master.title("Dice Roller")
        self.pack(padx=10, pady=10)
        self.create_widgets()

        # Store roll history
        self.roll_history = []

    def create_widgets(self):
        self.create_label_entry_button_widgets()
        self.create_result_label()
        self.create_history_widgets()

    def create_label_entry_button_widgets(self):
        self.sides_label = self.create_label("Number of sides:")
        self.sides_entry = self.create_entry(width=10)
        self.roll_button = self.create_button("Roll", self.roll_dice)
        self.clear_button = self.create_button("Clear", self.clear_fields)

    def create_result_label(self):
        self.result_label = self.create_label("", font=("Arial", 14, "bold"))
        self.history_label = self.create_label("Roll History:", anchor="w")
        self.history_text = self.create_text(height=5, width=30)

        self.history_scrollbar = tk.Scrollbar(self, command=self.history_text.yview)
        self.history_scrollbar.grid(row=3, column=4, sticky="NS")
        self.history_text.config(yscrollcommand=self.history_scrollbar.set)

    def create_history_widgets(self):
        self.history_text = self.create_text(height=5, width=30)
        self.history_scrollbar = tk.Scrollbar(self, command=self.history_text.yview)
        self.history_scrollbar.grid(row=3, column=4, sticky="NS")
        self.history_text.config(yscrollcommand=self.history_scrollbar.set)

    def create_label(self, text, **kwargs):
        label = tk.Label(self, text=text, bg=BACKGROUND_COLOR, fg=LABEL_COLOR, **kwargs)
        label.grid(padx=5, pady=5, sticky="E")
        return label

    def create_entry(self, **kwargs):
        entry = tk.Entry(self, bg=ENTRY_BACKGROUND, fg=ENTRY_TEXT_COLOR, **kwargs)
        entry.grid(padx=5, pady=5)
        return entry

    def create_button(self, text, command, **kwargs):
        button = tk.Button(self, text=text, command=command, bg=BUTTON_BACKGROUND, fg=BUTTON_TEXT_COLOR, **kwargs)
        button.grid(padx=5, pady=5)
        return button

    def create_text(self, **kwargs):
        text = tk.Text(self, bg=ENTRY_BACKGROUND, fg=ENTRY_TEXT_COLOR, **kwargs)
        text.grid(padx=5, pady=5)
        return text

    def roll_dice(self):
        try:
            num_sides = int(self.sides_entry.get())
            if num_sides < MIN_SIDES:
                raise ValueError("Number of sides must be greater than 0")
        except tk.TclError:
            self.show_error("Invalid input")
            return

        self.animate_dice_roll(num_sides, ANIMATION_ITERATIONS)

    def animate_dice_roll(self, num_sides, iterations):
        def update_dice_face():
            roll_result = random.choice(DICE_FACES)
            self.result_label.config(text=f"You rolled a {roll_result}!")

        def end_animation():
            roll_result = random.randint(1, num_sides)
            self.result_label.config(text=f"You rolled a {roll_result}!")
            self.roll_history.append(roll_result)
            self.update_history_text()

        def animation_loop(current_iteration):
            if current_iteration < iterations:
                update_dice_face()
                self.after(ANIMATION_DELAY, animation_loop, current_iteration + 1)
            else:
                end_animation()

        animation_loop(0)

    def clear_fields(self):
        if messagebox.askokcancel("Clear Fields", "Are you sure you want to clear the fields?"):
            self.sides_entry.delete(0, tk.END)
            self.result_label.config(text="")

    def update_history_text(self):
        self.history_text.delete(1.0, tk.END)
        for roll in self.roll_history:
            self.history_text.insert(tk.END, f"Roll: {roll}\n")
        self.history_text.see(tk.END)

    def show_error(self, message):
        messagebox.showerror("Error", message)

if __name__ == '__main__':
    root = tk.Tk()
    app = DiceRollerGUI(master=root)
    app.mainloop()